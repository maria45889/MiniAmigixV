"""
Notification Domain Service

Business logic related to notifications.
"""

from typing import List
from ..entities.notification import Notification, NotificationType, NotificationPriority


class NotificationService:
    """
    Domain service for notification-related business logic.
    """
    
    @staticmethod
    def should_send_immediately(notification: Notification) -> bool:
        """
        Determine if notification should be sent immediately.
        
        Args:
            notification: Notification to check
            
        Returns:
            bool: True if should send immediately
        """
        return notification.is_high_priority() or notification.notification_type in [
            NotificationType.ERROR,
            NotificationType.WARNING
        ]
    
    @staticmethod
    def filter_unread(notifications: List[Notification]) -> List[Notification]:
        """
        Filter notifications to only include unread ones.
        
        Args:
            notifications: List of notifications
            
        Returns:
            List of unread notifications
        """
        return [n for n in notifications if not n.is_read]
    
    @staticmethod
    def filter_by_priority(
        notifications: List[Notification],
        priority: NotificationPriority
    ) -> List[Notification]:
        """
        Filter notifications by priority level.
        
        Args:
            notifications: List of notifications
            priority: Priority level to filter by
            
        Returns:
            List of notifications with specified priority
        """
        return [n for n in notifications if n.priority == priority]
    
    @staticmethod
    def remove_expired(notifications: List[Notification]) -> List[Notification]:
        """
        Remove expired notifications from list.
        
        Args:
            notifications: List of notifications
            
        Returns:
            List of non-expired notifications
        """
        return [n for n in notifications if not n.is_expired()]
