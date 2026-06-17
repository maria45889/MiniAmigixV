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
import yt_dlp
from .models import ConversacionChat, MensajeChat, Cancion, PublicacionBlog
from eventos.models import Evento

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
            
            # Get conversation history
            # Fetch latest 10 and reverse to restore chronological order
            mensajes = list(MensajeChat.objects.filter(conversacion=conversacion).order_by('-fecha_creacion')[:10])[::-1]
            messages = [
                {"role": "system", "content": "Eres MiniAmigix, un asistente amigable y entusiasta. Responde en español de forma concisa. Usa emojis con moderación, solo cuando sea necesario para dar énfasis. 🌟"}
            ]
            
            for msg in mensajes:
                role = "user" if msg.es_usuario else "assistant"
                messages.append({"role": role, "content": msg.texto})
        else:
            # For non-authenticated users, just use current message
            messages = [
                {"role": "system", "content": "Eres MiniAmigix, un asistente amigable y entusiasta. Responde en español de forma concisa. Usa emojis con moderación. ✨"},
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
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'El usuario ya existe'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')

def home(request):
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
    else:
        context['stats_chats'] = 0
        context['stats_notas'] = 0
        context['stats_eventos'] = 0
        context['stats_canciones'] = 0

    return render(request, 'home.html', context)

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
                else:
                    traduccion = f"[{idiomas_nombres.get(origen, origen)} → {idiomas_nombres.get(destino, destino)}] {texto}"

            return JsonResponse({'traduccion': traduccion, 'origen': origen, 'destino': destino})
        except Exception as e:
            logger.error(f"Error en traductor: {str(e)}", exc_info=True)
            return JsonResponse({'error': 'Error interno al intentar traducir el texto.'}, status=500)

    return render(request, 'traductor.html')

def entretenimiento(request):
    recomendaciones = {'peliculas': [], 'series': [], 'libros': [], 'teatro': []}

    try:
        if hasattr(settings, 'YOUTUBE_API_KEY') and settings.YOUTUBE_API_KEY:
            # Buscar tráilers/populares en YouTube como recomendaciones
            categorias = {
                'peliculas': 'tráilers películas 2025 2026',
                'series': 'mejores series 2025 2026',
                'teatro': 'obras teatro recomendadas 2025',
            }
            for cat, query in categorias.items():
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': query,
                    'type': 'video',
                    'maxResults': 4,
                    'key': settings.YOUTUBE_API_KEY,
                    'regionCode': 'ES',
                    'relevanceLanguage': 'es'
                }
                headers = {'Referer': request.build_absolute_uri('/')}
                resp = requests.get(url, params=params, headers=headers, timeout=10)
                if resp.status_code == 200:
                    items = resp.json().get('items', [])
                    for item in items:
                        recomendaciones[cat].append({
                            'titulo': item['snippet']['title'],
                            'descripcion': item['snippet']['description'][:120],
                            'imagen': item['snippet']['thumbnails']['high']['url'],
                            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                            'video_id': item['id']['videoId']
                        })

        # Libros: usar Groq API para recomendar libros
        if settings.GROQ_API_KEY and not recomendaciones['libros']:
            client = openai.OpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
            prompt = "Recomienda 4 libros populares en español de diferentes géneros. Devuelve SOLO JSON con formato: [{\"titulo\": \"...\", \"autor\": \"...\", \"descripcion\": \"...\"}]. Sin markdown ni explicaciones."
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], max_tokens=500)
            json_match = re.search(r'\[.*\]', response.choices[0].message.content, re.DOTALL)
            if json_match:
                libros = json.loads(json_match.group())
                for libro in libros:
                    recomendaciones['libros'].append(libro)
    except Exception as e:
        logger.error(f"Error en vista entretenimiento al obtener recomendaciones externas: {str(e)}")

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
def stream_audio_api(request, youtube_id):
    url = f"https://www.youtube.com/watch?v={youtube_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            return JsonResponse({'success': True, 'url': audio_url})
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
        else:
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })
            expected_ext = 'mp4'
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Find the actual file generated in the temp directory to avoid path guessing errors
            files = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
            if not files:
                raise Exception("No se pudo localizar el archivo descargado.")

            # Prefer the file matching the expected extension (mp3/mp4)
            final_filename = next((f for f in files if f.endswith(expected_ext)), files[0])
            final_path = os.path.join(temp_dir, final_filename)

            if os.path.getsize(final_path) > 0:
                file = open(final_path, 'rb')
                response = FileResponse(file)

                # Sanitize the title for the attachment header
                title = info.get('title', 'descarga')
                safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip()
                response['Content-Disposition'] = f'attachment; filename="{safe_title}.{expected_ext}"'

                # Add Content-Length and Content-Type
                try:
                    size = os.path.getsize(final_path)
                    response['Content-Length'] = str(size)
                except Exception:
                    pass
                ctype, _ = mimetypes.guess_type(final_path)
                if ctype:
                    response['Content-Type'] = ctype

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
            else:
                # Clean up temp dir on failure
                try:
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass
                return HttpResponse('Error: Archivo no generado o vacío', status=500)
                
    except Exception as e:
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
    
    return render(request, 'blog.html', {
        'noticias_globales': noticias_globales,
        'mis_publicaciones': mis_publicaciones
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
        visible_para_todos = True
        
        if request.user.is_staff:
            es_oficial = request.POST.get('es_oficial') == 'on'
            fijado = request.POST.get('fijado') == 'on'
            visible_para_todos = request.POST.get('visible_para_todos') == 'on'
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
            from sugerencias.models import Sugerencia
            Sugerencia.objects.create(
                usuario=usuario,
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
                
                email = EmailMultiAlternatives(asunto, plain_message, settings.EMAIL_HOST_USER, ['miniamigixv@gmail.com'])
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
    if request.user.email != 'miniamigixv@gmail.com':
        return redirect('home')
        
    context = {
        'total_usuarios': User.objects.count(),
        'total_chats': ConversacionChat.objects.count(),
        'total_canciones': Cancion.objects.count(),
        'total_publicaciones': PublicacionBlog.objects.count(),
        'total_eventos': Evento.objects.count(),
        'ultimos_usuarios': User.objects.order_by('-date_joined')[:10],
    }
    print('ULTIMOS USUARIOS:')
    print([u.username for u in context['ultimos_usuarios']])
    return render(request, 'panel_admin.html', context)

@login_required
def panel_admin_email_user(request, user_id):
    if request.user.email != 'miniamigixv@gmail.com':
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

        try:
            email = EmailMultiAlternatives(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user_target.email],
            )
            email.attach_alternative(html_message, 'text/html')
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
