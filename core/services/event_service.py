"""
Event Domain Service

Business logic related to events and calendar.
"""

from datetime import datetime, timedelta
from typing import List
from ..entities.event import Event, EventStatus, EventPriority


class EventService:
    """
    Domain service for event-related business logic.
    """
    
    @staticmethod
    def get_upcoming_events(events: List[Event]) -> List[Event]:
        """
        Filter events to only include upcoming ones.
        
        Args:
            events: List of events
            
        Returns:
            List of upcoming events
        """
        return [e for e in events if e.is_upcoming() and e.status == EventStatus.SCHEDULED]
    
    @staticmethod
    def get_events_for_date(events: List[Event], date: datetime) -> List[Event]:
        """
        Get events for a specific date.
        
        Args:
            events: List of events
            date: Date to filter by
            
        Returns:
            List of events for the date
        """
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        return [
            e for e in events
            if e.start_time and start_of_day <= e.start_time < end_of_day
        ]
    
    @staticmethod
    def has_conflict(event: Event, existing_events: List[Event]) -> bool:
        """
        Check if event conflicts with existing events.
        
        Args:
            event: Event to check
            existing_events: List of existing events
            
        Returns:
            bool: True if there's a conflict
        """
        if not event.start_time or not event.end_time:
            return False
        
        for existing in existing_events:
            if (existing.status == EventStatus.CANCELLED or
                not existing.start_time or not existing.end_time):
                continue
            
            # Check for overlap
            if (event.start_time < existing.end_time and
                event.end_time > existing.start_time):
                return True
        
        return False
    
    @staticmethod
    def get_urgent_events(events: List[Event]) -> List[Event]:
        """
        Get events with urgent priority.
        
        Args:
            events: List of events
            
        Returns:
            List of urgent events
        """
        return [e for e in events if e.priority == EventPriority.URGENT]
