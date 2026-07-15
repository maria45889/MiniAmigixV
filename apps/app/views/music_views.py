"""
Music views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.app.services import MusicService
from apps.app.selectors import MusicSelector
from apps.app.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from apps.app.utils import JsonResponseHelper, LogHelper


@login_required
def musica(request):
    """Render music page."""
    canciones = MusicSelector.get_recent_songs(request.user, 20)
    playlists = MusicSelector.get_playlists(request.user)
    favoritos = MusicSelector.get_favorites(request.user)
    
    return render(request, 'musica.html', {
        'canciones': canciones,
        'playlists': playlists,
        'favoritos': favoritos
    })


@require_http_methods(["POST"])
def crear_playlist(request):
    """Create a new playlist."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        
        playlist, error = MusicService.create_playlist(request.user, nombre, descripcion)
        
        if error:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True, 'playlist_id': playlist.id})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al crear playlist: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def agregar_a_playlist(request):
    """Add song to playlist."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        playlist_id = data.get('playlist_id')
        cancion_id = data.get('cancion_id')
        
        success, error = MusicService.add_song_to_playlist(playlist_id, cancion_id, request.user)
        
        if not success:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al agregar a playlist: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def toggle_favorito(request):
    """Toggle favorite status for a song."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        cancion_id = data.get('cancion_id')
        
        is_favorite, message = MusicService.toggle_favorite(cancion_id, request.user)
        
        return JsonResponse({'success': True, 'is_favorite': is_favorite, 'message': message})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al toggle favorito: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
