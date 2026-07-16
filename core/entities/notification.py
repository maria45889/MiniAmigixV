"""
Notification Entity

Represents a notification in the system.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Any

from .base_entity import BaseEntity


class NotificationType(Enum):
    """Notification types."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    SYSTEM = "system"


class NotificationPriority(Enum):
    """Notification priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(kw_only=True)
class Notification(BaseEntity):
    """
    Notification domain entity.
    """
    user_id: str
    title: str
    message: str
    notification_type: NotificationType = NotificationType.INFO
    priority: NotificationPriority = NotificationPriority.MEDIUM
    is_read: bool = False
    action_url: Optional[str] = None
    metadata: Optional[dict] = None
    expires_at: Optional[datetime] = None
    
    def validate(self) -> bool:
        """Validate notification entity."""
        if not self.user_id:
            return False
        if not self.title or len(self.title) < 1:
            return False
        if not self.message or len(self.message) < 1:
            return False
        return True
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.mark_as_updated()
    
    def mark_as_unread(self):
        """Mark notification as unread."""
        self.is_read = False
        self.mark_as_updated()
    
    def is_expired(self) -> bool:
        """Check if notification is expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_high_priority(self) -> bool:
        """Check if notification is high priority."""
        return self.priority == NotificationPriority.HIGH
