from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Song(models.Model):
    """Modelo para representar una canción"""
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    album = models.CharField(max_length=200, null=True, blank=True)
    duracion = models.IntegerField(null=True, blank=True, help_text='Duración en segundos')
    youtube_url = models.URLField(null=True, blank=True)
    youtube_video_id = models.CharField(max_length=50, null=True, blank=True)
    portada_url = models.URLField(null=True, blank=True)
    letra = models.TextField(null=True, blank=True)
    fecha_agregada = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.artista}"
    
    class Meta:
        ordering = ['-fecha_agregada']
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'


class Playlist(models.Model):
    """Modelo para representar una playlist de canciones"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    canciones = models.ManyToManyField(Song, through='PlaylistSong', related_name='playlists')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    es_publica = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
    
    class Meta:
        ordering = ['-fecha_actualizacion']
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
    
    def total_canciones(self):
        return self.canciones.count()


class PlaylistSong(models.Model):
    """Modelo intermedio para ordenar canciones en playlists"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Song, on_delete=models.CASCADE)
    orden = models.IntegerField(default=0)
    fecha_agregada = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Canción en Playlist'
        verbose_name_plural = 'Canciones en Playlists'
        unique_together = ['playlist', 'cancion']


class Favorite(models.Model):
    """Modelo para representar canciones favoritas de un usuario"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    cancion = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favoritos')
    fecha_agregada = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.cancion.titulo}"
    
    class Meta:
        ordering = ['-fecha_agregada']
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        unique_together = ['usuario', 'cancion']


class ListeningHistory(models.Model):
    """Modelo para registrar el historial de reproducción"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historial_reproduccion')
    cancion = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='reproducciones')
    fecha_reproduccion = models.DateTimeField(auto_now_add=True)
    posicion = models.IntegerField(default=0, help_text='Posición en segundos donde se reprodujo')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.cancion.titulo} - {self.fecha_reproduccion}"
    
    class Meta:
        ordering = ['-fecha_reproduccion']
        verbose_name = 'Historial de Reproducción'
        verbose_name_plural = 'Historiales de Reproducción'


class MusicSettings(models.Model):
    """Modelo para guardar configuraciones de música del usuario"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='configuracion_musica')
    volumen = models.FloatField(default=0.7, help_text='Volumen entre 0 y 1')
    repetir = models.CharField(max_length=20, default='none', choices=[
        ('none', 'No repetir'),
        ('one', 'Repetir una'),
        ('all', 'Repetir todas'),
    ])
    aleatorio = models.BooleanField(default=False)
    ultima_cancion = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True)
    ultima_playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Configuración de {self.usuario.username}"
    
    class Meta:
        verbose_name = 'Configuración de Música'
        verbose_name_plural = 'Configuraciones de Música'
