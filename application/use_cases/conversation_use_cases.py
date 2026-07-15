"""
Conversation Use Cases

Application use cases for conversation-related operations.
"""

from dataclasses import dataclass
from typing import List, Optional

from .base_use_case import UseCase, UseCaseRequest, UseCaseResponse
from application.dto.conversation_dto import CreateConversationDTO, AddMessageDTO
from infrastructure.repositories.conversation_repository import ConversationRepository
from core.entities.conversation import Conversation
from core.entities.message import Message, MessageRole


@dataclass
class CreateConversationRequest(UseCaseRequest):
    """Request for creating a conversation."""
    user_id: str
    title: str
    model_used: Optional[str] = None


@dataclass
class AddMessageRequest(UseCaseRequest):
    """Request for adding a message."""
    conversation_id: str
    role: str
    content: str
    model_used: Optional[str] = None


@dataclass
class GetConversationRequest(UseCaseRequest):
    """Request for getting a conversation."""
    conversation_id: str
    user_id: str


@dataclass
class ListConversationsRequest(UseCaseRequest):
    """Request for listing conversations."""
    user_id: str
    archived_only: bool = False


class CreateConversationUseCase(UseCase[CreateConversationRequest, UseCaseResponse]):
    """Use case for creating a conversation."""
    
    def __init__(self, repository: ConversationRepository):
        self.repository = repository
    
    def execute(self, request: CreateConversationRequest) -> UseCaseResponse:
        """Execute the create conversation use case."""
        conversation = Conversation(
            user_id=request.user_id,
            title=request.title,
            model_used=request.model_used
        )
        
        if not conversation.validate():
            return self.create_error_response("Invalid conversation data")
        
        saved_conversation = self.repository.save(conversation)
        
        return self.create_success_response(
            "Conversation created successfully",
            {
                "id": saved_conversation.id,
                "user_id": saved_conversation.user_id,
                "title": saved_conversation.title,
                "model_used": saved_conversation.model_used
            }
        )


class AddMessageUseCase(UseCase[AddMessageRequest, UseCaseResponse]):
    """Use case for adding a message to a conversation."""
    
    def __init__(self, repository: ConversationRepository):
        self.repository = repository
    
    def execute(self, request: AddMessageRequest) -> UseCaseResponse:
        """Execute the add message use case."""
        conversation = self.repository.find_by_id(request.conversation_id)
        
        if not conversation:
            return self.create_error_response("Conversation not found")
        
        try:
            role = MessageRole(request.role)
        except ValueError:
            return self.create_error_response("Invalid message role")
        
        message = Message(
            conversation_id=request.conversation_id,
            role=role,
            content=request.content,
            model_used=request.model_used
        )
        
        if not message.validate():
            return self.create_error_response("Invalid message data")
        
        conversation.add_message(message)
        self.repository.save(conversation)
        
        return self.create_success_response(
            "Message added successfully",
            {
                "id": message.id,
                "conversation_id": message.conversation_id,
                "role": message.role.value,
                "content": message.content
            }
        )


class GetConversationUseCase(UseCase[GetConversationRequest, UseCaseResponse]):
    """Use case for getting a conversation."""
    
    def __init__(self, repository: ConversationRepository):
        self.repository = repository
    
    def execute(self, request: GetConversationRequest) -> UseCaseResponse:
        """Execute the get conversation use case."""
        conversation = self.repository.find_by_id(request.conversation_id)
        
        if not conversation:
            return self.create_error_response("Conversation not found")
        
        if conversation.user_id != request.user_id:
            return self.create_error_response("Access denied")
        
        messages_data = [
            {
                "id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None
            }
            for msg in conversation.messages
        ]
        
        return self.create_success_response(
            "Conversation retrieved successfully",
            {
                "id": conversation.id,
                "user_id": conversation.user_id,
                "title": conversation.title,
                "is_archived": conversation.is_archived,
                "model_used": conversation.model_used,
                "messages": messages_data
            }
        )


class ListConversationsUseCase(UseCase[ListConversationsRequest, UseCaseResponse]):
    """Use case for listing conversations."""
    
    def __init__(self, repository: ConversationRepository):
        self.repository = repository
    
    def execute(self, request: ListConversationsRequest) -> UseCaseResponse:
        """Execute the list conversations use case."""
        if request.archived_only:
            conversations = self.repository.find_archived(request.user_id)
        else:
            conversations = self.repository.find_active(request.user_id)
        
        conversations_data = [
            {
                "id": conv.id,
                "title": conv.title,
                "is_archived": conv.is_archived,
                "message_count": conv.get_message_count(),
                "created_at": conv.created_at.isoformat() if conv.created_at else None,
                "updated_at": conv.updated_at.isoformat() if conv.updated_at else None
            }
            for conv in conversations
        ]
        
        return self.create_success_response(
            "Conversations retrieved successfully",
            {"conversations": conversations_data}
        )
