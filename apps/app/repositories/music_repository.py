"""
Music repository.

Data access layer for music operations.
"""

from ..models import Cancion, Playlist, Favorite


class MusicRepository:
    """Repository for music data access."""
    
    @staticmethod
    def save_song(song):
        """Save song to database."""
        song.save()
        return song
    
    @staticmethod
    def delete_song(song_id: int, user):
        """Delete song."""
        song = Cancion.objects.get(id=song_id, usuario=user)
        song.delete()
    
    @staticmethod
    def save_playlist(playlist):
        """Save playlist to database."""
        playlist.save()
        return playlist
    
    @staticmethod
    def delete_playlist(playlist_id: int, user):
        """Delete playlist."""
        playlist = Playlist.objects.get(id=playlist_id, usuario=user)
        playlist.delete()
