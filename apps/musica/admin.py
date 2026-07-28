from django.contrib import admin
from .models import Song, Playlist, PlaylistSong, Favorite, ListeningHistory, MusicSettings


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'artista', 'album', 'fecha_agregada']
    search_fields = ['titulo', 'artista', 'album']
    list_filter = ['fecha_agregada']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'usuario', 'total_canciones', 'es_publica', 'fecha_creacion']
    search_fields = ['nombre', 'usuario__username']
    list_filter = ['es_publica', 'fecha_creacion']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cancion', 'fecha_agregada']
    search_fields = ['usuario__username', 'cancion__titulo']
    list_filter = ['fecha_agregada']


@admin.register(ListeningHistory)
class ListeningHistoryAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cancion', 'fecha_reproduccion', 'posicion']
    search_fields = ['usuario__username', 'cancion__titulo']
    list_filter = ['fecha_reproduccion']


@admin.register(MusicSettings)
class MusicSettingsAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'volumen', 'repetir', 'aleatorio']
    search_fields = ['usuario__username']
    list_filter = ['repetir', 'aleatorio']
