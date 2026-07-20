"""
OpenAI API integration.
"""

import logging
import openai
from typing import List, Dict

logger = logging.getLogger(__name__)


class OpenAIAPI:
    """Service for OpenAI API interactions."""
    
    @staticmethod
    def generate_response(
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
        provider_configs = OpenAIAPI._get_provider_configs(settings_obj, imagen)
        
        if not provider_configs:
            raise RuntimeError('No hay proveedores de IA configurados.')
        
        last_error = None
        for provider_name, client_kwargs, model, requires_image in provider_configs:
            current_messages = OpenAIAPI._prepare_messages(
                messages, provider_name, imagen, image_base64, message
            )
            
            try:
                client = openai.OpenAI(**client_kwargs)
                logger.info(f'Llamando a proveedor {provider_name} con modelo {model}')
                response = client.chat.completions.create(
                    model=model,
                    messages=current_messages,
                    max_tokens=max_tokens,
                    timeout=30.0,
                )
                logger.info(f'Respuesta recibida de {provider_name}')
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
    def _get_provider_configs(settings_obj, imagen: bool) -> List[tuple]:
        """Get available provider configurations."""
        configs = []

        # Priorizar Groq (más rápido)
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

        if imagen and getattr(settings_obj, 'OPENAI_API_KEY', None):
            configs.append((
                'openai-vision',
                {'api_key': settings_obj.OPENAI_API_KEY},
                'gpt-4o',
                True,
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
