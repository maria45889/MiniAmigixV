from .admin_utils import is_admin_owner
from .models import Notification


def notifications_context(request):
    """Context processor para agregar notificaciones a los templates"""
    context = {
        'unread_notifications_count': 0,
        'is_admin_owner': False,
    }
    
    if request.user.is_authenticated:
        context['unread_notifications_count'] = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        context['is_admin_owner'] = is_admin_owner(request)
    
    return context
