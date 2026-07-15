"""
API module.

Contains external API integrations.
"""

from .openai_api import OpenAIAPI
from .weather_api import WeatherAPI
from .youtube_api import YouTubeAPI
from .spotify_api import SpotifyAPI
from .gemini_api import GeminiAPI
from .translator_api import TranslatorAPI

__all__ = [
    'OpenAIAPI',
    'WeatherAPI',
    'YouTubeAPI',
    'SpotifyAPI',
    'GeminiAPI',
    'TranslatorAPI'
]
