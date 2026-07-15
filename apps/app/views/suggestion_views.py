"""
Suggestion views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@csrf_exempt
def enviar_sugerencia_rapida(request):
    """Send quick suggestion."""
    try:
        import json
        data = json.loads(request.body)
        sugerencia = data.get('sugerencia')
        
        # Placeholder for suggestion logic
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Error al enviar sugerencia: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
