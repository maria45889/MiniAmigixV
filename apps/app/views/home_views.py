"""
Home views.
"""

import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.app.services import UserService
from apps.app.selectors import ChatSelector, CalendarSelector, MusicSelector
from apps.app.selectors.calendar_selector import CalendarSelector

FRASES = [
    ("La imaginación es más importante que el conocimiento.", "Albert Einstein"),
    ("El único modo de hacer un gran trabajo es amar lo que haces.", "Steve Jobs"),
    ("La educación es el arma más poderosa que puedes usar para cambiar el mundo.", "Nelson Mandela"),
    ("No es la especie más fuerte la que sobrevive, sino la que mejor se adapta al cambio.", "Charles Darwin"),
    ("El futuro pertenece a quienes creen en la belleza de sus sueños.", "Eleanor Roosevelt"),
    ("La creatividad es la inteligencia divirtiéndose.", "Albert Einstein"),
    ("Cada día es una nueva oportunidad para cambiar tu vida.", "Anónimo"),
    ("El éxito es la suma de pequeños esfuerzos repetidos día tras día.", "Robert Collier"),
    ("No busques los errores, busca un remedio.", "Henry Ford"),
    ("La tecnología es solo una herramienta. La gente es quien marca la diferencia.", "Bill Gates"),
    ("Aprende como si fueras a vivir para siempre.", "Mahatma Gandhi"),
    ("La mejor manera de predecir el futuro es crearlo.", "Peter Drucker"),
    ("Todo experto fue alguna vez un principiante.", "Helen Hayes"),
    ("El conocimiento es poder.", "Francis Bacon"),
    ("Nunca es tarde para ser lo que podrías haber sido.", "George Eliot"),
    ("La música expresa lo que no puede decirse con palabras.", "Victor Hugo"),
    ("Un día sin aprender es un día perdido.", "Anónimo"),
    ("Lo que sabemos es una gota, lo que ignoramos es un océano.", "Isaac Newton"),
    ("La curiosidad es la mecha de la creatividad.", "Anónimo"),
    ("Haz de cada día tu obra maestra.", "John Wooden"),
]


def home(request):
    """Render home page."""
    context = {}
    
    # Frase motivacional aleatoria
    frase = random.choice(FRASES)
    context['frase_texto'] = frase[0]
    context['frase_autor'] = frase[1]
    
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
