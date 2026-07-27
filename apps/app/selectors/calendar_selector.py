"""
Calendar selector.

Database queries for calendar operations.
"""

from apps.eventos.models import Evento


class CalendarSelector:
    """Selector for calendar-related queries."""
    
    @staticmethod
    def get_upcoming_events(days: int = 5):
        """Get events in the next N days."""
        from datetime import timedelta
        from django.utils import timezone
        ahora = timezone.now()
        inicio_hoy = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_limite = inicio_hoy + timedelta(days=days, hours=23, minutes=59, seconds=59)
        return Evento.objects.filter(fecha__gte=inicio_hoy, fecha__lte=fecha_limite).order_by('fecha')
    
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
