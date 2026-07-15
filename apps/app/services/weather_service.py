"""
Weather service.

Business logic for weather operations.
"""

import logging
from typing import Optional, Dict

from ..api.weather_api import WeatherAPI
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for weather-related operations."""
    
    @staticmethod
    def get_current_weather(location: str, units: str = "metric") -> Optional[Dict]:
        """Get current weather for a location."""
        try:
            return WeatherAPI.get_current_weather(location, units)
        except Exception as e:
            LogHelper.log_error(logger, f"Error al obtener clima: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def get_forecast(location: str, days: int = 5, units: str = "metric") -> Optional[list]:
        """Get weather forecast for a location."""
        try:
            return WeatherAPI.get_forecast(location, days, units)
        except Exception as e:
            LogHelper.log_error(logger, f"Error al obtener pronóstico: {str(e)}", exc_info=True)
            return None
