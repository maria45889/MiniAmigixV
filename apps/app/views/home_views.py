"""
Home views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.app.services import UserService
from apps.app.selectors import ChatSelector, CalendarSelector, MusicSelector
from apps.app.selectors.calendar_selector import CalendarSelector


def home(request):
    """Render home page."""
    context = {}
    
    # Estadísticas del usuario
    if request.user.is_authenticated:
        context['stats'] = UserService.get_user_statistics(request.user)
        
        # Obtener eventos próximos para el reloj inteligente
        eventos_proximos = CalendarSelector.get_for_clock_widget(3, 3)
        context['eventos_proximos'] = eventos_proximos
    
    return render(request, 'home.html', context)


def index(request):
    """Redirect to tutorial home."""
    return redirect('tutorial_home')
