"""
Weather API integration.

Service for interacting with weather APIs like OpenWeatherMap.
"""

import logging
import requests

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for weather API interactions."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize weather service.
        
        Args:
            api_key: Weather API key (OpenWeatherMap)
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, location: str, units: str = "metric") -> dict:
        """
        Get current weather for a location.
        
        Args:
            location: City name or coordinates
            units: Units system ('metric', 'imperial', 'kelvin')
            
        Returns:
            Dictionary with weather data
        """
        if not self.api_key:
            raise RuntimeError("Weather API key not configured")
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'location': data['name'],
                'country': data['sys']['country'],
                'icon': data['weather'][0]['icon']
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            raise
        except KeyError as e:
            logger.error(f"Error parsing weather data: {e}")
            raise
    
    def get_forecast(self, location: str, days: int = 5, units: str = "metric") -> list:
        """
        Get weather forecast for a location.
        
        Args:
            location: City name or coordinates
            days: Number of days to forecast
            units: Units system ('metric', 'imperial', 'kelvin')
            
        Returns:
            List of forecast data dictionaries
        """
        if not self.api_key:
            raise RuntimeError("Weather API key not configured")
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': units,
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            forecasts = []
            
            for item in data['list']:
                forecasts.append({
                    'datetime': item['dt'],
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'icon': item['weather'][0]['icon']
                })
            
            return forecasts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching forecast data: {e}")
            raise
        except KeyError as e:
            logger.error(f"Error parsing forecast data: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if the service is available."""
        return self.api_key is not None
