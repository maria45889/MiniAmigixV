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
        from django.core.files.uploadedfile import InMemoryUploadedFile
        
        # Handle both JSON and FormData
        content_type = request.content_type
        
        if 'multipart/form-data' in content_type:
            # FormData with file upload
            titulo = request.POST.get('titulo')
            artista = request.POST.get('artista')
            youtube_id = request.POST.get('youtube_id')
            audio_file = request.FILES.get('audio_file')
            
            song, error = MusicService.add_song(request.user, youtube_id, titulo, artista, audio_file)
        else:
            # JSON data
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
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import yt_dlp
        import tempfile
        import os
        from django.http import FileResponse, HttpResponse
        
        logger.info(f"Extrayendo audio para YouTube ID: {youtube_id}")
        
        # Configure yt-dlp to extract audio
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
            'outtmpl': os.path.join(tempfile.gettempdir(), f'{youtube_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'nocheckformats': True,
            'timeout': 60,
            # Add options to avoid 403 errors
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'nocheckcertificate': True,
            'extract_flat': False,
        }
        
        # Extract audio using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = f'https://www.youtube.com/watch?v={youtube_id}'
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Verify file exists
            if not os.path.exists(filename):
                logger.error(f"Archivo no encontrado después de extracción: {filename}")
                return JsonResponse({'error': 'Error: archivo no encontrado después de extracción'}, status=500)
            
            # Get the actual file extension
            actual_ext = os.path.splitext(filename)[1][1:]  # Remove the dot
            
            # Determine content type based on actual extension
            if actual_ext in ['m4a', 'aac']:
                content_type = 'audio/mp4'
            elif actual_ext == 'webm':
                content_type = 'audio/webm'
            elif actual_ext == 'mp3':
                content_type = 'audio/mpeg'
            else:
                content_type = 'application/octet-stream'
            
            logger.info(f"Enviando audio: {filename}, tipo: {content_type}")
            
            # Read file content and return as response
            with open(filename, 'rb') as f:
                audio_content = f.read()
            
            # Schedule file deletion after response is sent
            import threading
            def delete_file():
                try:
                    import time
                    time.sleep(5)  # Wait longer for streaming
                    if os.path.exists(filename):
                        os.remove(filename)
                        logger.info(f"Archivo temporal eliminado: {filename}")
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo temporal: {str(e)}")
            
            thread = threading.Thread(target=delete_file)
            thread.start()
            
            # Return audio content as response
            response = HttpResponse(audio_content, content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{youtube_id}.{actual_ext}"'
            return response
                
    except Exception as e:
        logger.error(f"Error al extraer audio: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_audio_stream_api(request):
    """Get audio stream URL for YouTube video (returns JSON)."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import yt_dlp
        youtube_id = request.GET.get('youtube_id')
        if not youtube_id:
            return JsonResponse({'error': 'youtube_id es requerido'}, status=400)
        
        logger.info(f"Obteniendo stream de audio para YouTube ID: {youtube_id}")
        
        # Configure yt-dlp to get audio stream URL without downloading
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = f'https://www.youtube.com/watch?v={youtube_id}'
            info = ydl.extract_info(url, download=False)
            
            # Find the best audio format
            audio_url = None
            for format in info.get('formats', []):
                if format.get('acodec') != 'none' and format.get('vcodec') == 'none':
                    audio_url = format.get('url')
                    break
            
            if not audio_url:
                # Fallback to first audio format
                for format in info.get('formats', []):
                    if format.get('acodec') != 'none':
                        audio_url = format.get('url')
                        break
            
            if audio_url:
                logger.info(f"Stream de audio obtenido: {audio_url[:100]}...")
                return JsonResponse({'audio_url': audio_url})
            else:
                logger.error("No se pudo encontrar stream de audio")
                return JsonResponse({'error': 'No se pudo encontrar stream de audio'}, status=404)
                
    except Exception as e:
        logger.error(f"Error al obtener stream de audio: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def search_and_play_audio_api(request):
    """Search for audio by song name and artist using yt-dlp."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import yt_dlp
        query = request.GET.get('query')
        if not query:
            return JsonResponse({'error': 'query es requerido'}, status=400)
        
        logger.info(f"Buscando audio para: {query}")
        
        # Configure yt-dlp to search and get audio stream
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': False,
            'default_search': 'ytsearch',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search for the song
            search_url = f'ytsearch1:{query}'
            info = ydl.extract_info(search_url, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                video_info = info['entries'][0]
                video_id = video_info.get('id')
                
                if video_id:
                    # Get the audio stream URL for this video
                    logger.info(f"Video encontrado: {video_id}, obteniendo stream de audio...")
                    
                    # Get audio stream URL
                    audio_url = None
                    for format in video_info.get('formats', []):
                        if format.get('acodec') != 'none' and format.get('vcodec') == 'none':
                            audio_url = format.get('url')
                            break
                    
                    if not audio_url:
                        # Fallback to first audio format
                        for format in video_info.get('formats', []):
                            if format.get('acodec') != 'none':
                                audio_url = format.get('url')
                                break
                    
                    if audio_url:
                        logger.info(f"Audio encontrado: {audio_url[:100]}...")
                        return JsonResponse({
                            'audio_url': audio_url,
                            'youtube_id': video_id,
                            'title': video_info.get('title')
                        })
            
            logger.error("No se encontraron resultados para la búsqueda")
            return JsonResponse({'error': 'No se encontraron resultados'}, status=404)
                
    except Exception as e:
        logger.error(f"Error al buscar audio: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


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
        
        # Search lyrics using LRCLIB API
        import requests
        response = requests.get(f'https://lrclib.net/api/search?q={query}', timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            if results and len(results) > 0:
                return JsonResponse({'success': True, 'results': results})
            else:
                return JsonResponse({'success': False, 'error': 'No se encontraron letras'})
        else:
            return JsonResponse({'error': 'Error al buscar letras'}, status=500)
    except Exception as e:
        LogHelper.log_error(logger, f"Error al buscar letras: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_lyrics_api(request, song_id):
    """Get lyrics for a specific song."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        from apps.app.models import Cancion
        cancion = Cancion.objects.get(id=song_id, usuario=request.user)
        
        return JsonResponse({
            'success': True,
            'letra': cancion.letra,
            'letra_sincronizada': cancion.letra_sincronizada
        })
    except Cancion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Canción no encontrada'}, status=404)
    except Exception as e:
        LogHelper.log_error(logger, f"Error al obtener letras: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def save_lyrics_api(request, song_id):
    """Save lyrics for a specific song."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        lyrics = data.get('letra')
        synced_lyrics = data.get('letra_sincronizada')
        
        from apps.app.models import Cancion
        cancion = Cancion.objects.get(id=song_id, usuario=request.user)
        
        if lyrics:
            cancion.letra = lyrics
        if synced_lyrics:
            cancion.letra_sincronizada = synced_lyrics
        
        cancion.save()
        
        return JsonResponse({'success': True})
    except Cancion.DoesNotExist:
        return JsonResponse({'error': 'Canción no encontrada'}, status=404)
    except Exception as e:
        LogHelper.log_error(logger, f"Error al guardar letras: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def netease_lyrics_api(request):
    """Get lyrics from Netease API."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body) if request.content_type == 'application/json' else {}
        song = request.GET.get('song', data.get('song', ''))
        artist = request.GET.get('artist', data.get('artist', ''))
        
        if not song or not artist:
            return JsonResponse({'error': 'song y artist son requeridos'}, status=400)
        
        # Search for lyrics using LRCLIB as fallback
        import requests
        from requests.exceptions import Timeout, RequestException
        query = f'{artist} {song}'
        
        try:
            response = requests.get(f'https://lrclib.net/api/search?q={query}', timeout=15)
        except Timeout:
            return JsonResponse({'success': False, 'error': 'Timeout al buscar letras. Intenta nuevamente.'})
        except RequestException as e:
            return JsonResponse({'success': False, 'error': f'Error de conexión: {str(e)}'})
        
        if response.status_code == 200:
            results = response.json()
            if results and len(results) > 0:
                # Prioritize synced lyrics
                synced_match = next((r for r in results if r.get('syncedLyrics')), None)
                if synced_match:
                    return JsonResponse({
                        'success': True,
                        'syncedLyrics': synced_match.get('syncedLyrics'),
                        'plainLyrics': synced_match.get('plainLyrics')
                    })
                else:
                    return JsonResponse({
                        'success': True,
                        'syncedLyrics': None,
                        'plainLyrics': results[0].get('plainLyrics')
                    })
        
        return JsonResponse({'success': False, 'error': 'No se encontraron letras'})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al obtener letras de Netease: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': 'Error interno del servidor'})


@require_http_methods(["GET", "POST"])
@csrf_exempt
def download_media_api(request):
    """Download media from YouTube."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        # Get URL and format from request
        if request.method == 'GET':
            url = request.GET.get('url')
            format_type = request.GET.get('format', 'mp3')
        else:
            import json
            data = json.loads(request.body)
            url = data.get('url')
            format_type = data.get('format', 'mp3')
        
        if not url:
            return JsonResponse({'error': 'URL es requerida'}, status=400)
        
        logger.info(f"Iniciando descarga: URL={url}, formato={format_type}")
        
        # Import yt-dlp
        import yt_dlp
        import tempfile
        import os
        from django.http import FileResponse
        import re
        
        # Clean URL to remove playlist parameters and extract single video
        # Extract video ID from URL
        video_id_match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
        if not video_id_match:
            return JsonResponse({'error': 'No se pudo extraer el ID del video de la URL'}, status=400)
        
        video_id = video_id_match.group(1)
        clean_url = f'https://www.youtube.com/watch?v={video_id}'
        
        logger.info(f"URL limpia: {clean_url}")
        
        # Configure yt-dlp to download without FFmpeg
        # Use a format that doesn't require conversion
        if format_type == 'mp3':
            # Download audio-only format that doesn't need conversion
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'nocheckformats': True,  # Skip format checks that might require FFmpeg
                'timeout': 60,  # Add timeout to prevent hanging
                # Add options to avoid 403 errors
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'referer': 'https://www.youtube.com/',
                'nocheckcertificate': True,
                'extract_flat': False,
            }
        else:  # mp4
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'nocheckformats': True,
                'timeout': 60,  # Add timeout to prevent hanging
                # Add options to avoid 403 errors
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'referer': 'https://www.youtube.com/',
                'nocheckcertificate': True,
                'extract_flat': False,
            }
        
        logger.info("Configuración yt-dlp lista, iniciando descarga...")
        
        # Download using yt-dlp
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_url, download=True)
                logger.info(f"Descarga completada: {info.get('title', 'unknown')}")
                
                filename = ydl.prepare_filename(info)
                
                # Verify file exists
                if not os.path.exists(filename):
                    logger.error(f"Archivo no encontrado después de descarga: {filename}")
                    return JsonResponse({'error': 'Error: archivo no encontrado después de descarga'}, status=500)
                
                # Get the actual file extension
                actual_ext = os.path.splitext(filename)[1][1:]  # Remove the dot
                
                # Get the title for the filename
                title = info.get('title', 'descarga')
                # Sanitize the title
                title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                if not title:
                    title = 'descarga'
                
                # Create a clean filename with actual extension
                clean_filename = f"{title}.{actual_ext}"
                
                # Determine content type based on actual extension
                if actual_ext in ['m4a', 'aac']:
                    content_type = 'audio/mp4'
                elif actual_ext == 'webm':
                    content_type = 'audio/webm' if format_type == 'mp3' else 'video/webm'
                elif actual_ext == 'mp3':
                    content_type = 'audio/mpeg'
                elif actual_ext == 'mp4':
                    content_type = 'video/mp4'
                else:
                    content_type = 'application/octet-stream'
                
                logger.info(f"Enviando archivo: {clean_filename}, tipo: {content_type}")
                
                # Open file without context manager to let Django handle closing
                f = open(filename, 'rb')
                response = FileResponse(f, content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{clean_filename}"'
                
                # Schedule file deletion after response is sent
                import threading
                def delete_file():
                    try:
                        # Wait a bit to ensure response is sent
                        import time
                        time.sleep(2)
                        if os.path.exists(filename):
                            os.remove(filename)
                            logger.info(f"Archivo temporal eliminado: {filename}")
                    except Exception as e:
                        logger.warning(f"No se pudo eliminar archivo temporal: {str(e)}")
                
                thread = threading.Thread(target=delete_file)
                thread.start()
                
                return response
                
        except Exception as download_error:
            error_msg = str(download_error)
            logger.error(f"Error en yt-dlp: {error_msg}")
            
            # Check for specific YouTube errors
            if '403' in error_msg or 'Forbidden' in error_msg:
                return JsonResponse({
                    'error': 'YouTube está bloqueando la descarga de este video. Intenta con otro video o usa el reproductor integrado.'
                }, status=403)
            elif 'video not found' in error_msg.lower() or 'not available' in error_msg.lower():
                return JsonResponse({
                    'error': 'Video no encontrado o no disponible en tu región.'
                }, status=404)
            else:
                return JsonResponse({
                    'error': f'Error al descargar: {error_msg}'
                }, status=500)
                
    except Exception as e:
        LogHelper.log_error(logger, f"Error al descargar media: {str(e)}", exc_info=True)
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
