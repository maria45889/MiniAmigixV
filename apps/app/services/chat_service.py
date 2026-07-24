"""
Chat service.

Business logic for chat operations.
"""

import logging
import base64
from typing import List, Dict, Optional

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from ..constants.chat import (
    CHAT_CONFIG,
    EVENT_CONFIG,
    DEFAULT_IMAGE_MESSAGE
)
from ..selectors.chat_selector import ChatSelector
from ..selectors.calendar_selector import CalendarSelector
from ..selectors.notification_selector import NotificationSelector
from ..api.openai_api import OpenAIAPI
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class ChatService:
    """Service for chat-related operations."""
    
    @staticmethod
    def get_or_create_conversation(user, conversation_id: str = None):
        """Get or create conversation for user."""
        if conversation_id:
            conversation = ChatSelector.get_by_user_and_id(user, conversation_id)
            if not conversation:
                return None, "Conversation not found"
            return conversation, None
        else:
            return ChatSelector.get_or_create_main(user), None
    
    @staticmethod
    def save_image(imagen) -> Optional[str]:
        """Save uploaded image and return URL."""
        try:
            fs = FileSystemStorage()
            filename = fs.save(f'{CHAT_CONFIG["image_upload_path"]}{imagen.name}', imagen)
            imagen_url = f'/media/{filename}'
            LogHelper.log_info(logger, f"Imagen guardada exitosamente: {imagen_url}")
            return imagen_url
        except Exception as e:
            LogHelper.log_error(logger, f"Error al guardar imagen: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def convert_image_to_base64(imagen) -> str:
        """Convert image to base64 string."""
        image_data = imagen.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        imagen.seek(0)
        return image_base64
    
    @staticmethod
    def get_events_context(user) -> str:
        """Get formatted context of upcoming events."""
        eventos_proximos = []
        from django.utils import timezone
        hoy = timezone.now().date()
        eventos = CalendarSelector.get_upcoming_events(EVENT_CONFIG['upcoming_days'])
        
        for evento in eventos:
            evento_fecha = evento.fecha.date() if hasattr(evento.fecha, 'date') else evento.fecha
            dias_restantes = (evento_fecha - hoy).days
            if dias_restantes == 0:
                texto_dias = "hoy"
            elif dias_restantes == 1:
                texto_dias = "mañana"
            elif dias_restantes <= 3:
                texto_dias = f"en {dias_restantes} días"
            else:
                texto_dias = f"en {dias_restantes} días"
            eventos_proximos.append(
                f"- {evento.titulo} ({texto_dias}, {evento.fecha.strftime('%d/%m/%Y')})"
            )
        
        return "\n".join(eventos_proximos) if eventos_proximos else "No tienes eventos en los próximos 5 días."
    
    @staticmethod
    def create_chat_notification(user, response: str):
        """Create notification for chat response."""
        try:
            NotificationSelector.create_for_user(
                user=user,
                title=CHAT_CONFIG['notification_title'],
                message=f'{CHAT_CONFIG["notification_message_prefix"]}{response[:100]}{CHAT_CONFIG["notification_message_suffix"]}',
                notification_type='info',
                link=CHAT_CONFIG['notification_link']
            )
        except Exception as e:
            LogHelper.log_error(logger, f"Error al crear notificación de chat: {str(e)}")
    
    @staticmethod
    def generate_ai_response(
        messages: List[Dict],
        settings_obj,
        imagen: bool = False,
        max_tokens: int = 500,
        image_base64: str = None,
        message: str = None
    ) -> str:
        """Generate AI response using OpenAI API."""
        return OpenAIAPI.generate_response(
            messages=messages,
            settings_obj=settings_obj,
            imagen=imagen,
            max_tokens=max_tokens,
            image_base64=image_base64,
            message=message
        )
