"""
Admin views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@staff_member_required
def panel_admin(request):
    """Render admin panel dashboard with statistics."""
    from django.db.models import Count, Q, Avg
    from apps.app.models import ConversacionChat, Cancion, Playlist
    from apps.eventos.models import Evento
    from apps.notificaciones.models import Notificacion
    from apps.soporte.models import TicketSoporte
    from apps.blog.models import Post, Category, Comment
    from apps.sugerencias.models import Sugerencia, Visitante
    
    # Calculate dates for filtering
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # User statistics
    total_usuarios = User.objects.count()
    ultimos_usuarios = User.objects.order_by('-date_joined')[:10]
    
    # Chat statistics
    total_chats = ConversacionChat.objects.count()
    
    # Music statistics
    total_canciones = Cancion.objects.count()
    total_playlists = Playlist.objects.count()
    total_reproducciones = 0  # Placeholder - could be tracked separately
    
    # Event statistics
    total_eventos = Evento.objects.count()
    
    # Notification statistics
    total_notificaciones = Notificacion.objects.filter(leida=False).count()
    ultimas_notificaciones = Notificacion.objects.order_by('-fecha_creacion')[:5]
    
    # Support statistics
    total_tickets_pendientes = TicketSoporte.objects.filter(estado='abierto').count()
    total_tickets_resueltos = TicketSoporte.objects.filter(estado='resuelto').count()
    
    # Calculate average response time for resolved tickets
    resolved_tickets = TicketSoporte.objects.filter(
        estado='resuelto',
        fecha_resolucion__isnull=False,
        fecha_respuesta__isnull=False
    )
    if resolved_tickets.exists():
        avg_response = resolved_tickets.annotate(
            response_time=Avg('fecha_respuesta' - 'fecha_creacion')
        ).aggregate(avg=Avg('response_time'))['avg']
        tiempo_promedio_respuesta = f"{avg_response.days}d" if avg_response else "N/A"
    else:
        tiempo_promedio_respuesta = "N/A"
    
    # Blog statistics
    total_publicaciones = Post.objects.filter(publicado=True).count()
    total_categorias = Category.objects.count()
    total_comentarios = Comment.objects.count()
    ultimas_publicaciones = Post.objects.filter(publicado=True).order_by('-fecha_publicacion')[:5]
    
    # Suggestions statistics
    ultimas_sugerencias = Sugerencia.objects.order_by('-fecha_creacion')[:5]
    
    # Visitor statistics
    visitantes_hoy = Visitante.objects.filter(fecha_ultima_interaccion__date=today).count()
    visitantes_semana = Visitante.objects.filter(fecha_ultima_interaccion__date__gte=week_ago).count()
    visitantes_mes = Visitante.objects.filter(fecha_ultima_interaccion__date__gte=month_ago).count()
    ultimos_visitantes = Visitante.objects.order_by('-fecha_ultima_interaccion')[:10]
    
    # Security statistics (placeholders for now)
    intentos_fallidos = 0
    sesiones_activas = User.objects.filter(last_login__gte=timezone.now() - timedelta(hours=1)).count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_chats': total_chats,
        'total_canciones': total_canciones,
        'total_eventos': total_eventos,
        'total_notificaciones': total_notificaciones,
        'total_tickets_pendientes': total_tickets_pendientes,
        'total_tickets_resueltos': total_tickets_resueltos,
        'tiempo_promedio_respuesta': tiempo_promedio_respuesta,
        'total_publicaciones': total_publicaciones,
        'total_categorias': total_categorias,
        'total_comentarios': total_comentarios,
        'total_reproducciones': total_reproducciones,
        'total_playlists': total_playlists,
        'visitantes_hoy': visitantes_hoy,
        'visitantes_semana': visitantes_semana,
        'visitantes_mes': visitantes_mes,
        'ultimos_usuarios': ultimos_usuarios,
        'ultimas_notificaciones': ultimas_notificaciones,
        'ultimas_publicaciones': ultimas_publicaciones,
        'ultimas_sugerencias': ultimas_sugerencias,
        'ultimos_visitantes': ultimos_visitantes,
        'intentos_fallidos': intentos_fallidos,
        'sesiones_activas': sesiones_activas,
    }
    
    return render(request, 'panel_admin.html', context)


@staff_member_required
def admin_soporte(request):
    """Render admin support panel."""
    return render(request, 'admin_soporte.html')


@staff_member_required
def admin_sugerencias(request):
    """Render admin suggestions panel."""
    return render(request, 'admin_sugerencias.html')


@staff_member_required
def panel_admin_email_user(request, user_id):
    """Render email user form."""
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    return render(request, 'panel_admin_email_user.html', {'user_id': user_id, 'user_target': user})


@require_http_methods(["POST"])
@staff_member_required
@csrf_exempt
def responder_ticket(request, ticket_id):
    """Respond to a support ticket."""
    try:
        import json
        data = json.loads(request.body)
        respuesta = data.get('respuesta')
        
        # Placeholder for ticket response logic
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Error al responder ticket: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@staff_member_required
@csrf_exempt
def responder_sugerencia(request, sugerencia_id):
    """Respond to a suggestion."""
    try:
        import json
        data = json.loads(request.body)
        respuesta = data.get('respuesta')
        estado = data.get('estado')
        
        # Placeholder for suggestion response logic
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Error al responder sugerencia: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
@staff_member_required
def admin_stats_api(request):
    """Get admin statistics."""
    try:
        from django.db.models import Count, Q, Avg
        from apps.app.models import ConversacionChat, Cancion, Playlist
        from apps.eventos.models import Evento
        from apps.notificaciones.models import Notificacion
        from apps.soporte.models import TicketSoporte
        from apps.blog.models import Post, Category, Comment
        from apps.sugerencias.models import Sugerencia, Visitante
        from django.utils import timezone
        from datetime import timedelta
        
        # Calculate dates for filtering
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Gather statistics
        stats = {
            'total_usuarios': User.objects.count(),
            'total_chats': ConversacionChat.objects.count(),
            'total_canciones': Cancion.objects.count(),
            'total_eventos': Evento.objects.count(),
            'total_notificaciones': Notificacion.objects.filter(leida=False).count(),
            'total_tickets_pendientes': TicketSoporte.objects.filter(estado='abierto').count(),
            'total_tickets_resueltos': TicketSoporte.objects.filter(estado='resuelto').count(),
            'total_publicaciones': Post.objects.filter(publicado=True).count(),
            'total_categorias': Category.objects.count(),
            'total_comentarios': Comment.objects.count(),
            'total_reproducciones': 0,  # Placeholder
            'total_playlists': Playlist.objects.count(),
            'visitantes_hoy': Visitante.objects.filter(fecha_ultima_interaccion__date=today).count(),
            'visitantes_semana': Visitante.objects.filter(fecha_ultima_interaccion__date__gte=week_ago).count(),
            'visitantes_mes': Visitante.objects.filter(fecha_ultima_interaccion__date__gte=month_ago).count(),
            'intentos_fallidos': 0,
            'sesiones_activas': User.objects.filter(last_login__gte=timezone.now() - timedelta(hours=1)).count(),
        }
        return JsonResponse(stats)
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def exportar_reporte_excel(request):
    """Export report to Excel."""
    # Placeholder for Excel export
    return JsonResponse({'error': 'Función no implementada'}, status=501)
