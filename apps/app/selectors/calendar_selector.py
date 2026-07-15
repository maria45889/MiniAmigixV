"""
Calendar selector.

Database queries for calendar operations.
"""

from eventos.models import Evento


class CalendarSelector:
    """Selector for calendar-related queries."""
    
    @staticmethod
    def get_upcoming_events(days: int = 5):
        """Get events in the next N days."""
        from datetime import date, timedelta
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=days)
        return Evento.objects.filter(fecha__gte=hoy, fecha__lte=fecha_limite).order_by('fecha')
    
    @staticmethod
    def get_for_clock_widget(days: int = 3, limit: int = 3):
        """Get events for the clock widget."""
        return CalendarSelector.get_upcoming_events(days)[:limit]
    
    @staticmethod
    def count_all():
        """Count all events."""
        return Evento.objects.count()
    
    @staticmethod
    def get_events_in_range(start_date, end_date):
        """Get events within a date range."""
        return Evento.objects.filter(fecha__gte=start_date, fecha__lte=end_date).order_by('fecha')
