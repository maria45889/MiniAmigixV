from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Song, Playlist, PlaylistSong, Favorite, ListeningHistory, MusicSettings
from .serializers import (
    SongSerializer, SongCreateSerializer, PlaylistSerializer, 
    PlaylistCreateSerializer, FavoriteSerializer, ListeningHistorySerializer,
    MusicSettingsSerializer
)


class SongViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar canciones"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SongCreateSerializer
        return SongSerializer
    
    def get_queryset(self):
        queryset = Song.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                titulo__icontains=search
            ) | queryset.filter(
                artista__icontains=search
            )
        return queryset.order_by('-fecha_agregada')
    
    @action(detail=False, methods=['get'])
    def library(self, request):
        """Obtener todas las canciones de la biblioteca"""
        songs = self.get_queryset()
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def play(self, request, pk=None):
        """Registrar reproducción de una canción"""
        song = self.get_object()
        posicion = request.data.get('posicion', 0)
        
        # Crear registro en historial
        ListeningHistory.objects.create(
            usuario=request.user,
            cancion=song,
            posicion=posicion
        )
        
        # Actualizar configuración de música
        settings_obj, created = MusicSettings.objects.get_or_create(
            usuario=request.user
        )
        settings_obj.ultima_cancion = song
        settings_obj.save()
        
        return Response({'success': True, 'song': SongSerializer(song).data})


class PlaylistViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar playlists"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PlaylistCreateSerializer
        return PlaylistSerializer
    
    def get_queryset(self):
        return Playlist.objects.filter(usuario=request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_song(self, request, pk=None):
        """Agregar una canción a la playlist"""
        playlist = self.get_object()
        cancion_id = request.data.get('cancion_id')
        
        if not cancion_id:
            return Response(
                {'error': 'Se requiere cancion_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cancion = Song.objects.get(id=cancion_id)
            # Obtener el último orden
            last_order = PlaylistSong.objects.filter(
                playlist=playlist
            ).count()
            
            PlaylistSong.objects.create(
                playlist=playlist,
                cancion=cancion,
                orden=last_order
            )
            
            return Response({'success': True})
        except Song.DoesNotExist:
            return Response(
                {'error': 'Canción no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_song(self, request, pk=None):
        """Eliminar una canción de la playlist"""
        playlist = self.get_object()
        cancion_id = request.data.get('cancion_id')
        
        if not cancion_id:
            return Response(
                {'error': 'Se requiere cancion_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            playlist_song = PlaylistSong.objects.get(
                playlist=playlist,
                cancion_id=cancion_id
            )
            playlist_song.delete()
            return Response({'success': True})
        except PlaylistSong.DoesNotExist:
            return Response(
                {'error': 'Canción no encontrada en playlist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def reorder_songs(self, request, pk=None):
        """Reordenar canciones en la playlist"""
        playlist = self.get_object()
        songs_order = request.data.get('songs_order', [])
        
        if not isinstance(songs_order, list):
            return Response(
                {'error': 'songs_order debe ser una lista'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        for idx, cancion_id in enumerate(songs_order):
            try:
                playlist_song = PlaylistSong.objects.get(
                    playlist=playlist,
                    cancion_id=cancion_id
                )
                playlist_song.orden = idx
                playlist_song.save()
            except PlaylistSong.DoesNotExist:
                continue
        
        return Response({'success': True})


class FavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar favoritos"""
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    
    def get_queryset(self):
        return Favorite.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Alternar favorito de una canción"""
        cancion_id = request.data.get('cancion_id')
        
        if not cancion_id:
            return Response(
                {'error': 'Se requiere cancion_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cancion = Song.objects.get(id=cancion_id)
            favorite = Favorite.objects.filter(
                usuario=request.user,
                cancion=cancion
            ).first()
            
            if favorite:
                favorite.delete()
                return Response({'is_favorite': False})
            else:
                Favorite.objects.create(
                    usuario=request.user,
                    cancion=cancion
                )
                return Response({'is_favorite': True})
        except Song.DoesNotExist:
            return Response(
                {'error': 'Canción no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def check(self, request):
        """Verificar si una canción es favorita"""
        cancion_id = request.query_params.get('cancion_id')
        
        if not cancion_id:
            return Response(
                {'error': 'Se requiere cancion_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_favorite = Favorite.objects.filter(
            usuario=request.user,
            cancion_id=cancion_id
        ).exists()
        
        return Response({'is_favorite': is_favorite})


class ListeningHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para ver historial de reproducción"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListeningHistorySerializer
    
    def get_queryset(self):
        return ListeningHistory.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha_reproduccion')[:50]
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Limpiar historial de reproducción"""
        ListeningHistory.objects.filter(usuario=request.user).delete()
        return Response({'success': True})


class MusicSettingsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar configuración de música"""
    permission_classes = [IsAuthenticated]
    serializer_class = MusicSettingsSerializer
    
    def get_queryset(self):
        return MusicSettings.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_settings(self, request):
        """Obtener configuración del usuario actual"""
        settings_obj, created = MusicSettings.objects.get_or_create(
            usuario=request.user
        )
        serializer = self.get_serializer(settings_obj)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_volume(self, request):
        """Actualizar volumen"""
        volumen = request.data.get('volumen')
        
        if volumen is None:
            return Response(
                {'error': 'Se requiere volumen'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        settings_obj, created = MusicSettings.objects.get_or_create(
            usuario=request.user
        )
        settings_obj.volumen = max(0, min(1, float(volumen)))
        settings_obj.save()
        
        return Response({'success': True, 'volumen': settings_obj.volumen})
    
    @action(detail=False, methods=['post'])
    def toggle_shuffle(self, request):
        """Alternar modo aleatorio"""
        settings_obj, created = MusicSettings.objects.get_or_create(
            usuario=request.user
        )
        settings_obj.aleatorio = not settings_obj.aleatorio
        settings_obj.save()
        
        return Response({'success': True, 'aleatorio': settings_obj.aleatorio})
    
    @action(detail=False, methods=['post'])
    def set_repeat(self, request):
        """Establecer modo de repetición"""
        repeat_mode = request.data.get('repeat_mode', 'none')
        
        if repeat_mode not in ['none', 'one', 'all']:
            return Response(
                {'error': 'Modo de repetición inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        settings_obj, created = MusicSettings.objects.get_or_create(
            usuario=request.user
        )
        settings_obj.repetir = repeat_mode
        settings_obj.save()
        
        return Response({'success': True, 'repetir': settings_obj.repetir})
