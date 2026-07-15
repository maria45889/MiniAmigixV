"""
Weather views.
"""

from django.shortcuts import render

from apps.app.services import WeatherService


def clima(request):
    """Render weather page."""
    ciudad = request.GET.get('ciudad', 'Quito')
    datos_clima = None
    error = None
    
    try:
        datos_clima = WeatherService.get_current_weather(ciudad)
    except Exception as e:
        error = str(e)
    
    return render(request, 'clima.html', {
        'datos_clima': datos_clima,
        'ciudad': ciudad,
        'error': error
    })
