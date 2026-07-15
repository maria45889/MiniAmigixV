"""
Conversation Entity

Represents a conversation in the AI chat system.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from .base_entity import BaseEntity
from .message import Message


@dataclass
class Conversation(BaseEntity):
    """
    Conversation domain entity for AI chat.
    """
    user_id: str
    title: str
    messages: List[Message] = field(default_factory=list)
    is_archived: bool = False
    model_used: Optional[str] = None
    
    def validate(self) -> bool:
        """Validate conversation entity."""
        if not self.user_id:
            return False
        if not self.title or len(self.title) < 1:
            return False
        return True
    
    def add_message(self, message: Message):
        """Add a message to the conversation."""
        self.messages.append(message)
        self.mark_as_updated()
    
    def get_last_message(self) -> Optional[Message]:
        """Get the last message in the conversation."""
        return self.messages[-1] if self.messages else None
    
    def get_message_count(self) -> int:
        """Get total number of messages."""
        return len(self.messages)
    
    def archive(self):
        """Archive the conversation."""
        self.is_archived = True
        self.mark_as_updated()
    
    def unarchive(self):
        """Unarchive the conversation."""
        self.is_archived = False
        self.mark_as_updated()
