from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer, ConversacionChatSerializer, CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.app.models import ConversacionChat, MensajeChat
from django.conf import settings
import openai
from apps.notificaciones.models import Notificacion
from apps.perfil.models import Perfil
import logging
from apps.app.services import ChatService

logger = logging.getLogger(__name__)

class APIRootView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        return Response({
            'status': 'success',
            'message': 'MiniAmigixV API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/login/',
                'register': '/api/register/',
                'profile': '/api/profile/',
                'chat': '/api/chat/',
                'entretenimiento': '/entretenimiento/'
            }
        })

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ChatHistoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        conversacion = ConversacionChat.objects.filter(usuario=request.user).first()
        if not conversacion:
            return Response([])
        mensajes = MensajeChat.objects.filter(conversacion=conversacion).order_by('fecha_creacion')
        data = [{'role': 'user' if m.es_usuario else 'assistant', 'content': m.texto, 'created_at': m.fecha_creacion} for m in mensajes]
        return Response(data)

class ChatSendView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'No message provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        conversacion, created = ConversacionChat.objects.get_or_create(usuario=request.user, defaults={'titulo': 'Chat Principal'})
        
        MensajeChat.objects.create(conversacion=conversacion, es_usuario=True, texto=message)
        conversacion.save()

        mensajes = list(MensajeChat.objects.filter(conversacion=conversacion).order_by('-fecha_creacion')[:10])[::-1]
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        messages = [
            {"role": "system", "content": f"Eres MiniAmigix, el asistente de IA de la plataforma MiniAmigixV (creada en 2026). MiniAmigixV es una plataforma web de productividad y entretenimiento que incluye:\n\n🎵 **Música**: Reproductor de música con YouTube, playlists y favoritos\n📅 **Eventos/Agenda**: Calendario personal con recordatorios\n📝 **Blog**: Publicaciones y comentarios\n🎮 **Juegos**: Juegos educativos con puntuaciones\n🌤️ **Clima**: Información meteorológica\n🌐 **Traductor**: Traducción entre múltiples idiomas\n📚 **Estudio**: Recursos educativos\n💬 **Chat IA**: Conversaciones contigo (MiniAmigix)\n\nResponde en español de forma concisa. Usa emojis con moderación. 🌟\n\nLa fecha y hora actual es: {fecha_actual}\nNunca digas que no sabes la fecha actual.\n\n**IMPORTANTE: SÉ SENTIMENTAL Y EMPÁTICO**\n- Cuando el usuario exprese tristeza, angustia, dolor o emociones negativas, responde con mucha empatía y calidez\n- Usa un tono humano, cálido y comprensivo\n- Ofrece palabras de aliento, consuelo y apoyo emocional\n- Valida sus sentimientos y hazle saber que no está solo\n- Usa emojis de apoyo emocional como 💙, 🤗, 💪, ✨, 🌈 cuando sea apropiado\n- Sé un amigo virtual que realmente se preocupa por su bienestar emocional\n- Cuando el usuario comparta pérdidas, fracasos o momentos difíciles, ofrece comprensión sincera y palabras de esperanza\n- Evita respuestas frías o demasiado técnicas cuando el usuario está emocionalmente vulnerable"}
        ]
        
        for msg in mensajes:
            role = "user" if msg.es_usuario else "assistant"
            messages.append({"role": role, "content": msg.texto})

        try:
            bot_response = ChatService.generate_ai_response(
                messages=messages,
                settings_obj=settings,
                imagen=False,
                max_tokens=150,
                image_base64=None,
                message=message,
            )
            
            MensajeChat.objects.create(conversacion=conversacion, es_usuario=False, texto=bot_response)
            conversacion.save()
            
            try:
                Notificacion.objects.create(
                    usuario=request.user,
                    titulo='💬 Nueva respuesta del Chat IA',
                    mensaje=f'MiniAmigix ha respondido: "{bot_response[:100]}..."',
                    tipo='info',
                    enlace='/chat/'
                )
            except Exception as e:
                logger.error(f"Error al crear notificación de chat: {str(e)}")

            return Response({'response': bot_response})
        except Exception as e:
            logger.error(f"Error en ChatSendView: {str(e)}", exc_info=True)
            return Response({'error': 'Error procesando respuesta'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateLanguageView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        idioma = request.data.get('idioma')
        if not idioma:
            return Response({'error': 'Idioma no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)
        
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        perfil.idioma = idioma
        perfil.save()
        
        return Response({'success': True, 'idioma': idioma})
