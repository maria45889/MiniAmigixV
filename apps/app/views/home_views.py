"""
Home views.
"""

import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.app.services import UserService
from apps.app.selectors import CalendarSelector

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
        stats = UserService.get_user_statistics(request.user)
        context['stats_chats'] = stats.get('chats', 0)
        context['stats_canciones'] = stats.get('canciones', 0)
        context['stats_eventos'] = stats.get('eventos', 0)
        
        # Obtener eventos próximos para el reloj inteligente
        eventos_proximos = CalendarSelector.get_for_clock_widget(3, 3)
        context['eventos_proximos'] = eventos_proximos
        
        # Obtener clima real
        try:
            from apps.app.services import WeatherService
            clima_data = WeatherService.get_current_weather()
            if clima_data:
                context['clima_temp'] = clima_data.get('temp', 23)
                context['clima_desc'] = clima_data.get('description', 'Parcialmente nublado')
                context['clima_icon'] = clima_data.get('icon', '⛅')
        except:
            context['clima_temp'] = 23
            context['clima_desc'] = 'Parcialmente nublado'
            context['clima_icon'] = '⛅'
        
        # Actividad reciente del usuario
        from apps.app.models import ConversacionChat
        from apps.app.models import Cancion
        from eventos.models import Evento
        from django.utils import timezone
        from datetime import timedelta
        
        actividad = []
        
        # Último chat
        ultimo_chat = ConversacionChat.objects.filter(usuario=request.user).order_by('-fecha_actualizacion').first()
        if ultimo_chat:
            actividad.append({
                'tipo': 'chat',
                'nombre': 'Chat IA',
                'tiempo': 'Hoy' if ultimo_chat.fecha_actualizacion.date() == timezone.now().date() else 'Ayer',
                'icono': 'ti ti-message-dots',
                'bg': 'chat-bg'
            })
        
        # Última canción agregada
        ultima_cancion = Cancion.objects.filter(usuario=request.user).order_by('-fecha_agregada').first()
        if ultima_cancion:
            actividad.append({
                'tipo': 'musica',
                'nombre': 'Música',
                'tiempo': 'Hoy' if ultima_cancion.fecha_agregada.date() == timezone.now().date() else 'Ayer',
                'icono': 'ti ti-music',
                'bg': 'music-bg'
            })
        
        # Último evento creado
        ultimo_evento = Evento.objects.filter(usuario=request.user).order_by('-fecha_creacion').first()
        if ultimo_evento:
            actividad.append({
                'tipo': 'evento',
                'nombre': 'Evento creado',
                'tiempo': 'Hoy' if ultimo_evento.fecha_creacion.date() == timezone.now().date() else 'Ayer',
                'icono': 'ti ti-calendar',
                'bg': 'events-bg'
            })
        
        context['actividad_reciente'] = actividad[:4]
    else:
        # Datos por defecto para usuarios no autenticados
        context['stats_chats'] = 0
        context['stats_canciones'] = 0
        context['stats_eventos'] = 0
        context['clima_temp'] = 23
        context['clima_desc'] = 'Parcialmente nublado'
        context['clima_icon'] = '⛅'
        context['actividad_reciente'] = []
    
    return render(request, 'home.html', context)


def index(request):
    """Redirect to tutorial home."""
    return redirect('tutorial_home')
