# ============================================================================
# VIEWS
# ============================================================================

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Temporalmente deshabilitado - incompatible con Django 6.0
# from webpush import send_user_notification


@login_required
def send_test_notification(request):
    """
    Vista para enviar una notificación de prueba.
    Temporalmente deshabilitado - webpush incompatible con Django 6.0.
    """
    if request.method == 'POST':
        try:
            # Puedes personalizar el payload de la notificación
            payload = {
                "head": "¡Notificación de Prueba MiniAmigixV!",
                "body": "Esta es una notificación push de prueba enviada desde tu servidor Django.",
                "icon": "/static/imagenes/logo.png",
                "url": "/"
            }
            # send_user_notification(user=request.user, payload=payload, ttl=1000)
            return JsonResponse({'status': 'success', 'message': 'Notificación de prueba enviada.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})