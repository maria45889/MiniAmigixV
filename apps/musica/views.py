from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .utils.lyrics_provider import get_lyrics
from .utils.youtube_captions_provider import fetch_youtube_captions



@require_GET
def youtube_captions(request):
    """GET /music/youtube_captions/?video_id=...

    Response:
    {
      "success": bool,
      "synced": str | null,        # LRC-like with timestamps
      "lyricsFallback": str | null,
      "status": "ok" | "not_found"
    }
    """
    video_id = (request.GET.get('video_id') or '').strip()
    if not video_id:
        return JsonResponse({
            'success': False,
            'synced': None,
            'lyricsFallback': None,
            'status': 'not_found',
        }, status=400)

    # Optional: language not wired from frontend yet
    result = fetch_youtube_captions(video_id, lang=None)
    if not result:
        return JsonResponse({
            'success': False,
            'synced': None,
            'lyricsFallback': None,
            'status': 'not_found',
        })

    return JsonResponse({
        'success': True,
        'synced': result.get('synced') or '',
        'lyricsFallback': result.get('lyricsFallback') or '',
        'status': 'ok',
    })


@require_GET
def obtener_letra(request):

    """
    GET /music/lyrics/?titulo=...&artista=...&refresh=1

    Response schema (always):
    {
        "success": bool,
        "lyrics": str | null,
        "synced": str | null,
        "cached": bool,
        "source": "cache" | "api_primary" | "api_fallback" | "google_fallback",
        "status": "ok" | "not_found",
        "fallback_url": str | null
    }
    """
    titulo = request.GET.get('titulo', '').strip()
    artista = request.GET.get('artista', '').strip()
    force_refresh = request.GET.get('refresh', '0') == '1'

    if not titulo:
        return JsonResponse({
            "success": False,
            "lyrics": None,
            "synced": None,
            "cached": False,
            "source": "none",
            "status": "not_found",
            "fallback_url": None,
        }, status=400)

    result = get_lyrics(titulo, artista, force_refresh=force_refresh)
    return JsonResponse(result)
