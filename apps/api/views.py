from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer, ConversacionChatSerializer
from rest_framework.views import APIView
from app.models import ConversacionChat, MensajeChat
from django.conf import settings
import openai
from notificaciones.models import Notificacion
import logging

logger = logging.getLogger(__name__)

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
        messages = [
            {"role": "system", "content": "Eres MiniAmigix, un asistente amigable y entusiasta. Responde en español de forma concisa. Usa emojis con moderación. 🌟"}
        ]
        
        for msg in mensajes:
            role = "user" if msg.es_usuario else "assistant"
            messages.append({"role": role, "content": msg.texto})

        if settings.GROQ_API_KEY:
            client = openai.OpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
            model = "llama-3.3-70b-versatile"
        elif settings.OPENAI_API_KEY:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            model = "gpt-4o-mini"
        else:
            return Response({'error': 'No AI API keys configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=150
            )
            bot_response = response.choices[0].message.content
            
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
