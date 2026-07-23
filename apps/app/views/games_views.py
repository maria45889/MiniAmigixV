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
    from apps.app.models import Game
    
    juegos = Game.objects.filter(activo=True).distinct()
    
    # Calcular estadísticas
    from django.db.models import Max
    from apps.app.models import Score
    
    mejor_puntuacion = Score.objects.filter(usuario=request.user).aggregate(max_puntuacion=Max('puntuacion'))['max_puntuacion'] or 0
    
    from django.utils import timezone
    from datetime import datetime, timedelta
    hoy = timezone.now().date()
    partidas_hoy = Score.objects.filter(usuario=request.user, fecha_juego__date=hoy).count()
    
    # Obtener último juego jugado
    ultima_puntuacion = Score.objects.filter(usuario=request.user).order_by('-fecha_juego').first()
    ultimo_juego = ultima_puntuacion.juego if ultima_puntuacion else None
    
    context = {
        'juegos': juegos,
        'mejor_puntuacion': mejor_puntuacion,
        'partidas_hoy': partidas_hoy,
        'ultimo_juego': ultimo_juego,
    }
    
    return render(request, 'juegos.html', context)


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
