"""
Music selector.

Database queries for music operations.
"""

from ..models import Cancion, Playlist, Favorite


class MusicSelector:
    """Selector for music-related queries."""
    
    @staticmethod
    def get_recent_songs(user, limit: int = 20):
        """Get recent songs for user."""
        return Cancion.objects.filter(usuario=user).order_by('-fecha_agregada')[:limit]
    
    @staticmethod
    def get_playlists(user):
        """Get all playlists for user."""
        return Playlist.objects.filter(usuario=user).order_by('-fecha_actualizacion')
    
    @staticmethod
    def get_playlist_by_id(playlist_id: int, user):
        """Get playlist by ID and user."""
        return Playlist.objects.get(id=playlist_id, usuario=user)
    
    @staticmethod
    def get_song_by_id(song_id: int, user):
        """Get song by ID and user."""
        return Cancion.objects.get(id=song_id, usuario=user)
    
    @staticmethod
    def create_playlist(user, name: str, description: str = ''):
        """Create a new playlist."""
        return Playlist.objects.create(
            usuario=user,
            nombre=name,
            descripcion=description
        )
    
    @staticmethod
    def get_favorites(user):
        """Get favorite songs for user."""
        favoritos_canciones = Favorite.objects.filter(usuario=user).select_related('cancion')
        return [fav.cancion for fav in favoritos_canciones]
    
    @staticmethod
    def get_or_create_favorite(user, song):
        """Get or create favorite for user and song."""
        return Favorite.objects.get_or_create(usuario=user, cancion=song)
    
    @staticmethod
    def count_songs(user):
        """Count songs for user."""
        return Cancion.objects.filter(usuario=user).count()
