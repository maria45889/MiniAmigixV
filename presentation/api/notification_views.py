"""
Notification API Views

API endpoints for notification operations.
"""

from django.http import JsonResponse

from .base_view import BaseAPIView
from application.use_cases.notification_use_cases import (
    CreateNotificationUseCase,
    MarkNotificationAsReadUseCase,
    ListNotificationsUseCase
)
from application.dto.notification_dto import NotificationDTO
from infrastructure.repositories.notification_repository import NotificationRepository


class NotificationViewSet(BaseAPIView):
    """
    API viewset for notification operations.
    """
    
    def __init__(self):
        super().__init__()
        self.notification_repository = NotificationRepository()
        self.create_notification_use_case = CreateNotificationUseCase(self.notification_repository)
        self.list_notifications_use_case = ListNotificationsUseCase(self.notification_repository)
        self.mark_as_read_use_case = MarkNotificationAsReadUseCase(self.notification_repository)
    
    def get(self, request) -> JsonResponse:
        """
        Get notifications for the current user.
        
        Args:
            request: HTTP request
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        user_id = str(request.user.id)
        unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
        
        response = self.list_notifications_use_case.execute(
            type('Request', (), {'user_id': user_id, 'unread_only': unread_only})()
        )
        
        return self.success_response(response.data, response.message)
    
    def post(self, request) -> JsonResponse:
        """
        Create a new notification (admin only).
        
        Args:
            request: HTTP request
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated or not request.user.is_staff:
            return self.forbidden_response()
        
        import json
        data = json.loads(request.body)
        
        dto = NotificationDTO(
            id=None,
            user_id=data.get('user_id'),
            title=data.get('title'),
            message=data.get('message'),
            notification_type=data.get('notification_type', 'info'),
            priority=data.get('priority', 'medium'),
            action_url=data.get('action_url'),
            metadata=data.get('metadata')
        )
        
        response = self.create_notification_use_case.execute(dto)
        
        if response.success:
            return self.success_response(response.data, response.message, status=201)
        return self.error_response(response.message, response.errors)
    
    def put(self, request, notification_id: str) -> JsonResponse:
        """
        Mark a notification as read.
        
        Args:
            request: HTTP request
            notification_id: Notification ID
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        response = self.mark_as_read_use_case.execute(
            type('Request', (), {
                'notification_id': notification_id,
                'user_id': str(request.user.id)
            })()
        )
        
        if response.success:
            return self.success_response(response.data, response.message)
        return self.error_response(response.message)
