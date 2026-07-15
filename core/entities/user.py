"""
User Entity

Represents a user in the system.
Contains business logic related to users.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List

from .base_entity import BaseEntity


class UserRole(Enum):
    """User roles in the system."""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class Theme(Enum):
    """Theme preferences."""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


@dataclass
class User(BaseEntity):
    """
    User domain entity.
    
    Contains user-related business logic and validation.
    """
    email: str
    username: str
    first_name: str = ""
    last_name: str = ""
    role: UserRole = UserRole.USER
    theme: Theme = Theme.AUTO
    is_active: bool = True
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    last_login: Optional[datetime] = None
    
    def validate(self) -> bool:
        """Validate user entity."""
        if not self.email or '@' not in self.email:
            return False
        if not self.username or len(self.username) < 3:
            return False
        return True
    
    def get_full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == UserRole.ADMIN
    
    def is_moderator(self) -> bool:
        """Check if user is moderator or admin."""
        return self.role in [UserRole.ADMIN, UserRole.MODERATOR]
    
    def promote_to_admin(self):
        """Promote user to admin role."""
        self.role = UserRole.ADMIN
        self.mark_as_updated()
    
    def deactivate(self):
        """Deactivate user account."""
        self.is_active = False
        self.mark_as_updated()
    
    def activate(self):
        """Activate user account."""
        self.is_active = True
        self.mark_as_updated()
