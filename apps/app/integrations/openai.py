"""
OpenAI API integration.

Service for interacting with OpenAI API for AI responses.
"""

import logging
import openai

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key
            base_url: Custom base URL (for alternative providers like Groq)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.client = None
        
        if api_key:
            client_kwargs = {'api_key': api_key}
            if base_url:
                client_kwargs['base_url'] = base_url
            
            try:
                self.client = openai.OpenAI(**client_kwargs)
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {e}")
    
    def generate_chat_response(
        self,
        messages: list,
        model: str = "gpt-4o-mini",
        max_tokens: int = 500
    ) -> str:
        """
        Generate a chat response.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text
        """
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            raise
    
    def generate_vision_response(
        self,
        messages: list,
        model: str = "gpt-4o",
        max_tokens: int = 500
    ) -> str:
        """
        Generate a response with vision capabilities.
        
        Args:
            messages: List of message dictionaries (can include image URLs)
            model: Model to use (must support vision)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text
        """
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating vision response: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if the service is available."""
        return self.client is not None
