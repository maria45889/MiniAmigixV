from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .utils.lyrics_provider import get_lyrics


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
