"""
Event API Views

API endpoints for event and calendar operations.
"""

from django.http import JsonResponse

from .base_view import BaseAPIView
from application.use_cases.event_use_cases import (
    CreateEventUseCase,
    UpdateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    DeleteEventUseCase
)
from application.dto.event_dto import CreateEventDTO, UpdateEventDTO
from infrastructure.repositories.event_repository import EventRepository


class EventViewSet(BaseAPIView):
    """
    API viewset for event operations.
    """
    
    def __init__(self):
        super().__init__()
        self.event_repository = EventRepository()
        self.create_event_use_case = CreateEventUseCase(self.event_repository)
        self.get_event_use_case = GetEventUseCase(self.event_repository)
        self.update_event_use_case = UpdateEventUseCase(self.event_repository)
        self.list_events_use_case = ListEventsUseCase(self.event_repository)
        self.delete_event_use_case = DeleteEventUseCase(self.event_repository)
    
    def get(self, request, event_id: str = None) -> JsonResponse:
        """
        Get event(s).
        
        Args:
            request: HTTP request
            event_id: Optional event ID
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        user_id = str(request.user.id)
        
        if event_id:
            # Get single event
            response = self.get_event_use_case.execute(
                type('Request', (), {'event_id': event_id, 'user_id': user_id})()
            )
            if response.success:
                return self.success_response(response.data, response.message)
            return self.not_found_response(response.message)
        else:
            # List all events for user
            response = self.list_events_use_case.execute(
                type('Request', (), {'user_id': user_id})()
            )
            return self.success_response(response.data, response.message)
    
    def post(self, request) -> JsonResponse:
        """
        Create a new event.
        
        Args:
            request: HTTP request
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        from datetime import datetime
        import json
        data = json.loads(request.body)
        
        dto = CreateEventDTO(
            user_id=str(request.user.id),
            title=data.get('title'),
            description=data.get('description'),
            start_time=self._parse_datetime(data.get('start_time')),
            end_time=self._parse_datetime(data.get('end_time')),
            location=data.get('location'),
            priority=data.get('priority', 'medium'),
            reminder_minutes_before=data.get('reminder_minutes_before'),
            is_all_day=data.get('is_all_day', False)
        )
        
        response = self.create_event_use_case.execute(dto)
        
        if response.success:
            return self.success_response(response.data, response.message, status=201)
        return self.error_response(response.message, response.errors)
    
    def put(self, request, event_id: str) -> JsonResponse:
        """
        Update an event.
        
        Args:
            request: HTTP request
            event_id: Event ID to update
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        from datetime import datetime
        import json
        data = json.loads(request.body)
        
        dto = UpdateEventDTO(
            event_id=event_id,
            title=data.get('title'),
            description=data.get('description'),
            start_time=self._parse_datetime(data.get('start_time')),
            end_time=self._parse_datetime(data.get('end_time')),
            location=data.get('location'),
            status=data.get('status'),
            priority=data.get('priority'),
            reminder_minutes_before=data.get('reminder_minutes_before'),
            is_all_day=data.get('is_all_day')
        )
        
        response = self.update_event_use_case.execute(dto)
        
        if response.success:
            return self.success_response(response.data, response.message)
        return self.error_response(response.message, response.errors)
    
    def delete(self, request, event_id: str) -> JsonResponse:
        """
        Delete an event.
        
        Args:
            request: HTTP request
            event_id: Event ID to delete
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        response = self.delete_event_use_case.execute(
            type('Request', (), {'event_id': event_id, 'user_id': str(request.user.id)})()
        )
        
        if response.success:
            return self.success_response(None, response.message)
        return self.error_response(response.message)
    
    def _parse_datetime(self, datetime_str: str):
        """Parse datetime string to datetime object."""
        if not datetime_str:
            return None
        from datetime import datetime
        try:
            return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
