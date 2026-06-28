from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import json
import os
import re
import logging
import openai
import requests
import random
import datetime
from django.utils import timezone
import yt_dlp
from .models import ConversacionChat, MensajeChat, Cancion, PublicacionBlog, Playlist, Favorite, Game, Score, Achievement, UserAchievement, Category, Comment, EstadoAnimo, RecomendacionEntretenimiento
from eventos.models import Evento
from notificaciones.models import Notificacion
from apps.mongodb.services import DualDatabaseService

logger = logging.getLogger(__name__)

# Create your views here.

@require_http_methods(["POST"])
def chat_api(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        conv_id = data.get('conversation_id')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    if not message:
        return JsonResponse({'error': 'No message provided'}, status=400)

    try:
        # Get or create conversation for user
        if request.user.is_authenticated:
            if conv_id:
                conversacion = ConversacionChat.objects.filter(usuario=request.user, id=conv_id).first()
                if not conversacion:
                    return JsonResponse({'error': 'Conversation not found'}, status=404)
            else:
                # Evitamos get_or_create en campos no únicos para prevenir errores
                conversacion = ConversacionChat.objects.filter(usuario=request.user).first()
                if not conversacion:
                    conversacion = ConversacionChat.objects.create(usuario=request.user, titulo='Chat Principal')
            
            # Save user message
            MensajeChat.objects.create(
                conversacion=conversacion,
                es_usuario=True,
                texto=message
            )
            conversacion.save() # Forzamos la actualización de fecha_actualizacion (auto_now)
            
            # Guardar también en MongoDB (historial y análisis)
            DualDatabaseService.guardar_chat_mensaje(
                usuario=request.user.username,
                mensaje=message,
                respuesta=None,
                usar_mongodb=True
            )
            
            # Get conversation history
            # Fetch latest 10 and reverse to restore chronological order
            mensajes = list(MensajeChat.objects.filter(conversacion=conversacion).order_by('-fecha_creacion')[:10])[::-1]
            
            # Obtener eventos próximos del calendario (5 días antes y 3 días antes)
            eventos_proximos = []
            hoy = datetime.date.today()
            # Eventos en los próximos 5 días
            fecha_limite = hoy + datetime.timedelta(days=5)
            eventos = Evento.objects.filter(fecha__gte=hoy, fecha__lte=fecha_limite).order_by('fecha')
            
            for evento in eventos:
                dias_restantes = (evento.fecha - hoy).days
                if dias_restantes == 0:
                    texto_dias = "hoy"
                elif dias_restantes == 1:
                    texto_dias = "mañana"
                elif dias_restantes <= 3:
                    texto_dias = f"en {dias_restantes} días"
                else:
                    texto_dias = f"en {dias_restantes} días"
                eventos_proximos.append(f"- {evento.titulo} ({texto_dias}, {evento.fecha.strftime('%d/%m/%Y')})")
            
            eventos_contexto = "\n".join(eventos_proximos) if eventos_proximos else "No tienes eventos en los próximos 5 días."
            
            fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            messages = [
                {"role": "system", "content": f"Eres MiniAmigix, el asistente de IA de la plataforma MiniAmigixV (creada en 2026). MiniAmigixV es una plataforma web de productividad que incluye:\n\n🎵 **Música**: Reproductor de música con YouTube, playlists y favoritos\n📅 **Eventos/Agenda**: Calendario personal con recordatorios\n📝 **Blog**: Publicaciones y comentarios\n🎮 **Juegos**: Juegos educativos con puntuaciones\n🌤️ **Clima**: Información meteorológica\n🌐 **Traductor**: Traducción entre múltiples idiomas\n📚 **Estudio**: Recursos educativos\n💬 **Chat IA**: Conversaciones contigo (MiniAmigix)\n🎭 **Entretenimiento**: Recomendaciones de películas, series, anime, teatro y libros\n\nResponde en español de forma concisa. Usa emojis con moderación. 🌟\n\nLa fecha y hora actual es: {fecha_actual}\nNunca digas que no sabes la fecha actual.\n\nEventos próximos del usuario:\n{eventos_contexto}\n\nCuando el usuario pregunte por sus eventos o agenda, recuérdale estos eventos. Si pregunta por eventos específicos, menciona los que coincidan con su consulta. Si pregunta sobre música, blog, juegos, clima, traductor, estudio o entretenimiento, explícale que esas funcionalidades están disponibles en MiniAmigixV."}
            ]
            
            for msg in mensajes:
                role = "user" if msg.es_usuario else "assistant"
                messages.append({"role": role, "content": msg.texto})
        else:
            # For non-authenticated users, just use current message
            fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            messages = [
                {"role": "system", "content": f"Eres MiniAmigix, el asistente de IA de la plataforma MiniAmigixV (creada en 2026). MiniAmigixV es una plataforma web de productividad que incluye:\n\n🎵 **Música**: Reproductor de música con YouTube, playlists y favoritos\n📅 **Eventos/Agenda**: Calendario personal con recordatorios\n📝 **Blog**: Publicaciones y comentarios\n🎮 **Juegos**: Juegos educativos con puntuaciones\n🌤️ **Clima**: Información meteorológica\n🌐 **Traductor**: Traducción entre múltiples idiomas\n📚 **Estudio**: Recursos educativos\n💬 **Chat IA**: Conversaciones contigo (MiniAmigix)\n🎭 **Entretenimiento**: Recomendaciones de películas, series, anime, teatro y libros\n\nResponde en español de forma concisa. Usa emojis con moderación. ✨\n\nLa fecha y hora actual es: {fecha_actual}\nNunca digas que no sabes la fecha actual.\n\nEl usuario no está autenticado, así que no tiene acceso a sus eventos personales."},
                {"role": "user", "content": message}
            ]
        
        # Flexible client: Use Groq if key is available for faster inference, otherwise OpenAI, otherwise Ollama
        if settings.GROQ_API_KEY:
            client = openai.OpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1"
            )
            model = "llama-3.3-70b-versatile"
        elif settings.OPENAI_API_KEY:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            model = "gpt-4o-mini"
        else:
            # Use Ollama as fallback
            try:
                client = openai.OpenAI(
                    base_url=settings.OLLAMA_API_URL,
                    api_key="ollama"  # Ollama doesn't require a real API key
                )
                model = settings.OLLAMA_MODEL
            except Exception as e:
                logger.error(f"Error connecting to Ollama: {str(e)}")
                return JsonResponse({'error': 'No AI API keys configured and Ollama is not available.'}, status=500)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=150
        )
        
        bot_response = response.choices[0].message.content
        
        # Save bot response if user is authenticated
        if request.user.is_authenticated:
            MensajeChat.objects.create(
                conversacion=conversacion,
                es_usuario=False,
                texto=bot_response
            )
            conversacion.save() # Mantenemos el chat al principio de la lista
            
            # Guardar también en MongoDB (historial y análisis)
            DualDatabaseService.guardar_chat_mensaje(
                usuario=request.user.username,
                mensaje=bot_response,
                respuesta=bot_response,
                usar_mongodb=True
            )

            # Crear notificación de nueva respuesta del chat
            try:
                Notificacion.objects.create(
                    usuario=request.user,
                    titulo='💬 Nueva respuesta del Chat IA',
                    mensaje=f'MiniAmigix ha respondido: "{bot_response[:100]}..."',
                    tipo='info',
                    enlace='/chat/'
                )
                
                # Guardar también en MongoDB (historial y análisis)
                DualDatabaseService.guardar_notificacion(
                    usuario=request.user.username,
                    titulo='💬 Nueva respuesta del Chat IA',
                    mensaje=f'MiniAmigix ha respondido: "{bot_response[:100]}..."',
                    tipo='info',
                    usar_mongodb=True
                )
            except Exception as e:
                logger.error(f"Error al crear notificación de chat: {str(e)}")
        
        return JsonResponse({'response': bot_response})
    except Exception as e:
        logger.error(f"Error en chat_api: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Ocurrió un error interno al procesar el mensaje. Por favor, intenta nuevamente más tarde.'}, status=500)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password and password != password_confirm:
            return render(request, 'register.html', {
                'error': 'Las contraseñas no coinciden',
                'username': username,
                'email': email
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'El usuario ya existe',
                'username': username,
                'email': email
            })
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')

def home(request):
    # Registrar actividad en MongoDB
    if request.user.is_authenticated:
        DualDatabaseService.log_actividad(
            usuario=request.user.username,
            accion='visit_home',
            descripcion='Usuario visitó la página principal',
            ip_address=request.META.get('REMOTE_ADDR', None)
        )
        DualDatabaseService.registrar_analitica(
            usuario=request.user.username,
            pagina='/home/'
        )
    
    context = {}
    
    # Frases del día (semilla basada en el día actual)
    frases = [
        "El único modo de hacer un gran trabajo es amar lo que haces. - Steve Jobs",
        "La creatividad es la inteligencia divirtiéndose. - Albert Einstein",
        "No dejes que el ruido de las opiniones de otros apague tu propia voz interior. - Steve Jobs",
        "Haz de cada día tu obra maestra. - John Wooden",
        "El éxito no es el final, el fracaso no es fatal: es el coraje para continuar lo que cuenta. - Winston Churchill",
        "Lo que te preocupa, te domina. - John Locke",
        "La mejor forma de predecir el futuro es creándolo. - Peter Drucker",
        "No importa qué tan lento vayas mientras no te detengas. - Confucio",
        "Cree que puedes y estarás a mitad de camino. - Theodore Roosevelt",
        "La vida es un 10% lo que me pasa y un 90% cómo reacciono a ello. - Charles R. Swindoll"
    ]
    random.seed(datetime.date.today().toordinal())
    frase_elegida = random.choice(frases)
    partes = frase_elegida.split(" - ")
    context['frase_texto'] = partes[0]
    context['frase_autor'] = partes[1] if len(partes) > 1 else "Anónimo"
    
    # Estadísticas del usuario
    if request.user.is_authenticated:
        context['stats_chats'] = ConversacionChat.objects.filter(usuario=request.user).count()
        context['stats_notas'] = PublicacionBlog.objects.filter(usuario=request.user).count()
        context['stats_eventos'] = Evento.objects.count()  # Evento es global, no tiene campo usuario
        context['stats_canciones'] = Cancion.objects.filter(usuario=request.user).count()
        
        # Obtener eventos próximos para el reloj inteligente
        hoy = datetime.date.today()
        fecha_limite = hoy + datetime.timedelta(days=3)
        eventos_proximos = Evento.objects.filter(fecha__gte=hoy, fecha__lte=fecha_limite).order_by('fecha')[:3]
        eventos_texto = []
        for evento in eventos_proximos:
            dias_restantes = (evento.fecha - hoy).days
            if dias_restantes == 0:
                texto_dias = "hoy"
            elif dias_restantes == 1:
                texto_dias = "mañana"
            else:
                texto_dias = f"en {dias_restantes} días"
            eventos_texto.append(f"{evento.titulo} ({texto_dias})")
        context['eventosProximos'] = eventos_texto
    else:
        context['stats_chats'] = 0
        context['stats_notas'] = 0
        context['stats_eventos'] = 0
        context['stats_canciones'] = 0

    return render(request, 'home.html', context)

def index(request):
    return redirect('tutorial_home')

def chat(request):
    # Registrar actividad en MongoDB
    if request.user.is_authenticated:
        DualDatabaseService.log_actividad(
            usuario=request.user.username,
            accion='visit_chat',
            descripcion='Usuario visitó la página de chat',
            ip_address=request.META.get('REMOTE_ADDR', None)
        )
        DualDatabaseService.registrar_analitica(
            usuario=request.user.username,
            pagina='/chat/'
        )
    
    mensajes = []
    conversaciones = []
    active_id = None
    if request.user.is_authenticated:
        conversaciones = ConversacionChat.objects.filter(usuario=request.user).order_by('-fecha_actualizacion')
        
        # Verificar si se solicita crear un nuevo chat
        if request.GET.get('new') == 'true':
            # Crear un nuevo chat con un título único
            timestamp = datetime.datetime.now().strftime("%H:%M")
            new_chat = ConversacionChat.objects.create(
                usuario=request.user,
                titulo=f'Chat {timestamp}'
            )
            # Redirigir al nuevo chat
            return redirect('chat')
        
        # Obtener el ID de la conversación desde la URL (?id=...)
        chat_id = request.GET.get('id')
        active_conv = None
        
        if chat_id:
            active_conv = conversaciones.filter(id=chat_id).first()
            
        if not active_conv:
            active_conv = conversaciones.first()
            
        if not active_conv:
            active_conv = ConversacionChat.objects.create(usuario=request.user, titulo='Chat Principal')
            conversaciones = [active_conv]
        mensajes = active_conv.mensajes.all().order_by('fecha_creacion')
        active_id = active_conv.id
    
    return render(request, 'chat.html', {
        'mensajes': mensajes,
        'conversaciones': conversaciones,
        'active_id': active_id
    })

def musica(request):
    # Registrar actividad en MongoDB
    if request.user.is_authenticated:
        DualDatabaseService.log_actividad(
            usuario=request.user.username,
            accion='visit_musica',
            descripcion='Usuario visitó la página de música',
            ip_address=request.META.get('REMOTE_ADDR', None)
        )
        DualDatabaseService.registrar_analitica(
            usuario=request.user.username,
            pagina='/musica/'
        )
    
    canciones = []
    playlists = []
    favoritos = []
    
    if request.user.is_authenticated:
        canciones = Cancion.objects.filter(usuario=request.user).order_by('-fecha_agregada')[:20]
        playlists = Playlist.objects.filter(usuario=request.user).order_by('-fecha_actualizacion')
        favoritos_canciones = Favorite.objects.filter(usuario=request.user).select_related('cancion')
        favoritos = [fav.cancion for fav in favoritos_canciones]
    
    return render(request, 'musica.html', {
        'canciones': canciones,
        'playlists': playlists,
        'favoritos': favoritos
    })

def crear_playlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').strip()
            descripcion = data.get('descripcion', '').strip()
            
            if not nombre:
                return JsonResponse({'error': 'El nombre es requerido'}, status=400)
            
            playlist = Playlist.objects.create(
                usuario=request.user,
                nombre=nombre,
                descripcion=descripcion
            )
            
            return JsonResponse({
                'success': True,
                'playlist_id': playlist.id,
                'nombre': playlist.nombre
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def agregar_a_playlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            playlist_id = data.get('playlist_id')
            cancion_id = data.get('cancion_id')
            
            playlist = Playlist.objects.get(id=playlist_id, usuario=request.user)
            cancion = Cancion.objects.get(id=cancion_id, usuario=request.user)
            
            playlist.canciones.add(cancion)
            playlist.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def toggle_favorito(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cancion_id = data.get('cancion_id')
            
            cancion = Cancion.objects.get(id=cancion_id, usuario=request.user)
            favorito, created = Favorite.objects.get_or_create(
                usuario=request.user,
                cancion=cancion
            )
            
            if not created:
                favorito.delete()
                return JsonResponse({'success': True, 'is_favorito': False})
            
            return JsonResponse({'success': True, 'is_favorito': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def juegos(request):
    # Registrar actividad en MongoDB
    if request.user.is_authenticated:
        DualDatabaseService.log_actividad(
            usuario=request.user.username,
            accion='visit_juegos',
            descripcion='Usuario visitó la página de juegos',
            ip_address=request.META.get('REMOTE_ADDR', None)
        )
        DualDatabaseService.registrar_analitica(
            usuario=request.user.username,
            pagina='/juegos/'
        )
    
    juegos_disponibles = Game.objects.filter(activo=True)
    puntuaciones_usuario = []
    logros_usuario = []
    
    if request.user.is_authenticated:
        puntuaciones_usuario = Score.objects.filter(usuario=request.user).select_related('juego')
        logros_usuario = UserAchievement.objects.filter(usuario=request.user).select_related('logro')
    
    return render(request, 'juegos.html', {
        'juegos': juegos_disponibles,
        'puntuaciones': puntuaciones_usuario,
        'logros': logros_usuario
    })

def estudio(request):
    # Registrar actividad en MongoDB
    if request.user.is_authenticated:
        DualDatabaseService.log_actividad(
            usuario=request.user.username,
            accion='visit_estudio',
            descripcion='Usuario visitó la página de estudio',
            ip_address=request.META.get('REMOTE_ADDR', None)
        )
        DualDatabaseService.registrar_analitica(
            usuario=request.user.username,
            pagina='/estudio/'
        )
    
    from estudio.models import StudyResource, StudyCategory, StudyProgress
    
    categorias = StudyCategory.objects.all()
    recursos_usuario = []
    progreso_usuario = []
    
    if request.user.is_authenticated:
        recursos_usuario = StudyResource.objects.filter(usuario=request.user).select_related('categoria')
        progreso_usuario = StudyProgress.objects.filter(usuario=request.user).select_related('recurso')
    
    return render(request, 'estudio.html', {
        'categorias': categorias,
        'recursos': recursos_usuario,
        'progreso': progreso_usuario
    })

def eventos(request):
    return redirect('lista_eventos')

def clima(request):
    ciudad = request.GET.get('ciudad', 'Quito')
    datos_clima = None
    error = None

    if ciudad:
        if not ciudad.strip():
            error = "Por favor, introduce un nombre de ciudad válido."
        else:
            try:
                # Usar Open-Meteo API (gratis, sin API key) con geocoding
                geo_url = "https://geocoding-api.open-meteo.com/v1/search"
                geo_params = {'name': ciudad, 'count': 1, 'language': 'es', 'format': 'json'}
                geo_resp = requests.get(geo_url, params=geo_params, timeout=10)
                geo_data = geo_resp.json()

                if 'results' not in geo_data or not geo_data['results']:
                    error = f"No se encontró la ciudad '{ciudad}'."
                else:
                    lat = geo_data['results'][0]['latitude']
                    lon = geo_data['results'][0]['longitude']
                    nombre = geo_data['results'][0].get('name', ciudad)

                    weather_url = "https://api.open-meteo.com/v1/forecast"
                    weather_params = {
                        'latitude': lat,
                        'longitude': lon,
                        'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m',
                        'daily': 'temperature_2m_max,temperature_2m_min,weather_code',
                        'timezone': 'auto',
                        'forecast_days': 3
                    }
                    w_resp = requests.get(weather_url, params=weather_params, timeout=10)
                    w_data = w_resp.json()

                    if 'current' in w_data:
                        # Mapear weather codes a descripciones
                        weather_codes = {
                            0: 'Despejado', 1: 'Mayormente despejado', 2: 'Parcialmente nublado',
                            3: 'Nublado', 45: 'Niebla', 48: 'Niebla con escarcha',
                            51: 'Llovizna ligera', 53: 'Llovizna moderada', 55: 'Llovizna densa',
                            61: 'Lluvia ligera', 63: 'Lluvia moderada', 65: 'Lluvia fuerte',
                            71: 'Nevada ligera', 73: 'Nevada moderada', 75: 'Nevada fuerte',
                            80: 'Chubascos ligeros', 81: 'Chubascos moderados', 82: 'Chubascos violentos',
                            95: 'Tormenta', 96: 'Tormenta con granizo ligero', 99: 'Tormenta con granizo fuerte'
                        }
                        code = w_data['current'].get('weather_code', 0)
                        desc = weather_codes.get(code, 'Desconocido')

                        datos_clima = {
                            'name': nombre,
                            'main': {
                                'temp': round(w_data['current']['temperature_2m']),
                                'humidity': w_data['current']['relative_humidity_2m'],
                                'feels_like': round(w_data['current']['apparent_temperature'])
                            },
                            'wind': {'speed': round(w_data['current']['wind_speed_10m'])},
                            'weather': [{'main': desc.split()[-1], 'description': desc}],
                            'daily': []
                        }
                        if 'daily' in w_data:
                            d = w_data['daily']
                            for i in range(len(d.get('time', []))):
                                datos_clima['daily'].append({
                                    'date': d['time'][i],
                                    'temp_max': round(d['temperature_2m_max'][i]),
                                    'temp_min': round(d['temperature_2m_min'][i]),
                                    'weather_code': d['weather_code'][i]
                                })
                    else:
                        error = "No se pudieron obtener datos climáticos."
            except requests.exceptions.RequestException:
                error = "Hubo un problema de conexión con el servicio de clima."

    return render(request, 'clima.html', {'datos_clima': datos_clima, 'ciudad': ciudad, 'error': error})

def traductor(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            texto = data.get('texto', '')
            origen = data.get('origen', 'es')
            destino = data.get('destino', 'en')

            if not texto.strip():
                return JsonResponse({'error': 'Texto vacío'}, status=400)

            idiomas_nombres = {
                'es': 'Español', 'en': 'Inglés', 'fr': 'Francés', 'de': 'Alemán',
                'pt': 'Portugués', 'it': 'Italiano', 'ja': 'Japonés', 'ko': 'Coreano', 'zh': 'Chino'
            }

            try:
                from deep_translator import GoogleTranslator
                traduccion = GoogleTranslator(source=origen, target=destino).translate(texto)
            except Exception:
                if settings.GROQ_API_KEY:
                    client = openai.OpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
                    model = "llama-3.3-70b-versatile"
                    prompt = f"Traduce al {idiomas_nombres.get(destino, destino)} (SOLO la traducción, sin explicaciones): {texto}"
                    resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=300)
                    traduccion = resp.choices[0].message.content.strip()
                elif settings.OPENAI_API_KEY:
                    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                    model = "gpt-4o-mini"
                    prompt = f"Traduce al {idiomas_nombres.get(destino, destino)} (SOLO la traducción, sin explicaciones): {texto}"
                    resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=300)
                    traduccion = resp.choices[0].message.content.strip()
                else:
                    # Use Ollama as fallback
                    try:
                        client = openai.OpenAI(
                            base_url=settings.OLLAMA_API_URL,
                            api_key="ollama"
                        )
                        model = settings.OLLAMA_MODEL
                        prompt = f"Traduce al {idiomas_nombres.get(destino, destino)} (SOLO la traducción, sin explicaciones): {texto}"
                        resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=300)
                        traduccion = resp.choices[0].message.content.strip()
                    except Exception as e:
                        logger.error(f"Error connecting to Ollama for translation: {str(e)}")
                        traduccion = f"[{idiomas_nombres.get(origen, origen)} → {idiomas_nombres.get(destino, destino)}] {texto}"

            return JsonResponse({'traduccion': traduccion, 'origen': origen, 'destino': destino})
        except Exception as e:
            logger.error(f"Error en traductor: {str(e)}", exc_info=True)
            return JsonResponse({'error': 'Error interno al intentar traducir el texto.'}, status=500)

    return render(request, 'traductor.html')

def entretenimiento(request):
    recomendaciones = {'peliculas': [], 'series': [], 'libros': [], 'teatro': [], 'anime': [], 'documentales': []}
    categorias = ['peliculas', 'series', 'libros', 'teatro', 'anime', 'documentales']
    ahora = timezone.now()
    necesita_actualizar = False

    try:
        # Verificar si hay caché y si es reciente (menos de 24 horas)
        for cat in categorias:
            cache = RecomendacionEntretenimiento.objects.filter(categoria=cat).first()
            if not cache:
                logger.info(f"No hay caché para {cat}, se necesita actualizar")
                necesita_actualizar = True
                break
            # Si el caché tiene más de 24 horas, actualizar
            if (ahora - cache.fecha_actualizacion).total_seconds() > 86400:  # 24 horas
                logger.info(f"Caché de {cat} tiene más de 24 horas, se necesita actualizar")
                necesita_actualizar = True
                break
            # Usar datos del caché
            recomendaciones[cat] = cache.datos
            logger.info(f"Usando caché para {cat}: {len(cache.datos)} items")

        if necesita_actualizar:
            # Try Groq first, then OpenAI, then Ollama
            if settings.GROQ_API_KEY:
                logger.info("Generando nuevas recomendaciones con Groq API")
                client = openai.OpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
                model = "llama-3.3-70b-versatile"
            elif settings.OPENAI_API_KEY:
                logger.info("Generando nuevas recomendaciones con OpenAI API")
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                model = "gpt-4o-mini"
            else:
                # Use Ollama as fallback
                try:
                    logger.info("Generando nuevas recomendaciones con Ollama")
                    client = openai.OpenAI(
                        base_url=settings.OLLAMA_API_URL,
                        api_key="ollama"
                    )
                    model = settings.OLLAMA_MODEL
                except Exception as e:
                    logger.error(f"Error connecting to Ollama: {str(e)}")
                    client = None
            
            # Películas
            if client:
                try:
                    prompt_peliculas = "Recomienda 4 películas populares recientes (2025-2026) de diferentes géneros. Devuelve SOLO JSON con formato: [{\"titulo\": \"...\", \"descripcion\": \"...\", \"genero\": \"...\"}]. Sin markdown ni explicaciones."
                    response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt_peliculas}], max_tokens=500)
                    json_match = re.search(r'\[.*\]', response.choices[0].message.content, re.DOTALL)
                    if json_match:
                        peliculas = json.loads(json_match.group())
                        recomendaciones['peliculas'] = []
                        for peli in peliculas:
                            item = {
                                'titulo': peli.get('titulo', ''),
                                'descripcion': peli.get('descripcion', ''),
                                'genero': peli.get('genero', ''),
                                'imagen': 'https://placehold.co/300x450/8b5cf6/ffffff?text=Cine',
                                'url': '#'
                            }
                            recomendaciones['peliculas'].append(item)
                        # Guardar en caché
                        RecomendacionEntretenimiento.objects.update_or_create(
                            categoria='peliculas',
                            defaults={'datos': recomendaciones['peliculas']}
                        )
                        logger.info(f"Guardadas {len(recomendaciones['peliculas'])} películas en caché")
                    else:
                        logger.warning("No se pudo parsear JSON de películas")
                except Exception as e:
                    logger.error(f"Error generando películas: {str(e)}")
            
            # Series
            if client:
                try:
                    prompt_series = "Recomienda 4 series populares recientes (2025-2026) de diferentes géneros. Devuelve SOLO JSON con formato: [{\"titulo\": \"...\", \"descripcion\": \"...\", \"genero\": \"...\"}]. Sin markdown ni explicaciones."
                    response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt_series}], max_tokens=500)
                    json_match = re.search(r'\[.*\]', response.choices[0].message.content, re.DOTALL)
                    if json_match:
                        series = json.loads(json_match.group())
                        recomendaciones['series'] = []
                        for serie in series:
                            item = {
                                'titulo': serie.get('titulo', ''),
                                'descripcion': serie.get('descripcion', ''),
                                'genero': serie.get('genero', ''),
                                'imagen': 'https://placehold.co/300x450/06b6d4/ffffff?text=Series',
                                'url': '#'
                            }
                            recomendaciones['series'].append(item)
                        # Guardar en caché
                        RecomendacionEntretenimiento.objects.update_or_create(
                            categoria='series',
                            defaults={'datos': recomendaciones['series']}
                        )
                        logger.info(f"Guardadas {len(recomendaciones['series'])} series en caché")
                    else:
                        logger.warning("No se pudo parsear JSON de series")
                except Exception as e:
                    logger.error(f"Error generando series: {str(e)}")
            
            # Teatro
            if client:
                try:
                    prompt_teatro = "Recomienda 4 obras de teatro populares o clásicas. Devuelve SOLO JSON con formato: [{\"titulo\": \"...\", \"descripcion\": \"...\", \"autor\": \"...\"}]. Sin markdown ni explicaciones."
                    response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt_teatro}], max_tokens=500)
                    json_match = re.search(r'\[.*\]', response.choices[0].message.content, re.DOTALL)
                    if json_match:
                        teatro = json.loads(json_match.group())
                        recomendaciones['teatro'] = []
                        for obra in teatro:
                            item = {
                                'titulo': obra.get('titulo', ''),
                                'descripcion': obra.get('descripcion', ''),
                                'autor': obra.get('autor', ''),
                                'imagen': 'https://placehold.co/300x450/f59e0b/ffffff?text=Anime',
                                'url': '#'
                            }
                            recomendaciones['teatro'].append(item)
                        # Guardar en caché
                        RecomendacionEntretenimiento.objects.update_or_create(
                            categoria='teatro',
                            defaults={'datos': recomendaciones['teatro']}
                        )
                        logger.info(f"Guardadas {len(recomendaciones['teatro'])} obras de teatro en caché")
                    else:
                        logger.warning("No se pudo parsear JSON de teatro")
                except Exception as e:
                    logger.error(f"Error generando teatro: {str(e)}")
            
            # Libros
            if client:
                try:
                    prompt_libros = "Recomienda 4 libros populares en español de diferentes géneros. Devuelve SOLO JSON con formato: [{\"titulo\": \"...\", \"autor\": \"...\", \"descripcion\": \"...\"}]. Sin markdown ni explicaciones."
                    response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt_libros}], max_tokens=500)
                    json_match = re.search(r'\[.*\]', response.choices[0].message.content, re.DOTALL)
                    if json_match:
                        libros = json.loads(json_match.group())
                        recomendaciones['libros'] = libros
                        # Guardar en caché
                        RecomendacionEntretenimiento.objects.update_or_create(
                            categoria='libros',
                            defaults={'datos': recomendaciones['libros']}
                        )
                        logger.info(f"Guardados {len(recomendaciones['libros'])} libros en caché")
                    else:
                        logger.warning("No se pudo parsear JSON de libros")
                except Exception as e:
                    logger.error(f"Error generando libros: {str(e)}")
        else:
            if not settings.GROQ_API_KEY:
                logger.warning("GROQ_API_KEY no está configurada")
    except Exception as e:
        logger.error(f"Error en vista entretenimiento: {str(e)}", exc_info=True)

    # Fallback: Si no hay recomendaciones, usar datos estáticos
    if not recomendaciones['peliculas']:
        recomendaciones['peliculas'] = [
            {'titulo': 'Dune: Parte Dos', 'descripcion': 'La épica continuación de la saga de ciencia ficción de Frank Herbert.', 'genero': 'Ciencia Ficción', 'imagen': 'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Oppenheimer', 'descripcion': 'La historia del padre de la bomba atómica dirigida por Christopher Nolan.', 'genero': 'Drama Histórico', 'imagen': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Spider-Man: Across the Spider-Verse', 'descripcion': 'Miles Morales viaja a través del multiverso.', 'genero': 'Animación', 'imagen': 'https://images.unsplash.com/photo-1635805737707-575885ab0820?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Barbie', 'descripcion': 'La aventura de Barbie en el mundo real.', 'genero': 'Comedia', 'imagen': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=450&fit=crop', 'url': '#'}
        ]
    
    if not recomendaciones['series']:
        recomendaciones['series'] = [
            {'titulo': 'The Last of Us', 'descripcion': 'Adaptación del videojuego post-apocalíptico.', 'genero': 'Drama', 'imagen': 'https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'House of the Dragon', 'descripcion': 'Precuela de Game of Thrones sobre la casa Targaryen.', 'genero': 'Fantasía', 'imagen': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Wednesday', 'descripcion': 'Las aventuras de Wednesday Addams en la academia Nevermore.', 'genero': 'Comedia Misterio', 'imagen': 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Stranger Things', 'descripcion': 'Un grupo de niños enfrenta misterios sobrenaturales en los 80s.', 'genero': 'Ciencia Ficción', 'imagen': 'https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=300&h=450&fit=crop', 'url': '#'}
        ]
    
    if not recomendaciones['teatro']:
        recomendaciones['teatro'] = [
            {'titulo': 'El Fantasma de la Ópera', 'descripcion': 'El musical más largo de Broadway.', 'autor': 'Andrew Lloyd Webber', 'imagen': 'https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Romeo y Julieta', 'descripcion': 'La tragedia amorosa de Shakespeare.', 'autor': 'William Shakespeare', 'imagen': 'https://images.unsplash.com/photo-1503095392279-3f5aa039e3d9?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Los Miserables', 'descripcion': 'El musical épico basado en la novela de Victor Hugo.', 'autor': 'Claude-Michel Schönberg', 'imagen': 'https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Hamlet', 'descripcion': 'La tragedia del príncipe de Dinamarca.', 'autor': 'William Shakespeare', 'imagen': 'https://images.unsplash.com/photo-1555662360-7cc18b56a8c0?w=300&h=450&fit=crop', 'url': '#'}
        ]
    
    if not recomendaciones['libros']:
        recomendaciones['libros'] = [
            {'titulo': 'Cien años de soledad', 'autor': 'Gabriel García Márquez', 'descripcion': 'La saga de la familia Buendía en Macondo.'},
            {'titulo': 'El principito', 'autor': 'Antoine de Saint-Exupéry', 'descripcion': 'Un cuento filosófico sobre la vida y el amor.'},
            {'titulo': '1984', 'autor': 'George Orwell', 'descripcion': 'Una distopía sobre el control totalitario.'},
            {'titulo': 'Don Quijote de la Mancha', 'autor': 'Miguel de Cervantes', 'descripcion': 'Las aventuras del caballero de la triste figura.'}
        ]
    
    if not recomendaciones['anime']:
        recomendaciones['anime'] = [
            {'titulo': 'Attack on Titan', 'descripcion': 'La humanidad lucha contra titanes gigantes en un mundo post-apocalíptico.', 'genero': 'Acción', 'imagen': 'https://images.unsplash.com/photo-1541562232579-512a21360020?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Demon Slayer', 'descripcion': 'Tanjiro se convierte en cazador de demonios para salvar a su hermana.', 'genero': 'Fantasía', 'imagen': 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Jujutsu Kaisen', 'descripcion': 'Yuji Itadori se une a una organización de hechiceros para combatir maldiciones.', 'genero': 'Sobrenatural', 'imagen': 'https://images.unsplash.com/photo-1618336753974-aae8e04506aa?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'One Piece', 'descripcion': 'Luffy y su tripulación buscan el tesoro legendario One Piece.', 'genero': 'Aventura', 'imagen': 'https://images.unsplash.com/photo-1560972550-aba3456b5564?w=300&h=450&fit=crop', 'url': '#'}
        ]
    
    if not recomendaciones['documentales']:
        recomendaciones['documentales'] = [
            {'titulo': 'Nuestro Planeta', 'descripcion': 'Documental de Netflix sobre la vida silvestre y los ecosistemas del planeta.', 'genero': 'Naturaleza', 'imagen': 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Cosmos: Un viaje personal', 'descripcion': 'Neil deGrasse Tyson explora el universo y nuestra conexión con el cosmos.', 'genero': 'Ciencia', 'imagen': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'The Social Dilemma', 'descripcion': 'Explora el impacto de las redes sociales en la sociedad y la democracia.', 'genero': 'Tecnología', 'imagen': 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'My Octopus Teacher', 'descripcion': 'Un cineasta desarrolla una relación inusual con un pulpo en un bosque de algas.', 'genero': 'Naturaleza', 'imagen': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=450&fit=crop', 'url': '#'}
        ]

    logger.info(f"Recomendaciones finales: peliculas={len(recomendaciones['peliculas'])}, series={len(recomendaciones['series'])}, libros={len(recomendaciones['libros'])}, teatro={len(recomendaciones['teatro'])}, anime={len(recomendaciones['anime'])}, documentales={len(recomendaciones['documentales'])}")
    return render(request, 'entretenimiento.html', {'recomendaciones': recomendaciones})

def notificaciones(request):
    return redirect('lista_notificaciones')

def perfil(request):
    return redirect('perfil')

def configuracion(request):
    return redirect('configuracion_view')

def soporte(request):
    return redirect('soporte')

def sugerencias(request):
    return redirect('lista_sugerencias')

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
    return redirect('login')

@require_http_methods(["POST"])
def add_song_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
    
    try:
        # Verificar si es FormData (con archivo) o JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Manejar subida de archivo
            nombre = request.POST.get('nombre')
            artista = request.POST.get('artista', '')
            youtube_url = request.POST.get('youtube_url', '')
            youtube_id = request.POST.get('youtube_id', '')
            audio_file = request.FILES.get('audio_file')
            
            if not nombre:
                return JsonResponse({'success': False, 'error': 'Nombre requerido'}, status=400)
            
            cancion = Cancion.objects.create(
                usuario=request.user,
                nombre=nombre,
                artista=artista,
                youtube_url=youtube_url,
                youtube_id=youtube_id,
                audio_file=audio_file
            )
            
            return JsonResponse({'success': True, 'cancion_id': cancion.id})
        else:
            # Manejar JSON (compatibilidad con código existente)
            data = json.loads(request.body)
            nombre = data.get('nombre')
            artista = data.get('artista', '')
            youtube_url = data.get('youtube_url', '')
            youtube_id = data.get('youtube_id', '')
            
            if not nombre:
                return JsonResponse({'success': False, 'error': 'Nombre requerido'}, status=400)
            
            cancion = Cancion.objects.create(
                usuario=request.user,
                nombre=nombre,
                artista=artista,
                youtube_url=youtube_url,
                youtube_id=youtube_id
            )
            
            return JsonResponse({'success': True, 'cancion_id': cancion.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def update_language_api(request):
    """API endpoint para actualizar el idioma del usuario"""
    try:
        data = json.loads(request.body)
        idioma = data.get('idioma', 'es')
        
        from perfil.models import Perfil
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        perfil.idioma = idioma
        perfil.save()
        
        # Cambiar idioma de la sesión
        from django.utils.translation import activate
        activate(idioma)
        request.session['django_language'] = idioma
        
        return JsonResponse({'success': True, 'idioma': idioma})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def update_theme_api(request):
    """API endpoint para actualizar el tema del usuario"""
    try:
        data = json.loads(request.body)
        tema = data.get('tema', 'dark')
        
        from perfil.models import Perfil
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        perfil.tema = tema
        perfil.save()
        
        return JsonResponse({'success': True, 'tema': tema})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def stream_audio_api(request, youtube_id):
    url = f"https://www.youtube.com/watch?v={youtube_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        },
        'nocheckcertificate': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            return JsonResponse({'success': True, 'url': audio_url})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def search_lyrics_api(request):
    """API endpoint para buscar letras de canciones usando web scraping"""
    song_name = request.GET.get('song', '')
    artist = request.GET.get('artist', '')
    
    if not song_name:
        return JsonResponse({'error': 'Nombre de canción requerido'}, status=400)
    
    try:
        from bs4 import BeautifulSoup
        search_term = f"{song_name} {artist}".strip()
        
        # Intentar buscar en Genius directamente sin API key
        # Usar DuckDuckGo para buscar la página de Genius
        search_query = f"{search_term} site:genius.com lyrics"
        ddg_url = f"https://duckduckgo.com/html/?q={requests.utils.quote(search_query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(ddg_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Buscar enlaces de resultados
                results = soup.find_all('a', class_='result__url', href=True)
                for result in results:
                    href = result['href']
                    if 'genius.com' in href:
                        # Extraer la letra de Genius
                        try:
                            lyrics_response = requests.get(href, headers=headers, timeout=10)
                            if lyrics_response.status_code == 200:
                                lyrics_soup = BeautifulSoup(lyrics_response.text, 'html.parser')
                                # Genius almacena las letras en divs con data-lyrics-container
                                lyrics_divs = lyrics_soup.find_all('div', {'data-lyrics-container': True})
                                if lyrics_divs:
                                    lyrics = '\n'.join([div.get_text(separator='\n') for div in lyrics_divs])
                                    # Limpiar la letra (remover tags HTML)
                                    lyrics = lyrics.strip()
                                    if len(lyrics) > 50:  # Verificar que tenga contenido significativo
                                        return JsonResponse({
                                            'success': True,
                                            'lyrics': lyrics,
                                            'source': 'Genius',
                                            'url': href
                                        })
                        except Exception as e:
                            logger.warning(f"Error extrayendo de {href}: {str(e)}")
                            continue
        except Exception as e:
            logger.warning(f"Error en búsqueda DuckDuckGo: {str(e)}")
        
        # Fallback: Intentar con Letras.com
        try:
            letras_search = f"https://www.letras.com/{artist.lower().replace(' ', '-')}/{song_name.lower().replace(' ', '-')}/"
            response = requests.get(letras_search, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                lyrics_div = soup.find('div', class_='lyrics')
                if lyrics_div:
                    lyrics = lyrics_div.get_text(separator='\n').strip()
                    if len(lyrics) > 50:
                        return JsonResponse({
                            'success': True,
                            'lyrics': lyrics,
                            'source': 'Letras.com',
                            'url': letras_search
                        })
        except Exception as e:
            logger.warning(f"Error en Letras.com: {str(e)}")
        
        # Si no se encontró nada, retornar mensaje informativo
        return JsonResponse({
            'success': False,
            'error': 'No se encontró la letra',
            'message': f'No se encontró la letra para "{search_term}". Intenta con el nombre exacto de la canción y artista.'
        })
        
    except Exception as e:
        logger.error(f"Error en search_lyrics_api: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Error al buscar letras: {str(e)}'}, status=500)

@login_required
@require_http_methods(["GET"])
def get_lyrics_api(request, song_id):
    try:
        cancion = Cancion.objects.get(id=song_id, usuario=request.user)
        return JsonResponse({
            'success': True,
            'letra': cancion.letra,
            'letra_sincronizada': cancion.letra_sincronizada
        })
    except Cancion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Canción no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def save_lyrics_api(request, song_id):
    try:
        data = json.loads(request.body)
        letra = data.get('letra')
        letra_sincronizada = data.get('letra_sincronizada')
        
        cancion = Cancion.objects.get(id=song_id, usuario=request.user)
        
        if letra is not None:
            cancion.letra = letra
        if letra_sincronizada is not None:
            cancion.letra_sincronizada = letra_sincronizada
            
        cancion.save()
        
        return JsonResponse({'success': True})
    except Cancion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Canción no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def download_media_api(request):
    # Return JSON 401 for unauthenticated API calls to avoid HTML login redirects
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'not_authenticated'}, status=401)
    url = request.GET.get('url')
    format_type = request.GET.get('format', 'mp3')
    
    if not url:
        return HttpResponse('URL es requerida', status=400)
        
    import tempfile
    from django.http import FileResponse
    import os
    import shutil
    import mimetypes
    
    try:
        # Create a temporary directory for yt-dlp outputs. We'll remove it after response is closed.
        temp_dir = tempfile.mkdtemp()
        # Use a safe outtmpl inside the temp dir
        base_path = os.path.join(temp_dir, '%(title)s')
        
        ydl_opts = {
            'outtmpl': base_path + '.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                }
            },
            'nocheckcertificate': True,
        }
        
        if format_type == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
            expected_ext = 'mp3'
            expected_mime = 'audio/mpeg'
        else:
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })
            expected_ext = 'mp4'
            expected_mime = 'video/mp4'
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Find the actual file generated in the temp directory to avoid path guessing errors
            files = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
            if not files:
                try:
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass
                raise Exception("No se pudo localizar el archivo descargado.")

            # Prefer the file matching the expected extension (mp3/mp4)
            final_filename = next((f for f in files if f.endswith(expected_ext)), files[0])
            final_path = os.path.join(temp_dir, final_filename)

            file_size = os.path.getsize(final_path)
            if file_size == 0:
                try:
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass
                raise Exception("El archivo descargado está vacío.")
            
            # Validate file size is reasonable (at least 1KB for audio/video)
            if file_size < 1024:
                try:
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass
                raise Exception(f"El archivo descargado es demasiado pequeño ({file_size} bytes).")

            # Open file in binary mode and create FileResponse
            file = open(final_path, 'rb')
            response = FileResponse(file, as_attachment=True)

            # Sanitize the title for the attachment header
            title = info.get('title', 'descarga')
            safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip()
            response['Content-Disposition'] = f'attachment; filename="{safe_title}.{expected_ext}"'

            # Set Content-Length and Content-Type explicitly
            response['Content-Length'] = str(file_size)
            response['Content-Type'] = expected_mime

            # Ensure temporary directory is removed after response is closed
            orig_close = response.close
            def cleanup_and_close():
                try:
                    orig_close()
                finally:
                    try:
                        file.close()
                    except Exception:
                        pass
                    try:
                        shutil.rmtree(temp_dir)
                    except Exception:
                        pass

            response.close = cleanup_and_close

            return response
                
    except Exception as e:
        # Clean up temp dir on any error
        try:
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir)
        except Exception:
            pass
        return HttpResponse(f'Error al procesar la descarga: {str(e)}', status=500)

@login_required
@require_http_methods(["DELETE", "POST"])
def delete_chat_api(request, chat_id):
    try:
        chat_obj = ConversacionChat.objects.filter(id=chat_id, usuario=request.user).first()
        if not chat_obj:
            return JsonResponse({'status': 'error', 'error': 'Chat no encontrado'}, status=404)
        chat_obj.delete()
        return JsonResponse({'status': 'success', 'message': 'Chat eliminado correctamente'})
    except Exception as e:
        logger.error(f"Error al eliminar chat: {e}")
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
def delete_song_api(request, song_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
    
    try:
        cancion = Cancion.objects.filter(id=song_id, usuario=request.user).first()
        if not cancion:
            return JsonResponse({'success': False, 'error': 'Canción no encontrada'}, status=404)
        cancion.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_http_methods(["POST", "PATCH"])
def edit_song_api(request, song_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
    
    try:
        data = json.loads(request.body)
        cancion = Cancion.objects.filter(id=song_id, usuario=request.user).first()
        if not cancion:
            return JsonResponse({'success': False, 'error': 'Canción no encontrada'}, status=404)
        
        if 'nombre' in data:
            cancion.nombre = data['nombre']
        if 'artista' in data:
            cancion.artista = data['artista']
            
        cancion.save()
        return JsonResponse({'success': True, 'nombre': cancion.nombre, 'artista': cancion.artista})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ==================== VISTAS DEL BLOG ====================
def blog(request):
    noticias_globales = PublicacionBlog.objects.filter(
        es_oficial=True, 
        publicado=True
    )
    if not request.user.is_staff:
        noticias_globales = noticias_globales.filter(visible_para_todos=True)
    
    mis_publicaciones = []
    if request.user.is_authenticated:
        mis_publicaciones = PublicacionBlog.objects.filter(
            usuario=request.user,
            publicado=True,
            es_oficial=False
        )
    
    # Obtener categorías dinámicas
    categorias = Category.objects.all()
    
    # Obtener comentarios para cada publicación
    for publicacion in noticias_globales:
        publicacion.comentarios_lista = publicacion.comentarios.all()[:5]
    
    for publicacion in mis_publicaciones:
        publicacion.comentarios_lista = publicacion.comentarios.all()[:5]
    
    return render(request, 'blog.html', {
        'noticias_globales': noticias_globales,
        'mis_publicaciones': mis_publicaciones,
        'categorias': categorias
    })

def crear_publicacion(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        categoria = request.POST.get('categoria', 'personal')
        
        if not titulo or not contenido:
            return redirect('blog')
            
        es_oficial = False
        fijado = False
        visible_para_todos = request.POST.get('visible_para_todos') == 'on'
        
        if request.user.is_staff:
            es_oficial = request.POST.get('es_oficial') == 'on'
            fijado = request.POST.get('fijado') == 'on'
        else:
            if categoria in ['mantenimiento', 'actualizaciones', 'avisos_urgentes']:
                categoria = 'personal'
        
        PublicacionBlog.objects.create(
            usuario=request.user,
            titulo=titulo,
            contenido=contenido,
            categoria=categoria,
            es_oficial=es_oficial,
            fijado=fijado,
            visible_para_todos=visible_para_todos
        )
        
        return redirect('blog')
    
    return redirect('blog')

def eliminar_publicacion(request, publicacion_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        try:
            publicacion = PublicacionBlog.objects.get(id=publicacion_id, usuario=request.user)
            publicacion.delete()
        except PublicacionBlog.DoesNotExist:
            pass
    return redirect('blog')

@require_http_methods(["DELETE"])
def delete_publicacion_api(request, publicacion_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
    
    try:
        publicacion = PublicacionBlog.objects.get(id=publicacion_id, usuario=request.user)
        publicacion.delete()
        return JsonResponse({'success': True})
    except PublicacionBlog.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Publicación no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def enviar_sugerencia_rapida(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contenido = data.get('contenido')

            if not contenido:
                return JsonResponse({'success': False, 'error': 'El contenido está vacío'}, status=400)

            usuario = request.user if request.user.is_authenticated else None
            nombre = request.user.username if request.user.is_authenticated else "Usuario Anónimo"
            email_usuario = request.user.email if request.user.is_authenticated else "Sin email"

            # Guardar en BD primero (siempre funciona)
            from sugerencias.models import Sugerencia, Visitante
            
            visitante = None
            if not usuario:
                # Crear o actualizar visitante si no hay usuario registrado
                # Extraer nombre y email del contenido si está disponible
                nombre_visitante = nombre
                email_visitante = email_usuario if email_usuario != "Sin email" else None
                
                # Buscar visitante existente por email
                if email_visitante:
                    visitante, created = Visitante.objects.get_or_create(
                        email=email_visitante,
                        defaults={'nombre': nombre_visitante}
                    )
                    if not created:
                        visitante.nombre = nombre_visitante
                        visitante.save()
                else:
                    # Crear visitante sin email
                    visitante = Visitante.objects.create(
                        nombre=nombre_visitante,
                        email=email_visitante
                    )
                
                visitante.total_sugerencias += 1
                visitante.save()

            Sugerencia.objects.create(
                usuario=usuario,
                visitante=visitante,
                titulo=f"Sugerencia rápida - {nombre}",
                descripcion=contenido,
                categoria='mejora'
            )

            # Enviar email con HTML a miniamigixv@gmail.com
            email_error = None
            try:
                context = {
                    'nombre': nombre,
                    'email': email_usuario,
                    'mensaje': contenido,
                    'fecha': datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                html_message = render_to_string('email_sugerencia.html', context)
                plain_message = strip_tags(html_message)
                asunto = f"💡 NUEVA SUGERENCIA - {nombre}"
                
                admin_recipients = getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com'])
                if isinstance(admin_recipients, str):
                    admin_recipients = [admin_recipients]
                email = EmailMultiAlternatives(asunto, plain_message, settings.DEFAULT_FROM_EMAIL, admin_recipients)
                email.attach_alternative(html_message, "text/html")
                email.send()
            except Exception as e:
                email_error = str(e)

            if email_error:
                return JsonResponse({
                    'success': True,
                    'guardada_en': 'bd',
                    'email_error': email_error,
                    'mensaje': 'Sugerencia guardada en BD. El email no pudo enviarse. Verifica la contraseña de aplicación de Gmail.'
                })

            return JsonResponse({'success': True, 'guardada_en': 'bd_y_email'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def panel_admin(request):
    allowed_admins = getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com'])
    if request.user.email not in allowed_admins:
        return redirect('home')
    from sugerencias.models import Visitante
    context = {
        'total_usuarios': User.objects.count(),
        'total_chats': ConversacionChat.objects.count(),
        'total_canciones': Cancion.objects.count(),
        'total_publicaciones': PublicacionBlog.objects.count(),
        'total_eventos': Evento.objects.count(),
        'ultimos_usuarios': User.objects.order_by('-date_joined')[:10],
        'ultimas_notificaciones': Notificacion.objects.order_by('-fecha_creacion')[:5],
        'total_notificaciones': Notificacion.objects.count(),
        'total_visitantes': Visitante.objects.count(),
        'ultimos_visitantes': Visitante.objects.order_by('-fecha_ultima_interaccion')[:10],
    }
    return render(request, 'panel_admin.html', context)

@login_required
def admin_stats_api(request):
    # Verificar si el usuario es staff o superuser en lugar de verificar email específico
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    from sugerencias.models import Visitante
    
    stats = {
        'total_usuarios': User.objects.count(),
        'total_chats': ConversacionChat.objects.count(),
        'total_canciones': Cancion.objects.count(),
        'total_publicaciones': PublicacionBlog.objects.count(),
        'total_eventos': Evento.objects.count(),
        'total_notificaciones': Notificacion.objects.count(),
        'ultimos_usuarios': [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'date_joined': u.date_joined.strftime('%d %b %Y, %H:%M'),
                'is_superuser': u.is_superuser,
                'is_staff': u.is_staff
            }
            for u in User.objects.order_by('-date_joined')[:10]
        ],
        'ultimos_visitantes': [
            {
                'id': v.id,
                'nombre': v.nombre,
                'email': v.email,
                'fecha_ultima_interaccion': v.fecha_ultima_interaccion.strftime('%d %b %Y, %H:%M'),
                'total_sugerencias': v.total_sugerencias
            }
            for v in Visitante.objects.order_by('-fecha_ultima_interaccion')[:10]
        ]
    }
    return JsonResponse(stats)

@login_required
def panel_admin_email_user(request, user_id):
    admin_emails = getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com'])
    if isinstance(admin_emails, str):
        admin_emails = [admin_emails]

    if request.user.email not in admin_emails:
        return redirect('home')

    user_target = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not subject or not message:
            error = 'El asunto y el mensaje son obligatorios.'
            return render(request, 'panel_admin_email_user.html', {
                'user_target': user_target,
                'error': error,
                'subject': subject,
                'message': message,
            })

        if not user_target.email:
            error = 'Este usuario no tiene un correo válido.'
            return render(request, 'panel_admin_email_user.html', {
                'user_target': user_target,
                'error': error,
                'subject': subject,
                'message': message,
            })

        html_message = render_to_string('email_admin_response.html', {
            'recipient': user_target,
            'subject': subject,
            'message': message,
            'sender': request.user,
        })
        plain_message = strip_tags(html_message)

        # Aseguramos que el destinatario sea una lista [email]
        recipient_list = [user_target.email] if user_target.email else []

        try:
            email = EmailMultiAlternatives(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
            )
            email.attach_alternative(html_message, 'text/html')
            email.encoding = 'utf-8'
            email.send()
            return render(request, 'panel_admin_email_user.html', {
                'user_target': user_target,
                'success': True,
            })
        except Exception as e:
            return render(request, 'panel_admin_email_user.html', {
                'user_target': user_target,
                'error': f'No se pudo enviar el correo: {str(e)}',
                'subject': subject,
                'message': message,
            })

    return render(request, 'panel_admin_email_user.html', {
        'user_target': user_target,
    })

def crear_comentario(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            publicacion_id = data.get('publicacion_id')
            contenido = data.get('contenido', '').strip()
            padre_id = data.get('padre_id', None)
            
            if not contenido:
                return JsonResponse({'error': 'El contenido es requerido'}, status=400)
            
            publicacion = PublicacionBlog.objects.get(id=publicacion_id, publicado=True)
            
            comentario = Comment.objects.create(
                publicacion=publicacion,
                usuario=request.user,
                contenido=contenido
            )
            
            if padre_id:
                comentario.padre = Comment.objects.get(id=padre_id)
                comentario.save()
            
            return JsonResponse({
                'success': True,
                'comentario_id': comentario.id,
                'usuario': request.user.username,
                'contenido': contenido,
                'fecha': comentario.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def crear_categoria(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').strip()
            icono = data.get('icono', '📁')
            descripcion = data.get('descripcion', '').strip()
            
            if not nombre:
                return JsonResponse({'error': 'El nombre es requerido'}, status=400)
            
            categoria = Category.objects.create(
                nombre=nombre,
                icono=icono,
                descripcion=descripcion
            )
            
            return JsonResponse({
                'success': True,
                'categoria_id': categoria.id,
                'nombre': categoria.nombre,
                'icono': categoria.icono
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def eliminar_categoria(request, categoria_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    if request.method == 'DELETE':
        try:
            categoria = Category.objects.get(id=categoria_id)
            categoria.delete()
            return JsonResponse({'success': True})
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Categoría no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def guardar_puntuacion(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            juego_id = data.get('juego_id')
            puntuacion = data.get('puntuacion', 0)
            
            juego = Game.objects.get(id=juego_id, activo=True)
            score = Score.objects.create(
                usuario=request.user,
                juego=juego,
                puntuacion=puntuacion
            )
            
            # Verificar logros desbloqueados
            logros_desbloqueados = []
            logros = Achievement.objects.filter(juego=juego)
            for logro in logros:
                if logro.puntos_requeridos <= puntuacion:
                    user_logro, created = UserAchievement.objects.get_or_create(
                        usuario=request.user,
                        logro=logro
                    )
                    if created:
                        logros_desbloqueados.append({
                            'nombre': logro.nombre,
                            'icono': logro.icono,
                            'descripcion': logro.descripcion
                        })
            
            return JsonResponse({
                'success': True,
                'puntuacion': puntuacion,
                'logros_desbloqueados': logros_desbloqueados
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def admin_soporte(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')
    
    from soporte.models import TicketSoporte
    
    tickets = TicketSoporte.objects.all().select_related('usuario', 'respondido_por')
    
    # Calcular estadísticas
    total_tickets = tickets.count()
    tickets_abiertos = tickets.filter(estado='abierto').count()
    tickets_en_proceso = tickets.filter(estado='en_proceso').count()
    tickets_resueltos = tickets.filter(estado='resuelto').count()
    
    return render(request, 'admin_soporte.html', {
        'tickets': tickets,
        'total_tickets': total_tickets,
        'tickets_abiertos': tickets_abiertos,
        'tickets_en_proceso': tickets_en_proceso,
        'tickets_resueltos': tickets_resueltos
    })

def responder_ticket(request, ticket_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            respuesta = data.get('respuesta', '').strip()
            nuevo_estado = data.get('estado', 'en_proceso')
            
            if not respuesta:
                return JsonResponse({'error': 'La respuesta es requerida'}, status=400)
            
            ticket = TicketSoporte.objects.get(id=ticket_id)
            ticket.respuesta_admin = respuesta
            ticket.fecha_respuesta = datetime.datetime.now()
            ticket.respondido_por = request.user
            ticket.estado = nuevo_estado
            
            if nuevo_estado == 'resuelto':
                ticket.fecha_resolucion = datetime.datetime.now()
            
            ticket.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def admin_sugerencias(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')
    
    from sugerencias.models import Sugerencia
    
    sugerencias = Sugerencia.objects.all().select_related('usuario', 'respondido_por')
    
    # Calcular estadísticas
    total_sugerencias = sugerencias.count()
    sugerencias_pendientes = sugerencias.filter(estado='pendiente').count()
    sugerencias_en_revision = sugerencias.filter(estado='en_revision').count()
    sugerencias_aprobadas = sugerencias.filter(estado='aprobada').count()
    
    return render(request, 'admin_sugerencias.html', {
        'sugerencias': sugerencias,
        'total_sugerencias': total_sugerencias,
        'sugerencias_pendientes': sugerencias_pendientes,
        'sugerencias_en_revision': sugerencias_en_revision,
        'sugerencias_aprobadas': sugerencias_aprobadas
    })

def responder_sugerencia(request, sugerencia_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            respuesta = data.get('respuesta', '').strip()
            nuevo_estado = data.get('estado', 'en_revision')
            
            if not respuesta:
                return JsonResponse({'error': 'La respuesta es requerida'}, status=400)
            
            sugerencia = Sugerencia.objects.get(id=sugerencia_id)
            sugerencia.respuesta_admin = respuesta
            sugerencia.fecha_respuesta = datetime.datetime.now()
            sugerencia.respondido_por = request.user
            sugerencia.estado = nuevo_estado
            sugerencia.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@require_http_methods(["GET"])
def netease_lyrics_api(request):
    """Proxy para NetEase Music API para obtener letras sincronizadas"""
    song_name = request.GET.get('song', '')
    artist = request.GET.get('artist', '')

    if not song_name:
        return JsonResponse({'error': 'Nombre de canción requerido'}, status=400)

    try:
        query = f"{artist} {song_name}".strip()
        # Buscar canción en NetEase
        search_url = f"https://music.163.com/api/search/pc?s={requests.utils.quote(query)}&type=1&limit=10"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        search_response = requests.get(search_url, headers=headers, timeout=10)
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data and search_data.get('result') and search_data['result'].get('songs'):
                song_id_netease = search_data['result']['songs'][0]['id']

                # Obtener letras sincronizadas
                lyrics_url = f"https://music.163.com/api/song/lyric?id={song_id_netease}&lv=1&kv=1&tv=-1"
                lyrics_response = requests.get(lyrics_url, headers=headers, timeout=10)

                if lyrics_response.status_code == 200:
                    lyrics_data = lyrics_response.json()
                    if lyrics_data and lyrics_data.get('lrc') and lyrics_data['lrc'].get('lyric'):
                        return JsonResponse({
                            'success': True,
                            'syncedLyrics': lyrics_data['lrc']['lyric'],
                            'source': 'NetEase'
                        })

        return JsonResponse({'success': False, 'error': 'No se encontraron letras sincronizadas'})

    except Exception as e:
        logger.error(f"Error en netease_lyrics_api: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
