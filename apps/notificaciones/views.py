import json
from django.shortcuts import render
from .models import Notificacion
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

def lista_notificaciones(request):
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fijada', '-prioridad', '-fecha_creacion')
        no_leidas = notificaciones.filter(leida=False).count()
        total = notificaciones.count()
        
        # Group by date
        notificaciones_por_fecha = defaultdict(list)
        for notif in notificaciones:
            fecha = notif.fecha_creacion
            hoy = timezone.now().date()
            
            if fecha.date() == hoy:
                grupo = 'Hoy'
            elif fecha.date() == hoy - timedelta(days=1):
                grupo = 'Ayer'
            elif fecha.date() >= hoy - timedelta(days=7):
                grupo = 'Esta semana'
            elif fecha.date() >= hoy - timedelta(days=30):
                grupo = 'Este mes'
            else:
                grupo = fecha.strftime('%B %Y')
            
            notificaciones_por_fecha[grupo].append(notif)
        
        # Statistics by category
        stats_por_categoria = {}
        for cat_choice, cat_label in Notificacion._meta.get_field('categoria').choices:
            count = notificaciones.filter(categoria=cat_choice).count()
            if count > 0:
                stats_por_categoria[cat_choice] = count
        
        # Featured notifications (high priority or pinned)
        destacadas = notificaciones.filter(prioridad='alta')[:3]
    else:
        notificaciones = []
        no_leidas = 0
        total = 0
        notificaciones_por_fecha = {}
        stats_por_categoria = {}
        destacadas = []
    
    return render(request, 'notificaciones/lista_notificaciones.html', {
        'notificaciones': notificaciones,
        'notificaciones_por_fecha': dict(notificaciones_por_fecha),
        'no_leidas': no_leidas,
        'total': total,
        'stats_por_categoria': stats_por_categoria,
        'destacadas': destacadas,
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

def eliminar_notificacion(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            notif_id = data.get('id')
            if notif_id:
                Notificacion.objects.filter(id=notif_id, usuario=request.user).delete()
                return JsonResponse({'status': 'success'})
        except (json.JSONDecodeError, AttributeError):
            pass
    return JsonResponse({'status': 'error'}, status=400)

def fijar_notificacion(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            notif_id = data.get('id')
            fijar = data.get('fijar', True)
            if notif_id:
                Notificacion.objects.filter(id=notif_id, usuario=request.user).update(fijada=fijar)
                return JsonResponse({'status': 'success'})
        except (json.JSONDecodeError, AttributeError):
            pass
    return JsonResponse({'status': 'error'}, status=400)

def buscar_notificaciones(request):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')
        if query:
            notificaciones = Notificacion.objects.filter(
                usuario=request.user,
                titulo__icontains=query
            ).order_by('-fecha_creacion')[:20]
            results = [
                {
                    'id': n.id,
                    'titulo': n.titulo,
                    'mensaje': n.mensaje[:100],
                    'tipo': n.tipo,
                    'categoria': n.categoria,
                    'leida': n.leida,
                    'fecha': n.fecha_creacion.strftime('%d M Y, H:i'),
                    'enlace': n.enlace,
                }
                for n in notificaciones
            ]
            return JsonResponse({'status': 'success', 'results': results})
    return JsonResponse({'status': 'error'}, status=400)

