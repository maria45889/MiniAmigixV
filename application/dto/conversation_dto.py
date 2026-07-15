"""
Conversation DTOs

Data transfer objects for conversation-related operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class MessageDTO:
    """Message data transfer object."""
    id: str
    conversation_id: str
    role: str
    content: str
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class ConversationDTO:
    """Conversation data transfer object."""
    id: str
    user_id: str
    title: str
    messages: List[MessageDTO] = None
    is_archived: bool = False
    model_used: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []


@dataclass
class CreateConversationDTO:
    """DTO for creating a conversation."""
    user_id: str
    title: str
    model_used: Optional[str] = None


@dataclass
class AddMessageDTO:
    """DTO for adding a message to a conversation."""
    conversation_id: str
    role: str
    content: str
    model_used: Optional[str] = None
