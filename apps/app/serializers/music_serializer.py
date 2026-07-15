"""
Music serializers.
"""

from rest_framework import serializers
from ..models import Cancion, Playlist


class SongSerializer(serializers.ModelSerializer):
    """Serializer for Song model."""
    
    class Meta:
        model = Cancion
        fields = ['id', 'titulo', 'artista', 'url', 'duracion', 'fecha_agregada']
        read_only_fields = ['id', 'fecha_agregada']


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer for Playlist model."""
    
    songs = SongSerializer(many=True, read_only=True)
    song_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['id', 'nombre', 'descripcion', 'songs', 'song_count', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_actualizacion']
    
    def get_song_count(self, obj):
        return obj.canciones.count()
