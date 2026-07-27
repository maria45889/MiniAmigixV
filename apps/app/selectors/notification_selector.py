"""
Notification selector.

Database queries for notification operations.
"""

from apps.notificaciones.models import Notificacion


class NotificationSelector:
    """Selector for notification-related queries."""
    
    @staticmethod
    def create_for_user(user, title: str, message: str, notification_type: str = 'info', link: str = ''):
        """Create a notification for user."""
        return Notificacion.objects.create(
            usuario=user,
            titulo=title,
            mensaje=message,
            tipo=notification_type,
            enlace=link
        )
    
    @staticmethod
    def get_all(user):
        """Get all notifications for user."""
        return Notificacion.objects.filter(usuario=user).order_by('-fecha_creacion')
    
    @staticmethod
    def get_unread(user):
        """Get unread notifications for user."""
        return Notificacion.objects.filter(usuario=user, leida=False).order_by('-fecha_creacion')
    
    @staticmethod
    def mark_as_read(notification_id: int, user):
        """Mark notification as read."""
        notification = Notificacion.objects.get(id=notification_id, usuario=user)
        notification.leida = True
        notification.save()
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for user."""
        Notificacion.objects.filter(usuario=user, leida=False).update(leida=True)
