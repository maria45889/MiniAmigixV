"""
Views module.

Contains HTTP view functions for different domains.
"""

from .auth_views import login_view, register_view, logout_view
from .chat_views import chat_view, chat_api
from .home_views import home, index
from .music_views import musica, crear_playlist, agregar_a_playlist, toggle_favorito, add_song_api, stream_audio_api, update_theme_api, update_language_api, search_lyrics_api, get_lyrics_api, save_lyrics_api, netease_lyrics_api, download_media_api, delete_chat_api, delete_song_api, edit_song_api
from .calendar_views import eventos
from .weather_views import clima
from .study_views import estudio
from .entertainment_views import entretenimiento
from .profile_views import perfil, configuracion
from .admin_views import panel_admin, admin_soporte, admin_sugerencias, panel_admin_email_user, responder_ticket, responder_sugerencia, admin_stats_api, exportar_reporte_excel
from .games_views import juegos, guardar_puntuacion
from .suggestion_views import enviar_sugerencia_rapida

__all__ = [
    'login_view',
    'register_view',
    'logout_view',
    'chat_view',
    'chat_api',
    'home',
    'index',
    'musica',
    'crear_playlist',
    'agregar_a_playlist',
    'toggle_favorito',
    'add_song_api',
    'stream_audio_api',
    'update_theme_api',
    'update_language_api',
    'search_lyrics_api',
    'get_lyrics_api',
    'save_lyrics_api',
    'netease_lyrics_api',
    'download_media_api',
    'delete_chat_api',
    'delete_song_api',
    'edit_song_api',
    'eventos',
    'clima',
    'estudio',
    'entretenimiento',
    'perfil',
    'configuracion',
    'panel_admin',
    'admin_soporte',
    'admin_sugerencias',
    'panel_admin_email_user',
    'responder_ticket',
    'responder_sugerencia',
    'admin_stats_api',
    'exportar_reporte_excel',
    'juegos',
    'guardar_puntuacion',
    'enviar_sugerencia_rapida'
]
