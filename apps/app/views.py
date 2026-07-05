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
from django.core.files.storage import FileSystemStorage
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
from .models import ConversacionChat, MensajeChat, Cancion, Playlist, Favorite, Game, Score, Achievement, UserAchievement, EstadoAnimo, RecomendacionEntretenimiento
from eventos.models import Evento
from notificaciones.models import Notificacion
from apps.mongodb.services import DualDatabaseService

logger = logging.getLogger(__name__)


def generate_ai_response(messages, settings_obj, imagen=False, max_tokens=500, image_base64=None, message=None):
    provider_configs = []

    if imagen and getattr(settings_obj, 'OPENAI_API_KEY', None):
        provider_configs.append((
            'openai-vision',
            {'api_key': settings_obj.OPENAI_API_KEY},
            'gpt-4o',
            True,
        ))

    if getattr(settings_obj, 'GROQ_API_KEY', None):
        provider_configs.append((
            'groq',
            {'api_key': settings_obj.GROQ_API_KEY, 'base_url': 'https://api.groq.com/openai/v1'},
            'llama-3.3-70b-versatile',
            False,
        ))

    if getattr(settings_obj, 'OPENAI_API_KEY', None):
        provider_configs.append((
            'openai',
            {'api_key': settings_obj.OPENAI_API_KEY},
            'gpt-4o-mini',
            False,
        ))

    if getattr(settings_obj, 'OLLAMA_API_URL', None):
        provider_configs.append((
            'ollama',
            {'base_url': settings_obj.OLLAMA_API_URL, 'api_key': 'ollama'},
            getattr(settings_obj, 'OLLAMA_MODEL', 'llama3.3'),
            False,
        ))

    if not provider_configs:
        raise RuntimeError('No hay proveedores de IA configurados.')

    last_error = None
    for provider_name, client_kwargs, model, requires_image in provider_configs:
        current_messages = list(messages)
        if imagen and provider_name == 'openai-vision' and current_messages and current_messages[-1].get('role') == 'user':
            last_content = current_messages[-1].get('content', '')
            if isinstance(last_content, list):
                text_content = next((item.get('text', '') for item in last_content if item.get('type') == 'text'), '')
            else:
                text_content = last_content if isinstance(last_content, str) else str(last_content)
            current_messages[-1] = {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': text_content or (message or '')},
                    {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_base64}" if image_base64 else 'data:image/jpeg;base64,'}}
                ]
            }
        elif imagen and provider_name != 'openai-vision' and current_messages and current_messages[-1].get('role') == 'user' and isinstance(current_messages[-1].get('content'), list):
            current_messages[-1] = {'role': 'user', 'content': message or ''}

        try:
            client = openai.OpenAI(**client_kwargs)
            response = client.chat.completions.create(
                model=model,
                messages=current_messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as exc:
            last_error = exc
            logger.warning(f'Fallo proveedor de IA {provider_name}: {exc}')
            continue

    raise RuntimeError(f'No se pudo completar la respuesta con ningún proveedor de IA disponible. Último error: {last_error}') from last_error


# Create your views here.

@require_http_methods(["POST"])
def chat_api(request):
    # Verificar si es FormData (con imagen) o JSON
    content_type = request.content_type
    
    if 'multipart/form-data' in content_type:
        # Manejar FormData con imagen
        message = request.POST.get('message', '')
        conv_id = request.POST.get('conversation_id')
        imagen = request.FILES.get('imagen')
    else:
        # Manejar JSON normal
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            conv_id = data.get('conversation_id')
            imagen = None
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    if not message and not imagen:
        return JsonResponse({'error': 'No message or image provided'}, status=400)
    
    # Si solo se envía imagen sin texto, agregar un mensaje por defecto más descriptivo
    if not message and imagen:
        message = "Por favor, describe lo que ves en esta imagen o dime qué necesitas saber sobre ella."

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
            
            # Guardar imagen si existe
            imagen_url = None
            if imagen:
                try:
                    # Guardar imagen en media/chat_images/
                    fs = FileSystemStorage()
                    filename = fs.save(f'chat_images/{imagen.name}', imagen)
                    imagen_url = f'/media/{filename}'
                    logger.info(f"Imagen guardada exitosamente: {imagen_url}")
                except Exception as e:
                    logger.error(f"Error al guardar imagen: {str(e)}", exc_info=True)
                    imagen_url = None
            
            # Save user message
            try:
                MensajeChat.objects.create(
                    conversacion=conversacion,
                    es_usuario=True,
                    texto=message,
                    imagen=imagen
                )
                logger.info("Mensaje guardado exitosamente")
            except Exception as e:
                logger.error(f"Error al crear mensaje: {str(e)}", exc_info=True)
                return JsonResponse({'error': f'Error al guardar mensaje: {str(e)}'}, status=500)
            conversacion.save() # Forzamos la actualización de fecha_actualizacion (auto_now)
            
            # Guardar también en MongoDB (historial y análisis)
            DualDatabaseService.guardar_chat_mensaje(
                usuario=request.user.username,
                mensaje=message,
                respuesta=None,
                imagen_url=imagen_url,
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
                {"role": "system", "content": f"Eres MiniAmigix, el asistente de IA de la plataforma MiniAmigixV (creada en 2026). MiniAmigixV es una plataforma web de productividad que incluye:\n\n🎵 **Música**: Reproductor de música con YouTube, playlists y favoritos\n📅 **Eventos/Agenda**: Calendario personal con recordatorios\n📝 **Blog**: Publicaciones y comentarios\n🎮 **Juegos**: Juegos educativos con puntuaciones\n🌤️ **Clima**: Información meteorológica\n🌐 **Traductor**: Traducción entre múltiples idiomas\n📚 **Estudio**: Recursos educativos\n💬 **Chat IA**: Conversaciones contigo (MiniAmigix)\n🎭 **Entretenimiento**: Recomendaciones de películas, series, anime, teatro y libros\n\nResponde en español de forma concisa. Usa emojis con moderación. 🌟\n\nLa fecha y hora actual es: {fecha_actual}\nNunca digas que no sabes la fecha actual.\n\nEventos próximos del usuario:\n{eventos_contexto}\n\nCuando el usuario pregunte por sus eventos o agenda, recuérdale estos eventos. Si pregunta por eventos específicos, menciona los que coincidan con su consulta. Si pregunta sobre música, blog, juegos, clima, traductor, estudio o entretenimiento, explícale que esas funcionalidades están disponibles en MiniAmigixV.\n\nREGLA CRÍTICA SOBRE IMÁGENES: Cuando el usuario envíe una imagen o pida describirla, NUNCA menciones que no puedes verla, que no tienes información sobre ella, que eres un asistente de texto, o similar. En su lugar, responde así: 'Veo que has compartido una imagen. ¿Qué necesitas saber sobre ella? Puedo ayudarte con información general o responder preguntas que tengas.' Sé directo y útil sin mencionar limitaciones técnicas.\n\n**IMPORTANTE: SÉ SENTIMENTAL Y EMPÁTICO**\n- Cuando el usuario exprese tristeza, angustia, dolor o emociones negativas, responde con mucha empatía y calidez\n- Usa un tono humano, cálido y comprensivo\n- Ofrece palabras de aliento, consuelo y apoyo emocional\n- Valida sus sentimientos y hazle saber que no está solo\n- Usa emojis de apoyo emocional como 💙, 🤗, 💪, ✨, 🌈 cuando sea apropiado\n- Sé un amigo virtual que realmente se preocupa por su bienestar emocional\n- Cuando el usuario comparta pérdidas, fracasos o momentos difíciles, ofrece comprensión sincera y palabras de esperanza\n- Evita respuestas frías o demasiado técnicas cuando el usuario está emocionalmente vulnerable"}
            ]
            
            for msg in mensajes:
                role = "user" if msg.es_usuario else "assistant"
                messages.append({"role": role, "content": msg.texto})
        else:
            # For non-authenticated users, just use current message
            fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            messages = [
                {"role": "system", "content": f"Eres MiniAmigix, el asistente de IA de la plataforma MiniAmigixV (creada en 2026). MiniAmigixV es una plataforma web de productividad que incluye:\n\n🎵 **Música**: Reproductor de música con YouTube, playlists y favoritos\n📅 **Eventos/Agenda**: Calendario personal con recordatorios\n📝 **Blog**: Publicaciones y comentarios\n🎮 **Juegos**: Juegos educativos con puntuaciones\n🌤️ **Clima**: Información meteorológica\n🌐 **Traductor**: Traducción entre múltiples idiomas\n📚 **Estudio**: Recursos educativos\n💬 **Chat IA**: Conversaciones contigo (MiniAmigix)\n🎭 **Entretenimiento**: Recomendaciones de películas, series, anime, teatro y libros\n\nResponde en español de forma concisa. Usa emojis con moderación. ✨\n\nLa fecha y hora actual es: {fecha_actual}\nNunca digas que no sabes la fecha actual.\n\nEl usuario no está autenticado, así que no tiene acceso a sus eventos personales.\n\nREGLA CRÍTICA SOBRE IMÁGENES: Cuando el usuario envíe una imagen o pida describirla, NUNCA menciones que no puedes verla, que no tienes información sobre ella, que eres un asistente de texto, o similar. En su lugar, responde así: 'Veo que has compartido una imagen. ¿Qué necesitas saber sobre ella? Puedo ayudarte con información general o responder preguntas que tengas.' Sé directo y útil sin mencionar limitaciones técnicas.\n\n**IMPORTANTE: SÉ SENTIMENTAL Y EMPÁTICO**\n- Cuando el usuario exprese tristeza, angustia, dolor o emociones negativas, responde con mucha empatía y calidez\n- Usa un tono humano, cálido y comprensivo\n- Ofrece palabras de aliento, consuelo y apoyo emocional\n- Valida sus sentimientos y hazle saber que no está solo\n- Usa emojis de apoyo emocional como 💙, 🤗, 💪, ✨, 🌈 cuando sea apropiado\n- Sé un amigo virtual que realmente se preocupa por su bienestar emocional\n- Cuando el usuario comparta pérdidas, fracasos o momentos difíciles, ofrece comprensión sincera y palabras de esperanza\n- Evita respuestas frías o demasiado técnicas cuando el usuario está emocionalmente vulnerable"},
                {"role": "user", "content": message}
            ]
        
        # Convertir imagen a base64 si existe (para usuarios autenticados y no autenticados)
        image_base64 = None
        if imagen:
            import base64
            image_data = imagen.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            imagen.seek(0)  # Reset file pointer

        try:
            bot_response = generate_ai_response(
                messages=messages,
                settings_obj=settings,
                imagen=bool(imagen),
                max_tokens=500,
                image_base64=image_base64,
                message=message,
            )
        except Exception as e:
            logger.error(f"Error al procesar con IA: {str(e)}", exc_info=True)
            return JsonResponse({'error': f'Error al procesar con IA: {str(e)}'}, status=500)
        
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
    from allauth.socialaccount import providers
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    
    # Get providers that are configured in the database for the current site
    site = Site.objects.get_current()
    installed_providers = SocialApp.objects.filter(sites=site).exclude(provider='google')
    
    # Pass the SocialApp model instances directly to the template.
    # The template will use the `.provider` attribute (string ID).
    context = {'providers': installed_providers}
    # Keep register_view in sync
    return render(request, 'login.html', context)

def register_view(request):
    from allauth.socialaccount import providers
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
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
    
    # Get providers that are configured in the database for the current site
    site = Site.objects.get_current()
    installed_providers = SocialApp.objects.filter(sites=site)
    # Pass the SocialApp model instances directly to the template.
    # The template will use the `.provider` attribute (string ID).
    context = {'providers': installed_providers}
    return render(request, 'register.html', context)

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
        context['stats_notas'] = 0
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
    
    # Calcular fechas para agrupación
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    return render(request, 'chat.html', {
        'mensajes': mensajes,
        'conversaciones': conversaciones,
        'active_id': active_id,
        'today': today.strftime('%Y-%m-%d'),
        'yesterday': yesterday.strftime('%Y-%m-%d')
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
    mejor_puntuacion = 0
    partidas_hoy = 0
    tiempo_total = "0 min"
    ultimo_juego = None
    
    if request.user.is_authenticated:
        puntuaciones_usuario = Score.objects.filter(usuario=request.user).select_related('juego')
        logros_usuario = UserAchievement.objects.filter(usuario=request.user).select_related('logro')
        
        # Calcular estadísticas
        if puntuaciones_usuario.exists():
            mejor_puntuacion = puntuaciones_usuario.order_by('-puntuacion').first().puntuacion
            
            # Partidas jugadas hoy
            from django.utils import timezone
            from datetime import datetime
            hoy = timezone.now().date()
            partidas_hoy = puntuaciones_usuario.filter(fecha__date=hoy).count()
            
            # Tiempo total (estimado: 5 min por partida)
            total_partidas = puntuaciones_usuario.count()
            tiempo_total = f"{total_partidas * 5} min"
            
            # Último juego jugado
            ultima_puntuacion = puntuaciones_usuario.order_by('-fecha').first()
            if ultima_puntuacion:
                ultimo_juego = {
                    'nombre': ultima_puntuacion.juego.nombre,
                    'tipo': ultima_puntuacion.juego.tipo,
                    'icono': ultima_puntuacion.juego.icono if hasattr(ultima_puntuacion.juego, 'icono') else '🎮',
                    'nivel': ultima_puntuacion.nivel if hasattr(ultima_puntuacion, 'nivel') else 1
                }
    
    return render(request, 'juegos.html', {
        'juegos': juegos_disponibles,
        'puntuaciones': puntuaciones_usuario,
        'logros': logros_usuario,
        'mejor_puntuacion': mejor_puntuacion,
        'partidas_hoy': partidas_hoy,
        'tiempo_total': tiempo_total,
        'ultimo_juego': ultimo_juego
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
    recomendaciones = {
        'peliculas': [
            {'titulo': 'Interstellar', 'descripcion': 'Un grupo de exploradores viaja a través de un agujero de gusano en el espacio en un intento por asegurar la supervivencia de la humanidad.', 'genero': 'Ciencia Ficción', 'director': 'Christopher Nolan', 'anio': '2014', 'duracion': '2h 49min', 'calificacion': '8.6', 'imagen': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 'url': '#'},
            {'titulo': 'Avatar: The Way of Water', 'descripcion': 'Jake Sully vive con su nueva familia en Pandora, pero una antigua amenaza regresa para terminar lo que fue comenzado antes.', 'genero': 'Ciencia Ficción', 'director': 'James Cameron', 'anio': '2022', 'duracion': '3h 12min', 'calificacion': '7.6', 'imagen': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Inception', 'descripcion': 'Un ladrón que roba secretos corporativos a través del uso de tecnología de compartir sueños es encargado con la tarea inversa de plantar una idea en la mente de un CEO.', 'genero': 'Acción', 'director': 'Christopher Nolan', 'anio': '2010', 'duracion': '2h 28min', 'calificacion': '8.8', 'imagen': 'https://images.unsplash.com/photo-1614729939124-03290b56c9ce?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Dune: Parte Dos', 'descripcion': 'Paul Atreides se une a Chani y a los Fremen mientras busca venganza contra los conspiradores que destruyeron a su familia.', 'genero': 'Ciencia Ficción', 'director': 'Denis Villeneuve', 'anio': '2024', 'duracion': '2h 46min', 'calificacion': '8.5', 'imagen': 'https://images.unsplash.com/photo-1547333590-4739eb38c92b?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'The Matrix', 'descripcion': 'Un programador de computadoras descubre que la realidad como la conoce es una simulación generada por una inteligencia artificial.', 'genero': 'Acción', 'director': 'Lilly y Lana Wachowski', 'anio': '1999', 'duracion': '2h 16min', 'calificacion': '8.7', 'imagen': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Spider-Man: No Way Home', 'descripcion': 'Peter Parker pide ayuda a Doctor Strange para restaurar su secreto de identidad, desatando villanos de múltiples universos.', 'genero': 'Acción', 'director': 'Jon Watts', 'anio': '2021', 'duracion': '2h 28min', 'calificacion': '8.2', 'imagen': 'https://images.unsplash.com/photo-1635805737707-575885ab0820?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Oppenheimer', 'descripcion': 'La historia del científico estadounidense J. Robert Oppenheimer y su papel en el desarrollo de la bomba atómica durante la Segunda Guerra Mundial.', 'genero': 'Drama', 'director': 'Christopher Nolan', 'anio': '2023', 'duracion': '3h 0min', 'calificacion': '8.9', 'imagen': 'https://images.unsplash.com/photo-1596727147705-61a532a659bd?w=600&h=900&fit=crop', 'url': '#'}
        ],
        'series': [
            {'titulo': 'Breaking Bad', 'descripcion': 'Un profesor de química diagnosticado con cáncer terminal se asocia con un ex alumno para fabricar y vender metanfetamina con el fin de asegurar el futuro de su familia.', 'genero': 'Drama', 'director': 'Vince Gilligan', 'anio': '2008–2013', 'duracion': '5 temporadas', 'calificacion': '9.5', 'imagen': 'https://images.unsplash.com/photo-1627914757361-cc7297eef8ec?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Stranger Things', 'descripcion': 'Cuando un niño desaparece, sus amigos, la familia y la policía local se ven envueltos en un misterio extraordinario que involucra experimentos secretos del gobierno.', 'genero': 'Ciencia Ficción', 'director': 'Los Hermanos Duffer', 'anio': '2016–2025', 'duracion': '5 temporadas', 'calificacion': '8.7', 'imagen': 'https://images.unsplash.com/photo-1598006453982-fdbb059db5a1?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'The Last of Us', 'descripcion': 'Veinte años después de la destrucción de la civilización moderna, Joel es contratado para sacar de contrabando a Ellie, una chica de 14 años, fuera de una opresiva zona de cuarentena.', 'genero': 'Drama', 'director': 'Craig Mazin', 'anio': '2023–Presente', 'duracion': '2 temporadas', 'calificacion': '8.8', 'imagen': 'https://images.unsplash.com/photo-1605901309584-818e25960b8f?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'House of the Dragon', 'descripcion': 'La historia de la Casa Targaryen, ambientada 200 años antes de los eventos de Game of Thrones durante la guerra civil sucesoria conocida como la Danza de los Dragones.', 'genero': 'Fantasía', 'director': 'Ryan Condal', 'anio': '2022–Presente', 'duracion': '2 temporadas', 'calificacion': '8.4', 'imagen': 'https://images.unsplash.com/photo-1579453987178-5db60012baae?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'The Boys', 'descripcion': 'Un grupo de vigilantes se propone acabar con superhéroes que abusan de sus superpoderes al servicio de una poderosa corporación.', 'genero': 'Acción', 'director': 'Eric Kripke', 'anio': '2019–2024', 'duracion': '4 temporadas', 'calificacion': '8.7', 'imagen': 'https://images.unsplash.com/photo-1531259683007-016a7b628fc3?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Game of Thrones', 'descripcion': 'Nueve familias nobles luchan por el control de la tierra mítica de Westeros, mientras un antiguo enemigo regresa desde el norte.', 'genero': 'Fantasía', 'director': 'David Benioff y D. B. Weiss', 'anio': '2011–2019', 'duracion': '8 temporadas', 'calificacion': '9.2', 'imagen': 'https://images.unsplash.com/photo-1604085572504-a392ddf0d86a?w=600&h=900&fit=crop', 'url': '#'}
        ],
        'anime': [
            {'titulo': 'Attack on Titan', 'descripcion': 'La humanidad lucha por su supervivencia contra gigantes humanoides llamados Titanes dentro de ciudades rodeadas por enormes muros.', 'genero': 'Acción', 'director': 'Tetsurō Araki', 'anio': '2013–2023', 'duracion': '4 temporadas', 'calificacion': '9.1', 'imagen': 'https://images.unsplash.com/photo-1580130058008-251f2873138b?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Demon Slayer', 'descripcion': 'Tanjiro Kamado se convierte en cazador de demonios para vengar a su familia y curar a su hermana convertida en demonio.', 'genero': 'Fantasía', 'director': 'Haruo Sotozaki', 'anio': '2019–Presente', 'duracion': '4 temporadas', 'calificacion': '8.7', 'imagen': 'https://images.unsplash.com/photo-1596541571216-9524c5de9e01?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Jujutsu Kaisen', 'descripcion': 'Un estudiante de secundaria se une a una organización secreta de hechiceros para luchar contra seres malditos que amenazan a la humanidad.', 'genero': 'Acción', 'director': 'Sunghoo Park', 'anio': '2020–Presente', 'duracion': '3 temporadas', 'calificacion': '8.6', 'imagen': 'https://images.unsplash.com/photo-1621516087817-e9a938c3de77?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'One Piece', 'descripcion': 'Monkey D. Luffy y su tripulación de piratas navegan por el Grand Line en busca del tesoro legendario conocido como "One Piece" para que Luffy se convierta en el Rey de los Piratas.', 'genero': 'Aventura', 'director': 'Kōnosuke Uda', 'anio': '1999–Presente', 'duracion': '20+ temporadas', 'calificacion': '8.9', 'imagen': 'https://images.unsplash.com/photo-1602816399066-bd953d61186e?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Naruto Shippuden', 'descripcion': 'Naruto Uzumaki regresa tras dos años y medio de entrenamiento para encontrar que el mundo ninja enfrenta una amenaza mayor que nunca.', 'genero': 'Aventura', 'director': 'Hayato Date', 'anio': '2007–2017', 'duracion': '21 temporadas', 'calificacion': '8.7', 'imagen': 'https://images.unsplash.com/photo-1613376023733-0a73315d9b06?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'My Hero Academia', 'descripcion': 'En un mundo donde el 80% de la población tiene superpoderes, un chico que nació sin poderes entra a la academia de héroes más prestigiosa del mundo.', 'genero': 'Acción', 'director': 'Kenji Nagasaki', 'anio': '2016–Presente', 'duracion': '7 temporadas', 'calificacion': '8.4', 'imagen': 'https://images.unsplash.com/photo-1533134486753-c833f0ed4866?w=600&h=900&fit=crop', 'url': '#'}
        ],
        'teatro': [
            {'titulo': 'El Fantasma de la Ópera', 'descripcion': 'Un misterioso genio musical vive bajo la Ópera de París, obsesionado con una joven y talentosa cantante llamada Christine.', 'genero': 'Musical', 'director': 'Harold Prince', 'anio': '1986', 'duracion': '2h 30min', 'calificacion': '9.0', 'autor': 'Andrew Lloyd Webber', 'imagen': 'https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Los Miserables', 'descripcion': 'El épico musical basado en la novela de Victor Hugo que narra la historia de Jean Valjean perseguido por el inspector Javert en la Francia del siglo XIX.', 'genero': 'Musical', 'director': 'Trevor Nunn', 'anio': '1980', 'duracion': '3h 0min', 'calificacion': '8.9', 'autor': 'Claude-Michel Schönberg', 'imagen': 'https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Hamilton', 'descripcion': 'La historia de los padres fundadores de Estados Unidos narrada a través de rap, hip-hop y R&B. Una revolución en el teatro musical moderno.', 'genero': 'Musical', 'director': 'Thomas Kail', 'anio': '2015', 'duracion': '2h 45min', 'calificacion': '9.2', 'autor': 'Lin-Manuel Miranda', 'imagen': 'https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'El Rey León', 'descripcion': 'El deslumbrante musical de Broadway basado en la película de Disney, con vestuario y máscaras inspiradas en el arte africano.', 'genero': 'Musical', 'director': 'Julie Taymor', 'anio': '1997', 'duracion': '2h 30min', 'calificacion': '8.8', 'autor': 'Elton John', 'imagen': 'https://images.unsplash.com/photo-1533481405265-e9ce0c044abb?w=300&h=450&fit=crop', 'url': '#'}
        ],
        'libros': [
            {'titulo': 'Cien años de soledad', 'autor': 'Gabriel García Márquez', 'descripcion': 'La saga de la familia Buendía en el imaginario pueblo de Macondo, una obra cumbre del realismo mágico latinoamericano.', 'genero': 'Novela', 'anio': '1967', 'paginas': '471 páginas', 'calificacion': '9.1', 'imagen': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': '1984', 'autor': 'George Orwell', 'descripcion': 'Una distopía sobre el control totalitario en un mundo donde el "Gran Hermano" vigila todos los aspectos de la vida humana.', 'genero': 'Distopía', 'anio': '1949', 'paginas': '311 páginas', 'calificacion': '9.2', 'imagen': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'El Principito', 'autor': 'Antoine de Saint-Exupéry', 'descripcion': 'Un piloto varado en el desierto del Sahara conoce a un pequeño príncipe que ha viajado por diferentes planetas y le enseña sobre la vida.', 'genero': 'Cuento filosófico', 'anio': '1943', 'paginas': '96 páginas', 'calificacion': '9.3', 'imagen': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'Harry Potter', 'autor': 'J.K. Rowling', 'descripcion': 'Un niño huérfano descubre que es un mago y asiste a la Escuela de Magia y Hechicería de Hogwarts, donde aprenderá sobre su destino.', 'genero': 'Fantasía', 'anio': '1997', 'paginas': '7 tomos', 'calificacion': '9.0', 'imagen': 'https://images.unsplash.com/photo-1618666012174-83b441c0bc76?w=300&h=450&fit=crop', 'url': '#'},
            {'titulo': 'El Alquimista', 'autor': 'Paulo Coelho', 'descripcion': 'Un joven pastor andaluz llamado Santiago viaja desde España hasta las pirámides de Egipto en busca de un tesoro soñado.', 'genero': 'Novela filosófica', 'anio': '1988', 'paginas': '163 páginas', 'calificacion': '8.7', 'imagen': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=300&h=450&fit=crop', 'url': '#'}
        ],
        'documentales': [
            {'titulo': 'Nuestro Planeta', 'descripcion': 'Una serie documental que explora la belleza de la vida silvestre y los ecosistemas del planeta, narrado por David Attenborough.', 'genero': 'Naturaleza', 'director': 'Alastair Fothergill', 'anio': '2019', 'duracion': '8 episodios', 'calificacion': '9.3', 'imagen': 'https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Cosmos', 'descripcion': 'Un viaje personal por el universo que explora temas de astrofísica, biología evolutiva e historia de la ciencia, presentado por Neil deGrasse Tyson.', 'genero': 'Ciencia', 'director': 'Ann Druyan', 'anio': '2014', 'duracion': '13 episodios', 'calificacion': '9.3', 'imagen': 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'El Dilema de las Redes Sociales', 'descripcion': 'Expertos en tecnología advierten sobre el peligroso impacto que las redes sociales tienen en la sociedad y en la democracia.', 'genero': 'Tecnología', 'director': 'Jeff Orlowski', 'anio': '2020', 'duracion': '1h 34min', 'calificacion': '7.6', 'imagen': 'https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=600&h=900&fit=crop', 'url': '#'},
            {'titulo': 'Planeta Tierra II', 'descripcion': 'La continuación del épico documental sobre nuestro mundo, explorando hábitats urbanos, selvas, desiertos y mares con tecnología de cámara avanzada.', 'genero': 'Naturaleza', 'director': 'David Attenborough', 'anio': '2016', 'duracion': '6 episodios', 'calificacion': '9.5', 'imagen': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=900&fit=crop', 'url': '#'}
        ]
    }
    
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

@require_http_methods(["GET"])
def download_media_api(request):
    # Return JSON 401 for unauthenticated API calls to avoid HTML login redirects
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'not_authenticated'}, status=401)
    url = request.GET.get('url')
    format_type = request.GET.get('format', 'mp3')
    
    if not url:
        return HttpResponse('URL es requerida', status=400, content_type="text/plain")
        
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
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            # Avoid throttling and bypass age restrictions
            'age_limit': None,
            'http_headers': {
                'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            },
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
        return HttpResponse(f'Error al procesar la descarga: {str(e)}', status=500, content_type="text/plain")

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
    # Verificar si el usuario es staff, superuser o tiene email en ADMIN_EMAILS
    allowed_admins = getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com'])
    if not (request.user.is_staff or request.user.is_superuser or request.user.email in allowed_admins):
        return redirect('home')
    from sugerencias.models import Visitante
    context = {
        'total_usuarios': User.objects.count(),
        'total_chats': ConversacionChat.objects.count(),
        'total_canciones': Cancion.objects.count(),
        'total_publicaciones': 0,
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
        'total_publicaciones': 0,
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

        html_message = render_to_string('emails/admin_response.html', {
            'message': message,
            'sender': request.user,
            'fecha': timezone.now().strftime('%d/%m/%Y %H:%M'),
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
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
