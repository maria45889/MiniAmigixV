"""
Calendar service.

Business logic for calendar and event operations.
"""

import logging
from datetime import date, timedelta
from typing import List, Dict

from ..selectors.calendar_selector import CalendarSelector
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class CalendarService:
    """Service for calendar-related operations."""
    
    @staticmethod
    def get_upcoming_events_text(user, days: int = 3, limit: int = 3) -> List[Dict]:
        """Get upcoming events formatted for display."""
        hoy = date.today()
        eventos_proximos = CalendarSelector.get_for_clock_widget(days, limit)
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
                'fecha': evento.fecha.strftime('%d/%m/%Y')
            })
        
        return eventos_texto
    
    @staticmethod
    def get_events_in_range(start_date: date, end_date: date):
        """Get events within a date range."""
        return CalendarSelector.get_events_in_range(start_date, end_date)
