"""
Views module.

Contains HTTP view functions for different domains.
"""

from .auth_views import login_view, register_view, logout_view
from .chat_views import chat_view, chat_api
from .home_views import home, index
from .music_views import musica, crear_playlist, agregar_a_playlist, toggle_favorito
from .calendar_views import eventos
from .weather_views import clima
from .study_views import estudio
from .entertainment_views import entretenimiento
from .profile_views import perfil, configuracion

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
    'eventos',
    'clima',
    'estudio',
    'entretenimiento',
    'perfil',
    'configuracion'
]
