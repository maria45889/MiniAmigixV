"""
Chat views.
"""

import logging
import threading
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.app.services import ChatService
from apps.app.selectors import ChatSelector
from apps.app.api import OpenAIAPI
from apps.app.constants import CHAT_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES
from apps.app.utils import JsonResponseHelper, RequestParser, LogHelper
from apps.app.validators import ChatValidator

logger = logging.getLogger(__name__)


@login_required
def chat_view(request):
    """Render chat page."""
    conversaciones_data = ChatSelector.get_all_by_user_with_last_message(request.user)
    conversaciones = [item['conversation'] for item in conversaciones_data]

    # Get requested conversation by ID if provided
    conv_id = request.GET.get('id')
    active_conv = None
    if conv_id:
        active_conv = ChatSelector.get_by_user_and_id(request.user, conv_id)

    if not active_conv:
        active_conv = conversaciones[0] if conversaciones else None
        if not active_conv:
            active_conv = ChatSelector.get_or_create_main(request.user)
            conversaciones = [active_conv]
            conversaciones_data = [{'conversation': active_conv, 'last_message': None}]

    mensajes = ChatSelector.get_recent_chronological(active_conv, limit=50)
    active_id = active_conv.id

    return render(request, 'chat.html', {
        'conversaciones_data': conversaciones_data,
        'conversaciones': conversaciones,
        'active_conv': active_conv,
        'mensajes': mensajes,
        'active_id': active_id
    })


@require_http_methods(["POST"])
@csrf_exempt
def chat_api(request):
    """Chat API endpoint."""
    try:
        # Parse request - siempre usar POST para FormData
        message = request.POST.get('message', '')
        conv_id = request.POST.get('conversation_id')
        imagen = request.FILES.get('imagen')
        
        # Validate
        try:
            ChatValidator.validate_message(message, imagen)
        except Exception as e:
            return JsonResponseHelper.error_response(str(e))
        
        # Get or create conversation
        if request.user.is_authenticated:
            conversation, error = ChatService.get_or_create_conversation(request.user, conv_id)
            if error:
                return JsonResponseHelper.not_found_response(error)
            
            # Save image if exists
            imagen_url = None
            if imagen:
                imagen_url = ChatService.save_image(imagen)
            
            # Save user message
            ChatSelector.create_message(conversation, True, message, imagen)
            LogHelper.log_info(logger, SUCCESS_MESSAGES['message_saved'])
            
            conversation.save()
            
            # Get conversation history
            mensajes = ChatSelector.get_recent_chronological(conversation, CHAT_CONFIG['max_history_messages'])
            
            # Get events context
            eventos_contexto = ChatService.get_events_context(request.user)
            
            # Build messages for AI
            from ..constants.prompts import SYSTEM_PROMPT_AUTHENTICATED
            from ..utils import DateTimeHelper

            fecha_actual = DateTimeHelper.get_current_datetime_formatted()
            system_message = SYSTEM_PROMPT_AUTHENTICATED.format(
                fecha_actual=fecha_actual,
                eventos_contexto=eventos_contexto
            )
            
            messages = [{"role": "system", "content": system_message}]
            
            for msg in mensajes:
                role = "user" if msg.es_usuario else "assistant"
                messages.append({"role": role, "content": msg.texto})
        else:
            # Non-authenticated users
            from ..constants.prompts import SYSTEM_PROMPT_UNAUTHENTICATED
            from ..utils import DateTimeHelper

            fecha_actual = DateTimeHelper.get_current_datetime_formatted()
            system_message = SYSTEM_PROMPT_UNAUTHENTICATED.format(fecha_actual=fecha_actual)
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ]
        
        # Convert image to base64 if exists
        image_base64 = None
        if imagen:
            image_base64 = ChatService.convert_image_to_base64(imagen)
        
        # Generate AI response
        bot_response = ChatService.generate_ai_response(
            messages=messages,
            settings_obj=settings,
            imagen=bool(imagen),
            max_tokens=CHAT_CONFIG['max_tokens'],
            image_base64=image_base64,
            message=message,
        )
        
        # Save bot response for authenticated users
        if request.user.is_authenticated:
            ChatSelector.create_message(conversation, False, bot_response)
            conversation.save()

            # Create notification asynchronously to avoid blocking
            notification_thread = threading.Thread(
                target=ChatService.create_chat_notification,
                args=(request.user, bot_response)
            )
            notification_thread.daemon = True
            notification_thread.start()

        return JsonResponseHelper.success_response({'response': bot_response})

    except Exception as e:
        LogHelper.log_error(logger, f"Error en chat_api: {str(e)}", exc_info=True)
        return JsonResponseHelper.error_response(message=f"Ocurrió un error con la IA: {str(e)}", status=500)


@require_http_methods(["DELETE", "POST"])
@csrf_exempt
def delete_chat_api(request, chat_id):
    """Delete a chat conversation."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)

    try:
        from apps.app.models import ConversacionChat
        chat_obj = ConversacionChat.objects.filter(id=chat_id, usuario=request.user).first()
        if not chat_obj:
            return JsonResponse({'status': 'error', 'error': 'Chat no encontrado'}, status=404)
        chat_obj.delete()
        return JsonResponse({'status': 'success', 'message': 'Chat eliminado correctamente'})
    except Exception as e:
        LogHelper.log_error(logger, f"Error al eliminar chat: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def crear_chat_api(request):
    """Create a new chat conversation."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'success', 'conversation_id': None})

    try:
        count = ChatSelector.count_by_user(request.user)
        titulo = f"Chat #{count + 1}"
        conversacion = ChatSelector.create_for_user(request.user, title=titulo)
        return JsonResponse({
            'status': 'success',
            'conversation_id': conversacion.id,
            'titulo': conversacion.titulo
        })
    except Exception as e:
        LogHelper.log_error(logger, f"Error al crear chat: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

