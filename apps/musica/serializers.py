from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Song, Playlist, PlaylistSong, Favorite, ListeningHistory, MusicSettings


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'titulo', 'artista', 'album', 'duracion', 'youtube_url', 
                  'youtube_video_id', 'portada_url', 'letra', 'fecha_agregada']
        read_only_fields = ['fecha_agregada']


class SongCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['titulo', 'artista', 'album', 'duracion', 'youtube_url', 'portada_url', 'letra']
    
    def create(self, validated_data):
        youtube_url = validated_data.get('youtube_url', '')
        youtube_video_id = None
        
        # Extraer video ID de YouTube si existe
        if youtube_url:
            if 'youtube.com/watch?v=' in youtube_url:
                youtube_video_id = youtube_url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in youtube_url:
                youtube_video_id = youtube_url.split('youtu.be/')[1].split('?')[0]
        
        validated_data['youtube_video_id'] = youtube_video_id
        return Song.objects.create(**validated_data)


class PlaylistSongSerializer(serializers.ModelSerializer):
    cancion = SongSerializer(read_only=True)
    cancion_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PlaylistSong
        fields = ['id', 'playlist', 'cancion', 'cancion_id', 'orden', 'fecha_agregada']
        read_only_fields = ['fecha_agregada']


class PlaylistSerializer(serializers.ModelSerializer):
    canciones = PlaylistSongSerializer(many=True, read_only=True, source='playlistsong_set')
    total_canciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['id', 'nombre', 'descripcion', 'usuario', 'canciones', 'total_canciones',
                  'fecha_creacion', 'fecha_actualizacion', 'es_publica']
        read_only_fields = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_total_canciones(self, obj):
        return obj.total_canciones()


class PlaylistCreateSerializer(serializers.ModelSerializer):
    canciones_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True, 
        required=False
    )
    
    class Meta:
        model = Playlist
        fields = ['nombre', 'descripcion', 'es_publica', 'canciones_ids']
    
    def create(self, validated_data):
        canciones_ids = validated_data.pop('canciones_ids', [])
        playlist = Playlist.objects.create(**validated_data)
        
        # Agregar canciones a la playlist
        for idx, cancion_id in enumerate(canciones_ids):
            try:
                cancion = Song.objects.get(id=cancion_id)
                PlaylistSong.objects.create(
                    playlist=playlist,
                    cancion=cancion,
                    orden=idx
                )
            except Song.DoesNotExist:
                continue
        
        return playlist


class FavoriteSerializer(serializers.ModelSerializer):
    cancion = SongSerializer(read_only=True)
    cancion_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'usuario', 'cancion', 'cancion_id', 'fecha_agregada']
        read_only_fields = ['usuario', 'fecha_agregada']


class ListeningHistorySerializer(serializers.ModelSerializer):
    cancion = SongSerializer(read_only=True)
    
    class Meta:
        model = ListeningHistory
        fields = ['id', 'usuario', 'cancion', 'fecha_reproduccion', 'posicion']
        read_only_fields = ['usuario', 'fecha_reproduccion']


class MusicSettingsSerializer(serializers.ModelSerializer):
    ultima_cancion = SongSerializer(read_only=True)
    ultima_playlist = PlaylistSerializer(read_only=True)
    
    class Meta:
        model = MusicSettings
        fields = ['id', 'usuario', 'volumen', 'repetir', 'aleatorio', 
                  'ultima_cancion', 'ultima_playlist']
        read_only_fields = ['usuario']
