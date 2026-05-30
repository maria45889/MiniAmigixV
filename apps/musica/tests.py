"""
Tests for the musica app – lyrics fetching, caching, persistence and force refresh.
Run with: python manage.py test apps.musica
"""

from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse

from .models import Cancion
from .utils.lyrics_provider import (
    fetch_lrclib,
    fetch_lyrics_ovh,
    build_google_fallback,
    get_lyrics,
)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

class CancionModelTest(TestCase):
    def test_str_with_artist(self):
        c = Cancion(titulo="Bohemian Rhapsody", artista="Queen")
        self.assertEqual(str(c), "Bohemian Rhapsody – Queen")

    def test_str_without_artist(self):
        c = Cancion(titulo="Unknown Song")
        self.assertEqual(str(c), "Unknown Song")

    def test_tiene_letra_true(self):
        c = Cancion(titulo="T", letra="Some lyrics here")
        self.assertTrue(c.tiene_letra())

    def test_tiene_letra_false_empty(self):
        c = Cancion(titulo="T", letra="")
        self.assertFalse(c.tiene_letra())

    def test_tiene_letra_false_whitespace(self):
        c = Cancion(titulo="T", letra="   ")
        self.assertFalse(c.tiene_letra())


# ---------------------------------------------------------------------------
# lyrics_provider tests
# ---------------------------------------------------------------------------

class GetLyricsTest(TestCase):

    # ── Layer 1: cache hit ────────────────────────────────────────────────

    def test_cache_hit_returns_db_lyrics(self):
        """Canción exists with lyrics → source=cache, no API call."""
        Cancion.objects.create(titulo="Chantaje", artista="Shakira", letra="Na na na...", synced_lyrics="")

        with patch("apps.musica.utils.lyrics_provider.fetch_lrclib") as mock_lrclib, \
             patch("apps.musica.utils.lyrics_provider.fetch_lyrics_ovh") as mock_ovh:

            result = get_lyrics("Chantaje", "Shakira")

        self.assertTrue(result["success"])
        self.assertEqual(result["source"], "cache")
        self.assertTrue(result["cached"])
        self.assertIn("Na na na", result["lyrics"])
        mock_lrclib.assert_not_called()
        mock_ovh.assert_not_called()

    # ── Layer 2: cache miss – fetch and persist ───────────────────────────

    def test_fetch_and_persist_missing_lyrics(self):
        """Canción exists but letra='' → API fetches and persists."""
        cancion = Cancion.objects.create(titulo="Hips Don't Lie", artista="Shakira", letra="", synced_lyrics="")

        lrclib_result = {'lyrics': 'Oh baby when you talk like that...', 'synced': '[00:01.00]Oh baby...'}

        with patch("apps.musica.utils.lyrics_provider.fetch_lrclib", return_value=lrclib_result):
            result = get_lyrics("Hips Don't Lie", "Shakira")

        self.assertTrue(result["success"])
        self.assertEqual(result["source"], "api_primary")
        self.assertFalse(result["cached"])

        cancion.refresh_from_db()
        self.assertIn("Oh baby", cancion.letra)
        self.assertIn("[00:01.00]", cancion.synced_lyrics)

    # ── Layer 3: song not in DB, fetched and created ─────────────────────

    def test_song_not_found_in_db_still_fetches(self):
        """Canción does NOT exist in DB → fetched and new record created."""
        self.assertEqual(Cancion.objects.count(), 0)

        lrclib_result = {'lyrics': 'Waka waka eh eh...', 'synced': ''}

        with patch("apps.musica.utils.lyrics_provider.fetch_lrclib", return_value=lrclib_result):
            result = get_lyrics("Waka Waka", "Shakira")

        self.assertTrue(result["success"])
        self.assertEqual(result["source"], "api_primary")
        self.assertEqual(Cancion.objects.count(), 1)

        saved = Cancion.objects.first()
        self.assertIn("Waka waka", saved.letra)

    # ── Layer 4: force_refresh bypasses cache ──────────────────────────────

    def test_force_refresh_bypasses_cache(self):
        """DB has old lyrics; refresh=1 should fetch new and update DB."""
        Cancion.objects.create(titulo="Old Song", artista="Old Artist", letra="Old lyrics", synced_lyrics="")

        new_result = {'lyrics': 'Brand new lyrics!', 'synced': '[00:00.00]Brand new...'}

        with patch("apps.musica.utils.lyrics_provider.fetch_lrclib", return_value=new_result):
            result = get_lyrics("Old Song", "Old Artist", force_refresh=True)

        self.assertTrue(result["success"])
        self.assertFalse(result["cached"])
        self.assertIn("Brand new lyrics", result["lyrics"])

        saved = Cancion.objects.get(titulo__iexact="Old Song")
        self.assertEqual(saved.letra, "Brand new lyrics!")

    # ── Google fallback when both APIs fail ───────────────────────────────

    def test_google_fallback_when_apis_fail(self):
        """Both APIs return None → success=False, fallback_url provided."""
        with patch("apps.musica.utils.lyrics_provider.fetch_lrclib", return_value=None), \
             patch("apps.musica.utils.lyrics_provider.fetch_lyrics_ovh", return_value=None):

            result = get_lyrics("Unknown XYZ 12345", "Nobody")

        self.assertFalse(result["success"])
        self.assertEqual(result["source"], "google_fallback")
        self.assertEqual(result["status"], "not_found")
        self.assertIn("google.com/search", result["fallback_url"])
        self.assertIn("lyrics", result["fallback_url"])


# ---------------------------------------------------------------------------
# Endpoint tests
# ---------------------------------------------------------------------------

class LyricsEndpointTest(TestCase):

    def test_endpoint_requires_titulo(self):
        url = reverse('obtener_lyric')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_endpoint_cache_hit(self):
        Cancion.objects.create(titulo="Hola", artista="Manu Chao", letra="Hola, hola...")
        url = reverse('obtener_lyric')
        response = self.client.get(url, {'titulo': 'Hola', 'artista': 'Manu Chao'})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['source'], 'cache')

    def test_endpoint_force_refresh(self):
        Cancion.objects.create(titulo="Test Song", artista="Test Artist", letra="Old lyrics")
        new_result = {'lyrics': 'New lyrics!', 'synced': ''}
        with patch("apps.musica.utils.lyrics_provider.fetch_lrclib", return_value=new_result):
            url = reverse('obtener_lyric')
            response = self.client.get(url, {'titulo': 'Test Song', 'artista': 'Test Artist', 'refresh': '1'})
        data = response.json()
        self.assertTrue(data['success'])
        self.assertFalse(data['cached'])
        self.assertIn("New lyrics", data['lyrics'])

    def test_endpoint_not_found_returns_fallback_url(self):
        with patch("apps.musica.utils.lyrics_provider.fetch_lrclib", return_value=None), \
             patch("apps.musica.utils.lyrics_provider.fetch_lyrics_ovh", return_value=None):
            url = reverse('obtener_lyric')
            response = self.client.get(url, {'titulo': 'Totally Unknown Song XYZ'})
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['status'], 'not_found')
        self.assertIsNotNone(data['fallback_url'])


# ---------------------------------------------------------------------------
# Provider unit tests
# ---------------------------------------------------------------------------

class LyricsProviderUnitTest(TestCase):

    def test_build_google_fallback_encodes_properly(self):
        url = build_google_fallback("Bohemian Rhapsody", "Queen")
        self.assertIn("Bohemian+Rhapsody", url)
        self.assertIn("Queen", url)
        self.assertIn("lyrics", url)

    def test_build_google_fallback_special_chars(self):
        url = build_google_fallback("Shake It Off 🎵", "Taylor Swift")
        self.assertIn("google.com/search", url)
        # Should not raise on emojis or spaces

    @patch("apps.musica.utils.lyrics_provider.requests.get")
    def test_fetch_lrclib_timeout_returns_none(self, mock_get):
        import requests as req
        mock_get.side_effect = req.exceptions.Timeout
        result = fetch_lrclib("Any Song")
        self.assertIsNone(result)

    @patch("apps.musica.utils.lyrics_provider.requests.get")
    def test_fetch_lyrics_ovh_timeout_returns_none(self, mock_get):
        import requests as req
        mock_get.side_effect = req.exceptions.Timeout
        result = fetch_lyrics_ovh("Any Song", "Any Artist")
        self.assertIsNone(result)
