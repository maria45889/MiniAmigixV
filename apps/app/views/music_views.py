"""
Music views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.app.services import MusicService
from apps.app.selectors import MusicSelector
from apps.app.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from apps.app.utils import JsonResponseHelper, LogHelper
import logging

logger = logging.getLogger(__name__)


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


@require_http_methods(["POST"])
@csrf_exempt
def add_song_api(request):
    """Add a song to the music library."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        youtube_id = data.get('youtube_id')
        titulo = data.get('titulo')
        artista = data.get('artista')
        
        song, error = MusicService.add_song(request.user, youtube_id, titulo, artista)
        
        if error:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True, 'song_id': song.id})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al agregar canción: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def stream_audio_api(request, youtube_id):
    """Stream audio from YouTube."""
    # Placeholder for streaming functionality
    return JsonResponse({'error': 'Función no implementada'}, status=501)


@require_http_methods(["POST"])
@csrf_exempt
def update_theme_api(request):
    """Update user theme preference."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        theme = data.get('theme')
        
        from apps.app.services import UserService
        success, error = UserService.update_theme(request.user, theme)
        
        if not success:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al actualizar tema: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def update_language_api(request):
    """Update user language preference."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        idioma = data.get('idioma')
        
        from apps.app.services import UserService
        success, error = UserService.update_language(request.user, idioma)
        
        if not success:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al actualizar idioma: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def search_lyrics_api(request):
    """Search for song lyrics."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        query = data.get('query')
        
        # Placeholder for lyrics search
        return JsonResponse({'error': 'Función no implementada'}, status=501)
    except Exception as e:
        LogHelper.log_error(logger, f"Error al buscar letras: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_lyrics_api(request, song_id):
    """Get lyrics for a specific song."""
    # Placeholder for getting lyrics
    return JsonResponse({'error': 'Función no implementada'}, status=501)


@require_http_methods(["POST"])
@csrf_exempt
def save_lyrics_api(request, song_id):
    """Save lyrics for a specific song."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        lyrics = data.get('lyrics')
        
        # Placeholder for saving lyrics
        return JsonResponse({'error': 'Función no implementada'}, status=501)
    except Exception as e:
        LogHelper.log_error(logger, f"Error al guardar letras: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def netease_lyrics_api(request):
    """Get lyrics from Netease API."""
    # Placeholder for Netease lyrics
    return JsonResponse({'error': 'Función no implementada'}, status=501)


@require_http_methods(["POST"])
@csrf_exempt
def download_media_api(request):
    """Download media."""
    # Placeholder for download functionality
    return JsonResponse({'error': 'Función no implementada'}, status=501)


@require_http_methods(["POST"])
@csrf_exempt
def delete_chat_api(request, chat_id):
    """Delete a chat conversation."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        from apps.app.services import ChatService
        success, error = ChatService.delete_conversation(chat_id, request.user)
        
        if not success:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al eliminar chat: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def delete_song_api(request, song_id):
    """Delete a song from the library."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        success, error = MusicService.delete_song(song_id, request.user)
        
        if not success:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al eliminar canción: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def edit_song_api(request, song_id):
    """Edit a song in the library."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        titulo = data.get('titulo')
        artista = data.get('artista')
        
        success, error = MusicService.edit_song(song_id, request.user, titulo, artista)
        
        if not success:
            return JsonResponse({'error': error}, status=400)
        
        return JsonResponse({'success': True})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al editar canción: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
