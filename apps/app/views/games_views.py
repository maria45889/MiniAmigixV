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


def _get_or_create_arcade_profile(user):
    """Get or create ArcadeProfile for a user."""
    from apps.app.models import ArcadeProfile
    profile, _ = ArcadeProfile.objects.get_or_create(usuario=user)
    return profile


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

    # Get or create arcade profile for real stats
    arcade = _get_or_create_arcade_profile(request.user)

    context = {
        'juegos': juegos,
        'mejor_puntuacion': mejor_puntuacion,
        'partidas_hoy': partidas_hoy,
        'ultimo_juego': ultimo_juego,
        # Real arcade stats
        'arcade_xp': arcade.xp,
        'arcade_monedas': arcade.monedas,
        'arcade_partidas': arcade.partidas_ganadas,
        'arcade_racha': arcade.racha_dias,
        'arcade_nivel': arcade.nivel,
    }

    return render(request, 'juegos.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def guardar_puntuacion(request):
    """Save game score and award XP/coins to the user's ArcadeProfile."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)

    try:
        import json
        data = json.loads(request.body)
        xp_ganado = int(data.get('xp', 0))
        monedas_ganadas = int(data.get('monedas', 10))
        nombre_juego = data.get('juego', 'Juego')

        arcade = _get_or_create_arcade_profile(request.user)
        arcade.add_xp(xp_ganado, monedas_ganadas)

        return JsonResponse({
            'success': True,
            'xp_total': arcade.xp,
            'monedas_total': arcade.monedas,
            'partidas': arcade.partidas_ganadas,
            'racha': arcade.racha_dias,
            'nivel': arcade.nivel,
        })
    except Exception as e:
        logger.error(f"Error al guardar puntuación: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

