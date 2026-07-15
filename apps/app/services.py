"""
Business logic services.

Contains business logic separated from views for better organization.
"""

import logging
import base64
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple

import openai

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .constants import (
    SYSTEM_PROMPT_AUTHENTICATED,
    SYSTEM_PROMPT_UNAUTHENTICATED,
    DEFAULT_IMAGE_MESSAGE,
    CHAT_CONFIG,
    EVENT_CONFIG,
    DATETIME_FORMAT,
    DATE_FORMAT,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)
from .selectors import (
    ConversationSelectors,
    MessageSelectors,
    EventSelectors,
    NotificationSelectors,
    MusicSelectors,
    GameSelectors,
    StudySelectors
)

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-related operations."""
    
    @staticmethod
    def generate_ai_response(
        messages: List[Dict],
        settings_obj,
        imagen: bool = False,
        max_tokens: int = 500,
        image_base64: str = None,
        message: str = None
    ) -> str:
        """
        Generate AI response using available providers.
        
        Args:
            messages: List of message dictionaries
            settings_obj: Settings object with API keys
            imagen: Whether image processing is needed
            max_tokens: Maximum tokens for response
            image_base64: Base64 encoded image
            message: Text message
            
        Returns:
            AI response text
        """
        provider_configs = AIService._get_provider_configs(settings_obj, imagen)
        
        if not provider_configs:
            raise RuntimeError('No hay proveedores de IA configurados.')
        
        last_error = None
        for provider_name, client_kwargs, model, requires_image in provider_configs:
            current_messages = AIService._prepare_messages(
                messages, provider_name, imagen, image_base64, message
            )
            
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
        
        raise RuntimeError(
            f'No se pudo completar la respuesta con ningún proveedor de IA disponible. '
            f'Último error: {last_error}'
        ) from last_error
    
    @staticmethod
    def _get_provider_configs(settings_obj, imagen: bool) -> List[Tuple]:
        """Get available provider configurations."""
        configs = []
        
        if imagen and getattr(settings_obj, 'OPENAI_API_KEY', None):
            configs.append((
                'openai-vision',
                {'api_key': settings_obj.OPENAI_API_KEY},
                'gpt-4o',
                True,
            ))
        
        if getattr(settings_obj, 'GROQ_API_KEY', None):
            configs.append((
                'groq',
                {'api_key': settings_obj.GROQ_API_KEY, 'base_url': 'https://api.groq.com/openai/v1'},
                'llama-3.3-70b-versatile',
                False,
            ))
        
        if getattr(settings_obj, 'OPENAI_API_KEY', None):
            configs.append((
                'openai',
                {'api_key': settings_obj.OPENAI_API_KEY},
                'gpt-4o-mini',
                False,
            ))
        
        if getattr(settings_obj, 'OLLAMA_API_URL', None):
            configs.append((
                'ollama',
                {'base_url': settings_obj.OLLAMA_API_URL, 'api_key': 'ollama'},
                getattr(settings_obj, 'OLLAMA_MODEL', 'llama3.3'),
                False,
            ))
        
        return configs
    
    @staticmethod
    def _prepare_messages(
        messages: List[Dict],
        provider_name: str,
        imagen: bool,
        image_base64: str,
        message: str
    ) -> List[Dict]:
        """Prepare messages for specific provider."""
        current_messages = list(messages)
        
        if imagen and provider_name == 'openai-vision' and current_messages:
            if current_messages[-1].get('role') == 'user':
                last_content = current_messages[-1].get('content', '')
                if isinstance(last_content, list):
                    text_content = next(
                        (item.get('text', '') for item in last_content if item.get('type') == 'text'),
                        ''
                    )
                else:
                    text_content = last_content if isinstance(last_content, str) else str(last_content)
                
                current_messages[-1] = {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': text_content or (message or '')},
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f"data:image/jpeg;base64,{image_base64}" if image_base64 else 'data:image/jpeg;base64,'
                            }
                        }
                    ]
                }
        elif imagen and provider_name != 'openai-vision' and current_messages:
            if current_messages[-1].get('role') == 'user' and isinstance(current_messages[-1].get('content'), list):
                current_messages[-1] = {'role': 'user', 'content': message or ''}
        
        return current_messages
    
    @staticmethod
    def build_system_message(authenticated: bool, fecha_actual: str, eventos_contexto: str = "") -> str:
        """Build system message for AI."""
        if authenticated:
            return SYSTEM_PROMPT_AUTHENTICATED.format(
                fecha_actual=fecha_actual,
                eventos_contexto=eventos_contexto
            )
        else:
            return SYSTEM_PROMPT_UNAUTHENTICATED.format(fecha_actual=fecha_actual)


class ChatService:
    """Service for chat-related operations."""
    
    @staticmethod
    def get_or_create_conversation(user, conversation_id: str = None):
        """Get or create conversation for user."""
        if conversation_id:
            conversation = ConversationSelectors.get_by_user_and_id(user, conversation_id)
            if not conversation:
                return None, ERROR_MESSAGES['conversation_not_found']
            return conversation, None
        else:
            return ConversationSelectors.get_or_create_main(user), None
    
    @staticmethod
    def save_image(imagen) -> Optional[str]:
        """Save uploaded image and return URL."""
        try:
            fs = FileSystemStorage()
            filename = fs.save(f'{CHAT_CONFIG["image_upload_path"]}{imagen.name}', imagen)
            imagen_url = f'/media/{filename}'
            logger.info(f"Imagen guardada exitosamente: {imagen_url}")
            return imagen_url
        except Exception as e:
            logger.error(f"Error al guardar imagen: {str(e)}", exc_info=True)
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
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=EVENT_CONFIG['upcoming_days'])
        eventos = EventSelectors.get_upcoming_events(EVENT_CONFIG['upcoming_days'])
        
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
            eventos_proximos.append(
                f"- {evento.titulo} ({texto_dias}, {evento.fecha.strftime(DATE_FORMAT)})"
            )
        
        return "\n".join(eventos_proximos) if eventos_proximos else "No tienes eventos en los próximos 5 días."
    
    @staticmethod
    def create_chat_notification(user, response: str):
        """Create notification for chat response."""
        try:
            NotificationSelectors.create_for_user(
                user=user,
                title=CHAT_CONFIG['notification_title'],
                message=f'{CHAT_CONFIG["notification_message_prefix"]}{response[:100]}{CHAT_CONFIG["notification_message_suffix"]}',
                notification_type='info',
                link=CHAT_CONFIG['notification_link']
            )
        except Exception as e:
            logger.error(f"Error al crear notificación de chat: {str(e)}")


class EventService:
    """Service for event-related operations."""
    
    @staticmethod
    def get_upcoming_events_text(user, days: int = 3, limit: int = 3) -> List[Dict]:
        """Get upcoming events formatted for display."""
        hoy = date.today()
        eventos_proximos = EventSelectors.get_for_clock_widget(days, limit)
        eventos_texto = []
        
        for evento in eventos_proximos:
            dias_restantes = (evento.fecha - hoy).days
            if dias_restantes == 0:
                texto_dias = "hoy"
            elif dias_restantes == 1:
                texto_dias = "mañana"
            else:
                texto_dias = f"en {dias_restantes} días"
            
            eventos_texto.append({
                'titulo': evento.titulo,
                'texto_dias': texto_dias,
                'fecha': evento.fecha.strftime(DATE_FORMAT)
            })
        
        return eventos_texto


class StatisticsService:
    """Service for calculating statistics."""
    
    @staticmethod
    def get_user_statistics(user) -> Dict:
        """Get statistics for a user."""
        return {
            'chats': ConversationSelectors.get_all_by_user(user).count(),
            'notas': 0,
            'eventos': EventSelectors.count_all(),
            'canciones': MusicSelectors.count_songs(user)
        }


class MusicService:
    """Service for music-related operations."""
    
    @staticmethod
    def create_playlist(user, name: str, description: str = ''):
        """Create a new playlist."""
        if not name:
            return None, ERROR_MESSAGES['playlist_name_required']
        
        playlist = MusicSelectors.create_playlist(user, name, description)
        return playlist, None
    
    @staticmethod
    def add_song_to_playlist(playlist_id: int, song_id: int, user):
        """Add a song to a playlist."""
        try:
            playlist = MusicSelectors.get_playlist_by_id(playlist_id, user)
            cancion = MusicSelectors.get_song_by_id(song_id, user)
            playlist.canciones.add(cancion)
            playlist.save()
            return True, None
        except Exception as e:
            logger.error(f"Error al agregar canción a playlist: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def toggle_favorite(song_id: int, user):
        """Toggle favorite status for a song."""
        try:
            cancion = MusicSelectors.get_song_by_id(song_id, user)
            favorito, created = MusicSelectors.get_or_create_favorite(user, cancion)
            
            if not created:
                favorito.delete()
                return False, "Favorito eliminado"
            
            return True, "Agregado a favoritos"
        except Exception as e:
            logger.error(f"Error al toggle favorito: {str(e)}")
            return False, str(e)


class GameService:
    """Service for game-related operations."""
    
    @staticmethod
    def get_game_statistics(user) -> Dict:
        """Get game statistics for user."""
        puntuaciones_usuario = GameSelectors.get_scores(user)
        logros_usuario = GameSelectors.get_achievements(user)
        
        mejor_puntuacion = 0
        total_juegos = 0
        
        if puntuaciones_usuario:
            mejor_puntuacion = max(p.puntuacion for p in puntuaciones_usuario)
            total_juegos = puntuaciones_usuario.count()
        
        ultimo_juego = puntuaciones_usuario.first() if puntuaciones_usuario else None
        
        return {
            'mejor_puntuacion': mejor_puntuacion,
            'total_juegos': total_juegos,
            'ultimo_juego': ultimo_juego,
            'total_logros': logros_usuario.count()
        }


class StudyService:
    """Service for study-related operations."""
    
    @staticmethod
    def get_study_data(user) -> Dict:
        """Get study data for user."""
        categorias = StudySelectors.get_all_categories()
        recursos_usuario = StudySelectors.get_resources(user) if user.is_authenticated else []
        progreso_usuario = StudySelectors.get_progress(user) if user.is_authenticated else []
        
        return {
            'categorias': categorias,
            'recursos': recursos_usuario,
            'progreso': progreso_usuario
        }


class DateTimeService:
    """Service for date/time operations."""
    
    @staticmethod
    def get_current_datetime_formatted() -> str:
        """Get current date and time formatted."""
        return datetime.now().strftime(DATETIME_FORMAT)
    
    @staticmethod
    def get_current_date_formatted() -> str:
        """Get current date formatted."""
        return date.today().strftime(DATE_FORMAT)
    
    @staticmethod
    def generate_chat_timestamp() -> str:
        """Generate timestamp for chat title."""
        return datetime.now().strftime("%H:%M")


class ValidationService:
    """Service for validation operations."""
    
    @staticmethod
    def validate_chat_request(message: str, imagen) -> Tuple[bool, str]:
        """Validate chat request."""
        if not message and not imagen:
            return False, ERROR_MESSAGES['no_message']
        
        if not message and imagen:
            return True, DEFAULT_IMAGE_MESSAGE
        
        return True, message
