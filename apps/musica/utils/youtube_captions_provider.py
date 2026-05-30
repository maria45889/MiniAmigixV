import logging
import re
from urllib.parse import quote_plus

import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10  # seconds


def _extract_video_id(video_url_or_id: str) -> str:
    if not video_url_or_id:
        return ""
    s = str(video_url_or_id).strip()

    if re.fullmatch(r"[A-Za-z0-9_-]{6,}", s):
        return s

    patterns = [
        r"v=([A-Za-z0-9_-]{6,})",
        r"youtu\\.be/([A-Za-z0-9_-]{6,})",
        r"/shorts/([A-Za-z0-9_-]{6,})",
    ]
    for pat in patterns:
        m = re.search(pat, s)
        if m:
            return m.group(1)

    return ""


def _build_timedtext_url(video_id: str, lang: str | None = None) -> str:
    base = "https://www.youtube.com/api/timedtext"
    params: dict[str, str] = {"v": video_id}
    if lang:
        params["lang"] = lang
    qs = "&".join([f"{k}={quote_plus(v)}" for k, v in params.items()])
    return f"{base}?{qs}"


def _xml_entity_unescape(txt: str) -> str:
    """Minimal XML entity unescape without complex quote escaping."""
    if not txt:
        return txt

    # Use single-quoted literals to avoid quote-double edge cases in this environment.
    txt = txt.replace('&amp;', '&')
    txt = txt.replace('<', '<')
    txt = txt.replace('>', '>')
    txt = txt.replace('&#39;', "'")
    # For ", just remove it back to a double-quote.
    # (Construct the double quote via chr(34) to avoid writing it literally inside quotes.)
    txt = txt.replace('"', chr(34))
    return txt


def _parse_timedtext_xml(xml_text: str) -> list[dict]:
    entries: list[dict] = []
    if not xml_text:
        return entries

    # Extract each <text ...>...</text> with start seconds.
    # Note: We keep this regex simple and rely on flags=DOTALL.
    pattern = r"<text\\s+[^>]*start=\\\"(?P<start>[^\\\"]+)\\\"[^>]*>(?P<txt>.*?)</text>"

    for m in re.finditer(pattern, xml_text, flags=re.DOTALL):
        start = m.group('start')
        txt = m.group('txt')

        try:
            ts = float(start)
        except Exception:
            continue

        # Remove inner tags (e.g., <font>, <i>, etc.)
        txt = re.sub(r"<[^>]+>", '', txt)
        txt = _xml_entity_unescape(txt)
        txt = re.sub(r"\\s+", ' ', txt).strip()

        if txt:
            entries.append({'timestamp': ts, 'text': txt})

    return entries


def _to_lrc(entries: list[dict]) -> str:
    def fmt(ts: float) -> str:
        if ts < 0:
            ts = 0
        minutes = int(ts // 60)
        seconds_float = ts - minutes * 60
        seconds_whole = int(seconds_float)
        ms = int(round((seconds_float - seconds_whole) * 1000))
        if ms == 1000:
            minutes += 1
            ms = 0
        return f"{minutes:02d}:{seconds_whole:02d}.{ms:03d}"

    lines: list[str] = []
    for e in entries:
        ts = e.get('timestamp')
        text = e.get('text')
        if ts is None or not text:
            continue
        lines.append(f"[{fmt(float(ts))}] {text}")

    return '\n'.join(lines).strip()


def fetch_youtube_captions(video_id: str, lang: str | None = None) -> dict | None:
    resolved_id = _extract_video_id(video_id)
    if not resolved_id:
        return None

    try:
        url = _build_timedtext_url(resolved_id, lang=lang)
        resp = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={'User-Agent': 'MiniAmigixV/1.0 (captions-fetcher)'},
        )
        if not resp.ok:
            return None

        entries = _parse_timedtext_xml(resp.text)
        if not entries:
            return None

        synced = _to_lrc(entries)
        plain = '\n'.join([e.get('text', '') for e in entries if e.get('text')]).strip()

        if not synced.strip() and not plain.strip():
            return None

        return {'synced': synced, 'lyricsFallback': plain}

    except requests.RequestException as exc:
        logger.warning('youtube captions fetch error: %s', exc)
        return None

