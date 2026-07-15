"""
Games views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


@login_required
def juegos(request):
    """Render games page."""
    return render(request, 'juegos.html')


@require_http_methods(["POST"])
@csrf_exempt
def guardar_puntuacion(request):
    """Save game score."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    try:
        import json
        data = json.loads(request.body)
        juego = data.get('juego')
        puntuacion = data.get('puntuacion')
        
        # Placeholder for score saving logic
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Error al guardar puntuación: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
