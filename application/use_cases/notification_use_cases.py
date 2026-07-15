"""
Notification Use Cases

Application use cases for notification-related operations.
"""

from dataclasses import dataclass
from typing import Optional

from .base_use_case import UseCase, UseCaseRequest, UseCaseResponse
from application.dto.notification_dto import NotificationDTO
from infrastructure.repositories.notification_repository import NotificationRepository
from core.entities.notification import Notification, NotificationType, NotificationPriority
from core.services.notification_service import NotificationService


@dataclass
class CreateNotificationRequest(UseCaseRequest):
    """Request for creating a notification."""
    user_id: str
    title: str
    message: str
    notification_type: str = "info"
    priority: str = "medium"
    action_url: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class MarkNotificationAsReadRequest(UseCaseRequest):
    """Request for marking a notification as read."""
    notification_id: str
    user_id: str


@dataclass
class ListNotificationsRequest(UseCaseRequest):
    """Request for listing notifications."""
    user_id: str
    unread_only: bool = False


class CreateNotificationUseCase(UseCase[CreateNotificationRequest, UseCaseResponse]):
    """Use case for creating a notification."""
    
    def __init__(self, repository: NotificationRepository):
        self.repository = repository
    
    def execute(self, request: CreateNotificationRequest) -> UseCaseResponse:
        """Execute the create notification use case."""
        try:
            notification_type = NotificationType(request.notification_type)
            priority = NotificationPriority(request.priority)
        except ValueError:
            return self.create_error_response("Invalid notification type or priority")
        
        notification = Notification(
            user_id=request.user_id,
            title=request.title,
            message=request.message,
            notification_type=notification_type,
            priority=priority,
            action_url=request.action_url,
            metadata=request.metadata
        )
        
        if not notification.validate():
            return self.create_error_response("Invalid notification data")
        
        saved_notification = self.repository.save(notification)
        
        return self.create_success_response(
            "Notification created successfully",
            {
                "id": saved_notification.id,
                "user_id": saved_notification.user_id,
                "title": saved_notification.title,
                "message": saved_notification.message,
                "notification_type": saved_notification.notification_type.value,
                "priority": saved_notification.priority.value
            }
        )


class MarkNotificationAsReadUseCase(UseCase[MarkNotificationAsReadRequest, UseCaseResponse]):
    """Use case for marking a notification as read."""
    
    def __init__(self, repository: NotificationRepository):
        self.repository = repository
    
    def execute(self, request: MarkNotificationAsReadRequest) -> UseCaseResponse:
        """Execute the mark as read use case."""
        notification = self.repository.find_by_id(request.notification_id)
        
        if not notification:
            return self.create_error_response("Notification not found")
        
        if notification.user_id != request.user_id:
            return self.create_error_response("Access denied")
        
        notification.mark_as_read()
        self.repository.save(notification)
        
        return self.create_success_response(
            "Notification marked as read",
            {
                "id": notification.id,
                "is_read": notification.is_read
            }
        )


class ListNotificationsUseCase(UseCase[ListNotificationsRequest, UseCaseResponse]):
    """Use case for listing notifications."""
    
    def __init__(self, repository: NotificationRepository):
        self.repository = repository
    
    def execute(self, request: ListNotificationsRequest) -> UseCaseResponse:
        """Execute the list notifications use case."""
        if request.unread_only:
            notifications = self.repository.find_unread(request.user_id)
        else:
            notifications = self.repository.find_by_user_id(request.user_id)
        
        # Remove expired notifications
        notifications = NotificationService.remove_expired(notifications)
        
        notifications_data = [
            {
                "id": notif.id,
                "title": notif.title,
                "message": notif.message,
                "notification_type": notif.notification_type.value,
                "priority": notif.priority.value,
                "is_read": notif.is_read,
                "action_url": notif.action_url,
                "created_at": notif.created_at.isoformat() if notif.created_at else None
            }
            for notif in notifications
        ]
        
        return self.create_success_response(
            "Notifications retrieved successfully",
            {"notifications": notifications_data}
        )
