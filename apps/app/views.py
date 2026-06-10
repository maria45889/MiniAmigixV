from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import openai
from .models import ConversacionChat, MensajeChat

# Create your views here.

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        message = data.get('message', '')
        
        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        
        try:
            # Get or create conversation for user
            if request.user.is_authenticated:
                conversacion, created = ConversacionChat.objects.get_or_create(
                    usuario=request.user,
                    defaults={'titulo': 'Conversación actual'}
                )
                
                # Save user message
                MensajeChat.objects.create(
                    conversacion=conversacion,
                    es_usuario=True,
                    texto=message
                )
                
                # Get conversation history
                mensajes = MensajeChat.objects.filter(conversacion=conversacion).order_by('fecha_creacion')[-10:]
                messages = [
                    {"role": "system", "content": "Eres un asistente útil y amigable llamado MiniAmigix. Responde en español de manera clara y concisa."}
                ]
                
                for msg in mensajes:
                    role = "user" if msg.es_usuario else "assistant"
                    messages.append({"role": role, "content": msg.texto})
            else:
                # For non-authenticated users, just use current message
                messages = [
                    {"role": "system", "content": "Eres un asistente útil y amigable llamado MiniAmigix. Responde en español de manera clara y concisa."},
                    {"role": "user", "content": message}
                ]
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
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
            
            return JsonResponse({'response': bot_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'El usuario ya existe'})
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return render(request, 'home.html')
    
    return render(request, 'register.html')

def home(request):
    return render(request, 'home.html')

def index(request):
    from django.shortcuts import redirect
    return redirect('tutorial_home')

def chat(request):
    return render(request, 'chat.html')

def musica(request):
    return render(request, 'musica.html')

def juegos(request):
    return render(request, 'juegos.html')

def estudio(request):
    return render(request, 'estudio.html')

def eventos(request):
    from django.shortcuts import redirect
    return redirect('lista_eventos')

def clima(request):
    return render(request, 'clima.html')

def traductor(request):
    return render(request, 'traductor.html')

def entretenimiento(request):
    return render(request, 'entretenimiento.html')

def blog(request):
    return render(request, 'blog.html')

def notificaciones(request):
    from django.shortcuts import redirect
    return redirect('lista_notificaciones')

def perfil(request):
    from django.shortcuts import redirect
    return redirect('perfil')

def configuracion(request):
    from django.shortcuts import redirect
    return redirect('configuracion_view')

def soporte(request):
    from django.shortcuts import redirect
    return redirect('soporte')

def sugerencias(request):
    from django.shortcuts import redirect
    return redirect('lista_sugerencias')

def logout_view(request):
    from django.contrib.auth import logout
    from django.shortcuts import redirect
    logout(request)
    return redirect('home')
