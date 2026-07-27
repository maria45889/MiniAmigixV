"""
User service.

Business logic for user operations.
"""

import logging
from typing import Dict

from ..selectors.user_selector import UserSelector
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related operations."""
    
    @staticmethod
    def get_user_statistics(user) -> Dict:
        """Get statistics for a user."""
        from ..selectors.chat_selector import ChatSelector
        from ..selectors.calendar_selector import CalendarSelector
        from ..selectors.music_selector import MusicSelector
        
        return {
            'chats': ChatSelector.count_by_user(user),
            'notas': 0,
            'eventos': CalendarSelector.count_all(),
            'canciones': MusicSelector.count_songs(user)
        }
    
    @staticmethod
    def update_user_profile(user, **kwargs):
        """Update user profile."""
        try:
            UserSelector.update_user(user, **kwargs)
            LogHelper.log_info(logger, f"Perfil actualizado: {user.username}")
            return True, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al actualizar perfil: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    def update_theme(user, theme):
        """Update user theme preference."""
        try:
            from apps.perfil.models import Perfil
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            perfil.tema = theme
            perfil.save()
            LogHelper.log_info(logger, f"Tema actualizado para {user.username}: {theme}")
            return True, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al actualizar tema: {str(e)}", exc_info=True)
            return False, str(e)
