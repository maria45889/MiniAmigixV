"""
lyrics_provider.py
==================
Modular service that retrieves song lyrics through a layered strategy:

    1. DB cache      → instant, no network
    2. LRCLIB        → primary API, supports LRC synced lyrics
    3. Lyrics.ovh    → secondary fallback
    4. Google search → last resort, returns a search URL

Public API:
    get_lyrics(titulo, artista, force_refresh=False) -> dict
"""

import logging
import re
from urllib.parse import quote_plus

import requests

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
LRCLIB_SEARCH = "https://lrclib.net/api/search"
LYRICS_OVH = "https://api.lyrics.ovh/v1"
GOOGLE_SEARCH = "https://www.google.com/search?q="
REQUEST_TIMEOUT = 5  # seconds


# -------------------------------------------------------------------
# Internal helpers
# -------------------------------------------------------------------

def _clean_title(raw: str) -> str:
    """Strip parentheses, brackets, double-slashes and extra whitespace."""
    cleaned = re.sub(r'\(.*?\)', '', raw)
    cleaned = re.sub(r'\[.*?\]', '', cleaned)
    cleaned = re.sub(r'//+', ' ', cleaned)
    return cleaned.strip()


def _split_artist_title(raw: str):
    """
    Try to extract (artist, title) from patterns like 'Artist - Title' or 'Artist | Title'.
    Returns (artist, title) or (None, raw) if no separator found.
    """
    for sep in (' - ', ' – ', ' — ', ' | '):
        if sep in raw:
            parts = raw.split(sep, 1)
            return parts[0].strip(), parts[1].strip()
    return None, raw.strip()


# -------------------------------------------------------------------
# Layer 1 – DB cache
# -------------------------------------------------------------------

def get_cached_lyrics(titulo: str, artista: str):
    """
    Returns a Cancion instance if it exists in DB and has lyrics, else None.
    Imported lazily to avoid circular imports at module load time.
    """
    from apps.musica.models import Cancion  # lazy import
    cancion = Cancion.objects.filter(
        titulo__iexact=titulo,
        artista__iexact=artista,
    ).first()
    if cancion and cancion.tiene_letra():
        return cancion
    return None


# -------------------------------------------------------------------
# Layer 2 – LRCLIB (primary API)
# -------------------------------------------------------------------

def fetch_lrclib(titulo: str, artista: str = '') -> dict | None:
    """
    Query LRCLIB. Returns {'lyrics': str, 'synced': str|None} or None.
    Prefers syncedLyrics (LRC format) when available.
    """
    query = _clean_title(f"{artista} {titulo}" if artista else titulo)
    try:
        resp = requests.get(
            LRCLIB_SEARCH,
            params={'q': query},
            timeout=REQUEST_TIMEOUT,
            headers={'User-Agent': 'MiniAmigixV/1.0 (lyrics-fetcher)'},
        )
        if not resp.ok:
            return None
        results = resp.json()
        if not results:
            return None
        hit = results[0]
        synced = hit.get('syncedLyrics') or ''
        plain = hit.get('plainLyrics') or ''
        lyrics = synced or plain
        if not lyrics.strip():
            return None
        return {'lyrics': plain.strip(), 'synced': synced.strip()}
    except requests.RequestException as exc:
        logger.warning("LRCLIB error: %s", exc)
        return None


# -------------------------------------------------------------------
# Layer 3 – Lyrics.ovh (secondary fallback)
# -------------------------------------------------------------------

def fetch_lyrics_ovh(titulo: str, artista: str = '') -> dict | None:
    """
    Query Lyrics.ovh. Requires artist and title.
    Returns {'lyrics': str, 'synced': ''} or None.
    """
    if not artista:
        # Try to extract from title
        extracted_artist, extracted_title = _split_artist_title(titulo)
        if not extracted_artist:
            return None
        artista = extracted_artist
        titulo = extracted_title

    try:
        url = f"{LYRICS_OVH}/{quote_plus(artista)}/{quote_plus(titulo)}"
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        if not resp.ok:
            return None
        data = resp.json()
        lyrics = data.get('lyrics', '').strip()
        if not lyrics:
            return None
        return {'lyrics': lyrics, 'synced': ''}
    except requests.RequestException as exc:
        logger.warning("Lyrics.ovh error: %s", exc)
        return None


# -------------------------------------------------------------------
# Layer 4 – Google Search fallback
# -------------------------------------------------------------------

def build_google_fallback(titulo: str, artista: str = '') -> str:
    """
    Returns a Google search URL for the song lyrics.
    URL-encodes properly to handle spaces, emojis, special chars.
    """
    query = f"{artista} {titulo} lyrics".strip() if artista else f"{titulo} lyrics"
    return f"{GOOGLE_SEARCH}{quote_plus(query)}"


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def get_lyrics(titulo: str, artista: str = '', force_refresh: bool = False) -> dict:
    """
    Main entry point. Returns a standardised response dict:

    {
        "success": bool,
        "lyrics":  str | None,
        "synced":  str | None,
        "cached":  bool,
        "source":  "cache" | "api_primary" | "api_fallback" | "google_fallback",
        "status":  "ok" | "not_found",
        "fallback_url": str | None,
    }
    """
    from apps.musica.models import Cancion  # lazy import

    titulo = (titulo or '').strip()
    artista = (artista or '').strip()

    if not titulo:
        return _not_found(titulo, artista)

    # ── Layer 1: DB cache (skip if force_refresh) ────────────────
    if not force_refresh:
        cancion = get_cached_lyrics(titulo, artista)
        if cancion:
            return {
                "success": True,
                "lyrics": cancion.letra,
                "synced": cancion.synced_lyrics or '',
                "cached": True,
                "source": "cache",
                "status": "ok",
                "fallback_url": None,
            }

    # ── Layer 2: LRCLIB ─────────────────────────────────────────
    result = fetch_lrclib(titulo, artista)
    source = "api_primary"

    # ── Layer 3: Lyrics.ovh ──────────────────────────────────────
    if not result:
        result = fetch_lyrics_ovh(titulo, artista)
        source = "api_fallback"

    # ── Persist to DB ────────────────────────────────────────────
    if result:
        cancion, _ = Cancion.objects.get_or_create(
            titulo__iexact=titulo,
            artista__iexact=artista,
            defaults={'titulo': titulo, 'artista': artista},
        )
        cancion.letra = result.get('lyrics', '')
        cancion.synced_lyrics = result.get('synced', '')
        cancion.save(update_fields=['letra', 'synced_lyrics', 'actualizado_en'])

        return {
            "success": True,
            "lyrics": cancion.letra,
            "synced": cancion.synced_lyrics or '',
            "cached": False,
            "source": source,
            "status": "ok",
            "fallback_url": None,
        }

    # ── Layer 4: Google fallback ─────────────────────────────────
    return _not_found(titulo, artista)


def _not_found(titulo: str, artista: str) -> dict:
    return {
        "success": False,
        "lyrics": None,
        "synced": None,
        "cached": False,
        "source": "google_fallback",
        "status": "not_found",
        "fallback_url": build_google_fallback(titulo, artista),
    }
