"""
Music service.

Business logic for music operations.
"""

import logging
from typing import Optional, Tuple

from ..selectors.music_selector import MusicSelector
from ..validators import MusicValidator
from ..exceptions import ValidationException, NotFoundException
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class MusicService:
    """Service for music-related operations."""
    
    @staticmethod
    def create_playlist(user, name: str, description: str = '') -> Tuple[Optional[object], Optional[str]]:
        """Create a new playlist."""
        try:
            MusicValidator.validate_playlist_name(name)
            MusicValidator.validate_playlist_description(description)
        except ValidationException as e:
            return None, e.message
        
        if not name:
            return None, "El nombre es requerido"
        
        try:
            playlist = MusicSelector.create_playlist(user, name, description)
            LogHelper.log_info(logger, f"Playlist creada: {name}")
            return playlist, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al crear playlist: {str(e)}", exc_info=True)
            return None, str(e)
    
    @staticmethod
    def add_song_to_playlist(playlist_id: int, song_id: int, user) -> Tuple[bool, Optional[str]]:
        """Add a song to a playlist."""
        try:
            playlist = MusicSelector.get_playlist_by_id(playlist_id, user)
            cancion = MusicSelector.get_song_by_id(song_id, user)
            playlist.canciones.add(cancion)
            playlist.save()
            LogHelper.log_info(logger, f"Canción agregada a playlist: {playlist_id}")
            return True, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al agregar canción a playlist: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    def toggle_favorite(song_id: int, user) -> Tuple[bool, str]:
        """Toggle favorite status for a song."""
        try:
            cancion = MusicSelector.get_song_by_id(song_id, user)
            favorito, created = MusicSelector.get_or_create_favorite(user, cancion)
            
            if not created:
                favorito.delete()
                LogHelper.log_info(logger, f"Favorito eliminado: {song_id}")
                return False, "Favorito eliminado"
            
            LogHelper.log_info(logger, f"Favorito agregado: {song_id}")
            return True, "Agregado a favoritos"
        except Exception as e:
            LogHelper.log_error(logger, f"Error al toggle favorito: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    def add_song(user, youtube_id: str = None, titulo: str = None, artista: str = None, audio_file = None) -> Tuple[Optional[object], Optional[str]]:
        """Add a new song to the library."""
        try:
            from ..models import Cancion
            
            if not titulo:
                return None, "El título es requerido"
            
            if not youtube_id and not audio_file:
                return None, "Se requiere ID de YouTube o archivo de audio"
            
            # Crear la canción
            cancion = Cancion.objects.create(
                usuario=user,
                nombre=titulo,
                artista=artista or '',
                youtube_id=youtube_id or '',
                youtube_url=f'https://www.youtube.com/watch?v={youtube_id}' if youtube_id else '',
                audio_file=audio_file
            )
            
            LogHelper.log_info(logger, f"Canción agregada: {titulo}")
            return cancion, None
            
        except Exception as e:
            LogHelper.log_error(logger, f"Error al agregar canción: {str(e)}", exc_info=True)
            return None, str(e)
    
    @staticmethod
    def edit_song(song_id: int, user, titulo: str = None, artista: str = None) -> Tuple[bool, Optional[str]]:
        """Edit an existing song."""
        try:
            cancion = MusicSelector.get_song_by_id(song_id, user)
            
            if titulo:
                cancion.nombre = titulo
            if artista is not None:
                cancion.artista = artista
            
            cancion.save()
            LogHelper.log_info(logger, f"Canción editada: {song_id}")
            return True, None
            
        except Exception as e:
            LogHelper.log_error(logger, f"Error al editar canción: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    def delete_song(song_id: int, user) -> Tuple[bool, Optional[str]]:
        """Delete a song from the library."""
        try:
            cancion = MusicSelector.get_song_by_id(song_id, user)
            cancion.delete()
            LogHelper.log_info(logger, f"Canción eliminada: {song_id}")
            return True, None
            
        except Exception as e:
            LogHelper.log_error(logger, f"Error al eliminar canción: {str(e)}", exc_info=True)
            return False, str(e)
