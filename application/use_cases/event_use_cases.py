"""
Event Use Cases

Application use cases for event-related operations.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .base_use_case import UseCase, UseCaseRequest, UseCaseResponse
from application.dto.event_dto import CreateEventDTO, UpdateEventDTO
from infrastructure.repositories.event_repository import EventRepository
from core.entities.event import Event, EventStatus, EventPriority
from core.services.event_service import EventService


@dataclass
class CreateEventRequest(UseCaseRequest):
    """Request for creating an event."""
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
class UpdateEventRequest(UseCaseRequest):
    """Request for updating an event."""
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


@dataclass
class GetEventRequest(UseCaseRequest):
    """Request for getting an event."""
    event_id: str
    user_id: str


@dataclass
class ListEventsRequest(UseCaseRequest):
    """Request for listing events."""
    user_id: str
    upcoming_only: bool = False


@dataclass
class DeleteEventRequest(UseCaseRequest):
    """Request for deleting an event."""
    event_id: str
    user_id: str


class CreateEventUseCase(UseCase[CreateEventRequest, UseCaseResponse]):
    """Use case for creating an event."""
    
    def __init__(self, repository: EventRepository):
        self.repository = repository
    
    def execute(self, request: CreateEventRequest) -> UseCaseResponse:
        """Execute the create event use case."""
        try:
            priority = EventPriority(request.priority)
        except ValueError:
            return self.create_error_response("Invalid priority value")
        
        event = Event(
            user_id=request.user_id,
            title=request.title,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            location=request.location,
            priority=priority,
            reminder_minutes_before=request.reminder_minutes_before,
            is_all_day=request.is_all_day
        )
        
        if not event.validate():
            return self.create_error_response("Invalid event data")
        
        saved_event = self.repository.save(event)
        
        return self.create_success_response(
            "Event created successfully",
            {
                "id": saved_event.id,
                "user_id": saved_event.user_id,
                "title": saved_event.title,
                "start_time": saved_event.start_time.isoformat() if saved_event.start_time else None,
                "end_time": saved_event.end_time.isoformat() if saved_event.end_time else None
            }
        )


class UpdateEventUseCase(UseCase[UpdateEventRequest, UseCaseResponse]):
    """Use case for updating an event."""
    
    def __init__(self, repository: EventRepository):
        self.repository = repository
    
    def execute(self, request: UpdateEventRequest) -> UseCaseResponse:
        """Execute the update event use case."""
        event = self.repository.find_by_id(request.event_id)
        
        if not event:
            return self.create_error_response("Event not found")
        
        # Update fields
        if request.title is not None:
            event.title = request.title
        if request.description is not None:
            event.description = request.description
        if request.start_time is not None:
            event.start_time = request.start_time
        if request.end_time is not None:
            event.end_time = request.end_time
        if request.location is not None:
            event.location = request.location
        if request.status is not None:
            try:
                event.status = EventStatus(request.status)
            except ValueError:
                return self.create_error_response("Invalid status value")
        if request.priority is not None:
            try:
                event.priority = EventPriority(request.priority)
            except ValueError:
                return self.create_error_response("Invalid priority value")
        if request.reminder_minutes_before is not None:
            event.reminder_minutes_before = request.reminder_minutes_before
        if request.is_all_day is not None:
            event.is_all_day = request.is_all_day
        
        if not event.validate():
            return self.create_error_response("Invalid event data")
        
        saved_event = self.repository.save(event)
        
        return self.create_success_response(
            "Event updated successfully",
            {
                "id": saved_event.id,
                "title": saved_event.title,
                "status": saved_event.status.value,
                "priority": saved_event.priority.value
            }
        )


class GetEventUseCase(UseCase[GetEventRequest, UseCaseResponse]):
    """Use case for getting an event."""
    
    def __init__(self, repository: EventRepository):
        self.repository = repository
    
    def execute(self, request: GetEventRequest) -> UseCaseResponse:
        """Execute the get event use case."""
        event = self.repository.find_by_id(request.event_id)
        
        if not event:
            return self.create_error_response("Event not found")
        
        if event.user_id != request.user_id:
            return self.create_error_response("Access denied")
        
        return self.create_success_response(
            "Event retrieved successfully",
            {
                "id": event.id,
                "user_id": event.user_id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat() if event.start_time else None,
                "end_time": event.end_time.isoformat() if event.end_time else None,
                "location": event.location,
                "status": event.status.value,
                "priority": event.priority.value,
                "reminder_minutes_before": event.reminder_minutes_before,
                "is_all_day": event.is_all_day
            }
        )


class ListEventsUseCase(UseCase[ListEventsRequest, UseCaseResponse]):
    """Use case for listing events."""
    
    def __init__(self, repository: EventRepository):
        self.repository = repository
    
    def execute(self, request: ListEventsRequest) -> UseCaseResponse:
        """Execute the list events use case."""
        if request.upcoming_only:
            events = self.repository.find_upcoming(request.user_id)
        else:
            events = self.repository.find_by_user_id(request.user_id)
        
        events_data = [
            {
                "id": event.id,
                "title": event.title,
                "start_time": event.start_time.isoformat() if event.start_time else None,
                "end_time": event.end_time.isoformat() if event.end_time else None,
                "status": event.status.value,
                "priority": event.priority.value,
                "is_all_day": event.is_all_day
            }
            for event in events
        ]
        
        return self.create_success_response(
            "Events retrieved successfully",
            {"events": events_data}
        )


class DeleteEventUseCase(UseCase[DeleteEventRequest, UseCaseResponse]):
    """Use case for deleting an event."""
    
    def __init__(self, repository: EventRepository):
        self.repository = repository
    
    def execute(self, request: DeleteEventRequest) -> UseCaseResponse:
        """Execute the delete event use case."""
        event = self.repository.find_by_id(request.event_id)
        
        if not event:
            return self.create_error_response("Event not found")
        
        if event.user_id != request.user_id:
            return self.create_error_response("Access denied")
        
        success = self.repository.delete(request.event_id)
        
        if success:
            return self.create_success_response("Event deleted successfully")
        return self.create_error_response("Failed to delete event")
