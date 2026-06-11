from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import os
import openai
import requests
from .models import ConversacionChat, MensajeChat, Cancion, PublicacionBlog

# Create your views here.

def chat_api(request):
    if request.method == 'POST':
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
                
                # Get conversation history
                # Fetch latest 10 and reverse to restore chronological order
                mensajes = list(MensajeChat.objects.filter(conversacion=conversacion).order_by('-fecha_creacion')[:10])[::-1]
                messages = [
                    {"role": "system", "content": "Eres MiniAmigix, un asistente amigable y entusiasta. Responde en español, de forma concisa y utiliza emojis para hacer la conversación más amena. 🚀"}
                ]
                
                for msg in mensajes:
                    role = "user" if msg.es_usuario else "assistant"
                    messages.append({"role": role, "content": msg.texto})
            else:
                # For non-authenticated users, just use current message
                messages = [
                    {"role": "system", "content": "Eres MiniAmigix, un asistente amigable y entusiasta. Responde en español, de forma concisa y utiliza emojis. ✨"},
                    {"role": "user", "content": message}
                ]
            
            # Flexible client: Use Groq if key is available for faster inference, otherwise OpenAI
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
                return JsonResponse({'error': 'No AI API keys configured.'}, status=500)

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
            
            return JsonResponse({'response': bot_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'GET':
        return JsonResponse({'error': 'Please use POST to interact with the Chat API'}, status=405)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

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
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'El usuario ya existe'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')

def home(request):
    return render(request, 'home.html')

def index(request):
    return redirect('tutorial_home')

def chat(request):
    mensajes = []
    conversaciones = []
    active_id = None
    if request.user.is_authenticated:
        conversaciones = ConversacionChat.objects.filter(usuario=request.user).order_by('-fecha_actualizacion')
        
        # Verificar si se solicita crear un nuevo chat
        if request.GET.get('new') == 'true':
            # Crear un nuevo chat con un título único
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M")
            new_chat = ConversacionChat.objects.create(
                usuario=request.user,
                titulo=f'Chat {timestamp}'
            )
            # Redirigir al nuevo chat
            from django.shortcuts import redirect
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
    canciones = []
    if request.user.is_authenticated:
        canciones = Cancion.objects.filter(usuario=request.user).order_by('-fecha_agregada')[:5]
    
    return render(request, 'musica.html', {
        'canciones': canciones
    })

def juegos(request):
    return render(request, 'juegos.html')

def estudio(request):
    return render(request, 'estudio.html')

def eventos(request):
    return redirect('lista_eventos')

def clima(request):
    ciudad = request.GET.get('ciudad', '')
    datos_clima = None
    error = None

    if ciudad:
        # Ejemplo usando OpenWeatherMap (necesitas una API KEY en settings.py)
        api_key_raw = getattr(settings, 'OPENWEATHER_API_KEY', None)
        api_key = api_key_raw.strip() if api_key_raw else None
        if api_key:
            # Asegúrate de que la ciudad no esté vacía antes de hacer la solicitud
            if not ciudad.strip():
                error = "Por favor, introduce un nombre de ciudad válido."
            else:
                try:
                    url = "https://api.openweathermap.org/data/2.5/weather"
                    params = {
                        'q': ciudad,
                        'appid': api_key,
                        'units': 'metric',
                        'lang': 'es'
                    }
                    response = requests.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        datos_clima = response.json()
                    else:
                        # Intentamos obtener el mensaje de error real de la API
                        try:
                            api_data = response.json()
                            mensaje_api = api_data.get('message', 'Error desconocido')
                        except Exception:
                            mensaje_api = "Respuesta no válida del servidor"

                        if response.status_code == 401:
                            error = f"Autenticación fallida: {mensaje_api}. Verifica tu API Key y espera 2 horas si es nueva."
                        elif response.status_code == 404:
                            error = f"Ciudad no encontrada: {mensaje_api}."
                        else:
                            error = f"Error {response.status_code}: {mensaje_api}"
                except requests.exceptions.RequestException:
                    error = "Hubo un problema de conexión con el servicio de clima."
        else:
            error = "La clave API de OpenWeatherMap no está configurada en el servidor. Por favor, verifica tu archivo .env y settings.py."

    return render(request, 'clima.html', {'datos_clima': datos_clima, 'ciudad': ciudad, 'error': error})

def traductor(request):
    return render(request, 'traductor.html')

def entretenimiento(request):
    return render(request, 'entretenimiento.html')

def blog(request):
    return render(request, 'blog.html')

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
    logout(request)
    return redirect('home')

@require_http_methods(["POST"])
def add_song_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
    
    try:
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

@require_http_methods(["DELETE"])
def delete_song_api(request, song_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
    
    try:
        cancion = Cancion.objects.get(id=song_id, usuario=request.user)
        cancion.delete()
        return JsonResponse({'success': True})
    except Cancion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Canción no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ==================== VISTAS DEL BLOG ====================
def blog(request):
    publicaciones = []
    if request.user.is_authenticated:
        # Solo mostrar publicaciones del usuario actual
        publicaciones = PublicacionBlog.objects.filter(
            usuario=request.user,
            publicado=True
        ).order_by('-fecha_publicacion')
    
    return render(request, 'blog.html', {
        'publicaciones': publicaciones
    })

def crear_publicacion(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        categoria = request.POST.get('categoria', 'personal')
        
        if not titulo or not contenido:
            return render(request, 'blog.html', {
                'error': 'Por favor completa todos los campos'
            })
        
        PublicacionBlog.objects.create(
            usuario=request.user,
            titulo=titulo,
            contenido=contenido,
            categoria=categoria
        )
        
        return redirect('blog')
    
    return render(request, 'blog.html')

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
