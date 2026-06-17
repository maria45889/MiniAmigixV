import json
from django.shortcuts import render
from .models import Notificacion
from django.http import JsonResponse
from django.utils import timezone

def lista_notificaciones(request):
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
        no_leidas = notificaciones.filter(leida=False).count()
    else:
        notificaciones = []
        no_leidas = 0
    return render(request, 'notificaciones/lista_notificaciones.html', {
        'notificaciones': notificaciones,
        'no_leidas': no_leidas
    })

def marcar_leidas(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            notif_id = data.get('id')
            if notif_id:
                Notificacion.objects.filter(id=notif_id, usuario=request.user).update(leida=True)
            else:
                Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
            return JsonResponse({'status': 'success'})
        except (json.JSONDecodeError, AttributeError):
            Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def crear_notificacion_prueba(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            Notificacion.objects.create(
                usuario=request.user,
                titulo='🧪 Notificación de Prueba',
                mensaje='Esta es una notificación de prueba creada manualmente para verificar que el sistema funciona correctamente.',
                tipo='info',
                leida=False
            )
            return JsonResponse({'status': 'success', 'message': 'Notificación de prueba creada'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido o usuario no autenticado'}, status=400)
