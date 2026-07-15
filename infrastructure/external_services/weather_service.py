"""
Weather Service

Service for interacting with weather APIs.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class WeatherData:
    """Weather data structure."""
    temperature: float
    humidity: int
    description: str
    wind_speed: float
    location: str
    icon: Optional[str] = None


class WeatherServiceInterface(ABC):
    """Interface for weather service."""
    
    @abstractmethod
    def get_current_weather(self, location: str) -> Optional[WeatherData]:
        """Get current weather for a location."""
        pass
    
    @abstractmethod
    def get_forecast(self, location: str, days: int = 5) -> list:
        """Get weather forecast for a location."""
        pass


class WeatherService(WeatherServiceInterface):
    """
    Concrete implementation of weather service using OpenWeatherMap.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the weather service.
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
    
    def get_current_weather(self, location: str) -> Optional[WeatherData]:
        """
        Get current weather for a location.
        
        Args:
            location: City name or coordinates
            
        Returns:
            WeatherData object or None if error
        """
        if not self.api_key:
            return None
        
        try:
            import requests
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return WeatherData(
                temperature=data['main']['temp'],
                humidity=data['main']['humidity'],
                description=data['weather'][0]['description'],
                wind_speed=data['wind']['speed'],
                location=data['name'],
                icon=data['weather'][0]['icon']
            )
            
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    def get_forecast(self, location: str, days: int = 5) -> list:
        """
        Get weather forecast for a location.
        
        Args:
            location: City name or coordinates
            days: Number of days to forecast
            
        Returns:
            List of WeatherData objects
        """
        if not self.api_key:
            return []
        
        try:
            import requests
            url = f"http://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            forecasts = []
            
            for item in data['list']:
                forecasts.append(WeatherData(
                    temperature=item['main']['temp'],
                    humidity=item['main']['humidity'],
                    description=item['weather'][0]['description'],
                    wind_speed=item['wind']['speed'],
                    location=data['city']['name'],
                    icon=item['weather'][0]['icon']
                ))
            
            return forecasts
            
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if the service is available."""
        return self.api_key is not None
