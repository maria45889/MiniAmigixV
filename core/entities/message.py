"""
Message Entity

Represents a message in a conversation.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from .base_entity import BaseEntity


class MessageRole(Enum):
    """Message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass(kw_only=True)
class Message(BaseEntity):
    """
    Message domain entity.
    """
    conversation_id: str
    role: MessageRole
    content: str
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    
    def validate(self) -> bool:
        """Validate message entity."""
        if not self.conversation_id:
            return False
        if not isinstance(self.role, MessageRole):
            return False
        if not self.content or len(self.content) < 1:
            return False
        return True
    
    def is_from_user(self) -> bool:
        """Check if message is from user."""
        return self.role == MessageRole.USER
    
    def is_from_assistant(self) -> bool:
        """Check if message is from assistant."""
        return self.role == MessageRole.ASSISTANT
    
    def is_system(self) -> bool:
        """Check if message is system message."""
        return self.role == MessageRole.SYSTEM
