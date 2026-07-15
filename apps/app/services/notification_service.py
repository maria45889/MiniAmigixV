"""
Notification service.

Business logic for notification operations.
"""

import logging
from typing import List

from ..selectors.notification_selector import NotificationSelector
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for notification operations."""
    
    @staticmethod
    def create_notification(user, title: str, message: str, notification_type: str = 'info', link: str = ''):
        """Create a notification for user."""
        try:
            notification = NotificationSelector.create_for_user(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                link=link
            )
            LogHelper.log_info(logger, f"Notificación creada: {title}")
            return notification, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al crear notificación: {str(e)}", exc_info=True)
            return None, str(e)
    
    @staticmethod
    def mark_as_read(notification_id: int, user):
        """Mark notification as read."""
        try:
            NotificationSelector.mark_as_read(notification_id, user)
            LogHelper.log_info(logger, f"Notificación marcada como leída: {notification_id}")
            return True, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al marcar notificación: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    def get_user_notifications(user, unread_only: bool = False) -> List:
        """Get notifications for user."""
        try:
            if unread_only:
                return NotificationSelector.get_unread(user)
            return NotificationSelector.get_all(user)
        except Exception as e:
            LogHelper.log_error(logger, f"Error al obtener notificaciones: {str(e)}", exc_info=True)
            return []
