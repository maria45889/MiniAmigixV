"""
Admin views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import logging

logger = logging.getLogger(__name__)


@staff_member_required
def panel_admin(request):
    """Render admin panel dashboard."""
    return render(request, 'panel_admin.html')


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
    return render(request, 'admin_email_user.html', {'user_id': user_id})


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
        # Placeholder for stats logic
        stats = {
            'users': 0,
            'chats': 0,
            'events': 0,
            'tickets': 0,
            'suggestions': 0
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
