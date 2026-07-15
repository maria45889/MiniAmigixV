"""
Event DTOs

Data transfer objects for event-related operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EventDTO:
    """Event data transfer object."""
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    status: str = "scheduled"
    priority: str = "medium"
    reminder_minutes_before: Optional[int] = None
    is_all_day: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateEventDTO:
    """DTO for creating an event."""
    user_id: str
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    priority: str = "medium"
    reminder_minutes_before: Optional[int] = None
    is_all_day: bool = False


@dataclass
class UpdateEventDTO:
    """DTO for updating an event."""
    event_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    reminder_minutes_before: Optional[int] = None
    is_all_day: Optional[bool] = None
