from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from webpush import send_user_notification
import json

@login_required
def send_test_notification(request):
    if request.method == 'POST':
        try:
            # Puedes personalizar el payload de la notificación
            payload = {
                "head": "¡Notificación de Prueba MiniAmigixV!",
                "body": "Esta es una notificación push de prueba enviada desde tu servidor Django.",
                "icon": "/static/logo.svg", # Asegúrate de que esta ruta sea accesible
                "url": "/" # URL a la que redirigirá al hacer clic
            }
            send_user_notification(user=request.user, payload=payload, ttl=1000)
            return JsonResponse({'status': 'success', 'message': 'Notificación de prueba enviada.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})