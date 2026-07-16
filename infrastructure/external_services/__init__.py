"""
External Services

Services that interact with external APIs and systems.
These are infrastructure concerns that the domain layer depends on.
"""

from .base_service import ExternalService
from .openai_service import OpenAIService
from .weather_service import WeatherService
from .email_service import EmailService

__all__ = ['ExternalService', 'OpenAIService', 'WeatherService', 'EmailService']
