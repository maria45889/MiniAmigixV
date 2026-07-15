"""
Entertainment views.
"""

from django.shortcuts import render

from apps.app.constants import ENTERTAINMENT_RECOMMENDATIONS


def entretenimiento(request):
    """Render entertainment page."""
    recomendaciones = ENTERTAINMENT_RECOMMENDATIONS
    return render(request, 'entretenimiento.html', {'recomendaciones': recomendaciones})
