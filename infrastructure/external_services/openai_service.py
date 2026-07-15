"""
OpenAI Service

Service for interacting with OpenAI API.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import os


class OpenAIServiceInterface(ABC):
    """Interface for AI service."""
    
    @abstractmethod
    def generate_response(self, prompt: str, conversation_history: List[dict] = None) -> str:
        """Generate a response from the AI."""
        pass


class OpenAIService(OpenAIServiceInterface):
    """
    Concrete implementation of AI service using OpenAI.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI service.
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("OpenAI package not installed. AI features will be limited.")
    
    def generate_response(self, prompt: str, conversation_history: List[dict] = None) -> str:
        """
        Generate a response from OpenAI.
        
        Args:
            prompt: User's prompt
            conversation_history: Previous messages in the conversation
            
        Returns:
            Generated response text
        """
        if not self.client:
            return "AI service not available. Please configure OpenAI API key."
        
        try:
            messages = []
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if the service is available."""
        return self.client is not None
