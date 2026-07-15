"""
Notification DTOs

Data transfer objects for notification-related operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NotificationDTO:
    """Notification data transfer object."""
    id: str
    user_id: str
    title: str
    message: str
    notification_type: str = "info"
    priority: str = "medium"
    is_read: bool = False
    action_url: Optional[str] = None
    metadata: Optional[dict] = None
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
