"""
User DTOs

Data transfer objects for user-related operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    """User data transfer object."""
    id: str
    email: str
    username: str
    first_name: str = ""
    last_name: str = ""
    role: str = "user"
    theme: str = "auto"
    is_active: bool = True
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


@dataclass
class CreateUserDTO:
    """DTO for creating a user."""
    email: str
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""


@dataclass
class UpdateUserDTO:
    """DTO for updating a user."""
    user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    theme: Optional[str] = None
    avatar_url: Optional[str] = None
