"""
Selectors module.

Contains database query selectors for different domains.
"""

from .auth_selector import AuthSelector
from .chat_selector import ChatSelector
from .music_selector import MusicSelector
from .weather_selector import WeatherSelector
from .study_selector import StudySelector
from .entertainment_selector import EntertainmentSelector
from .calendar_selector import CalendarSelector
from .user_selector import UserSelector
from .notification_selector import NotificationSelector

__all__ = [
    'AuthSelector',
    'ChatSelector',
    'MusicSelector',
    'WeatherSelector',
    'StudySelector',
    'EntertainmentSelector',
    'CalendarSelector',
    'UserSelector',
    'NotificationSelector'
]
