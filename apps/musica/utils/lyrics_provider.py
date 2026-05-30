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

    # Generate multiple artist/title attempts using heuristics
    attempts = _generate_artist_title_attempts(titulo, artista)
    
    # If no attempts were generated, fall back to original inputs
    if not attempts:
        attempts = [(artista, titulo)]

    # Try each attempt in order
    for attempt_artista, attempt_titulo in attempts:
        # Skip if both are empty
        if not attempt_artista and not attempt_titulo:
            continue
            
        # ── Layer 1: DB cache (skip if force_refresh) ────────────────
        if not force_refresh:
            cancion = get_cached_lyrics(attempt_titulo, attempt_artista)
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
        result = fetch_lrclib(attempt_titulo, attempt_artista)
        source = "api_primary"

        # ── Layer 3: Lyrics.ovh ──────────────────────────────────────
        if not result:
            result = fetch_lyrics_ovh(attempt_titulo, attempt_artista)
            source = "api_fallback"

        # ── Persist to DB ────────────────────────────────────────────
        if result:
            cancion, _ = Cancion.objects.get_or_create(
                titulo__iexact=attempt_titulo,
                artista__iexact=attempt_artista,
                defaults={'titulo': attempt_titulo, 'artista': attempt_artista},
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

    # If all attempts failed, return not found with the original inputs
    return _not_found(titulo, artista)


def _normalize_search_string(raw: str) -> str:
    """
    Normalize a search string by removing common YouTube noise and decorative symbols.
    
    Removes:
    - Parentheses and brackets content
    - Words like Letra, Lyrics, Official Video, Audio Oficial, HD
    - Decorative symbols like ♡ ♥ ♪ ✨ | •
    - Extra whitespace
    """
    if not raw:
        return ""
    
    # Start with the raw string
    cleaned = str(raw)
    
    # Remove content inside parentheses and brackets
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)
    cleaned = re.sub(r'\[[^\]]*\]', '', cleaned)
    
    # Remove common noise words (case insensitive)
    noise_words = [
        r'\bletra\b', r'\blyrics\b', r'\bofficial\s+video\b', 
        r'\baudio\s+oficial\b', r'\bhd\b', r'\b4k\b'
    ]
    for pattern in noise_words:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Remove decorative symbols
    cleaned = re.sub(r'[♡♥♪✨|•]', '', cleaned)
    
    # Clean up extra spaces and normalize
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single
    cleaned = cleaned.strip()
    
    return cleaned


def _generate_artist_title_attempts(titulo: str, artista: str = '') -> list:
    """
    Generate multiple (artist, title) attempts based on heuristics for dirty YouTube titles.
    
    Returns a list of (artist, title) tuples to try in order of preference.
    """
    attempts = []
    
    # Clean inputs
    titulo_clean = titulo.strip()
    artista_clean = artista.strip() if artista else ''
    
    # If we already have artist and title, try them first
    if artista_clean and titulo_clean:
        attempts.append((artista_clean, titulo_clean))
    
    # Work with the title if we don't have a separate artist
    if not artista_clean:
        # Normalize the title first
        normalized = _normalize_search_string(titulo_clean)
        
        # Attempt 1: Try splitting by common separators (including //)
        separators = ['//', ' - ', ' – ', ' — ', ' | ', '/', '\\\\']
        for sep in separators:
            if sep in normalized:
                parts = normalized.split(sep, 1)
                if len(parts) == 2:
                    artist_attempt = parts[0].strip()
                    title_attempt = parts[1].strip()
                    # Only add if both parts are meaningful
                    if artist_attempt and title_attempt and len(artist_attempt) > 1 and len(title_attempt) > 1:
                        attempts.append((artist_attempt, title_attempt))
                break  # Only use the first matching separator
        
        # Attempt 2: Try the normalized string as title with empty artist
        if normalized:
            attempts.append(("", normalized))
        
        # Attempt 3: Try original title as title with empty artist
        if titulo_clean and titulo_clean != normalized:
            attempts.append(("", titulo_clean))
        
        # Attempt 4: If we have multiple // separators, try first and middle parts
        if '//' in titulo_clean:
            parts = [p.strip() for p in titulo_clean.split('//') if p.strip()]
            if len(parts) >= 3:
                # Try first as artist, second as title
                attempts.append((parts[0], parts[1]))
                # Try first as artist, rest joined as title
                if len(parts) > 2:
                    attempts.append((parts[0], ' '.join(parts[1:])))
            elif len(parts) == 2:
                # Try both parts as artist/title and title/artist
                attempts.append((parts[0], parts[1]))
                attempts.append((parts[1], parts[0]))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_attempts = []
    for attempt in attempts:
        if attempt not in seen:
            seen.add(attempt)
            unique_attempts.append(attempt)
    
    return unique_attempts


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
