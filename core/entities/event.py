"""
Event Entity

Represents an event in the calendar/agenda system.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from .base_entity import BaseEntity


class EventStatus(Enum):
    """Event status."""
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    POSTPONED = "postponed"


class EventPriority(Enum):
    """Event priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Event(BaseEntity):
    """
    Event domain entity for calendar/agenda.
    """
    user_id: str
    title: str
    description: Optional[str] = None
    start_time: datetime = None
    end_time: datetime = None
    location: Optional[str] = None
    status: EventStatus = EventStatus.SCHEDULED
    priority: EventPriority = EventPriority.MEDIUM
    reminder_minutes_before: Optional[int] = None
    is_all_day: bool = False
    
    def validate(self) -> bool:
        """Validate event entity."""
        if not self.user_id:
            return False
        if not self.title or len(self.title) < 1:
            return False
        if not self.is_all_day and (not self.start_time or not self.end_time):
            return False
        if self.start_time and self.end_time and self.start_time > self.end_time:
            return False
        return True
    
    def is_upcoming(self) -> bool:
        """Check if event is upcoming."""
        if not self.start_time:
            return False
        return self.start_time > datetime.utcnow()
    
    def is_past(self) -> bool:
        """Check if event is in the past."""
        if not self.end_time:
            return False
        return self.end_time < datetime.utcnow()
    
    def cancel(self):
        """Cancel the event."""
        self.status = EventStatus.CANCELLED
        self.mark_as_updated()
    
    def complete(self):
        """Mark event as completed."""
        self.status = EventStatus.COMPLETED
        self.mark_as_updated()
    
    def postpone(self):
        """Postpone the event."""
        self.status = EventStatus.POSTPONED
        self.mark_as_updated()
