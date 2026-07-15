"""
Conversation API Views

API endpoints for conversation and message operations.
"""

from django.http import JsonResponse

from .base_view import BaseAPIView
from application.use_cases.conversation_use_cases import (
    CreateConversationUseCase,
    AddMessageUseCase,
    GetConversationUseCase,
    ListConversationsUseCase
)
from application.dto.conversation_dto import CreateConversationDTO, AddMessageDTO
from infrastructure.repositories.conversation_repository import ConversationRepository


class ConversationViewSet(BaseAPIView):
    """
    API viewset for conversation operations.
    """
    
    def __init__(self):
        super().__init__()
        self.conversation_repository = ConversationRepository()
        self.create_conversation_use_case = CreateConversationUseCase(self.conversation_repository)
        self.get_conversation_use_case = GetConversationUseCase(self.conversation_repository)
        self.list_conversations_use_case = ListConversationsUseCase(self.conversation_repository)
        self.add_message_use_case = AddMessageUseCase(self.conversation_repository)
    
    def get(self, request, conversation_id: str = None) -> JsonResponse:
        """
        Get conversation(s).
        
        Args:
            request: HTTP request
            conversation_id: Optional conversation ID
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        user_id = str(request.user.id)
        
        if conversation_id:
            # Get single conversation
            response = self.get_conversation_use_case.execute(
                type('Request', (), {'conversation_id': conversation_id, 'user_id': user_id})()
            )
            if response.success:
                return self.success_response(response.data, response.message)
            return self.not_found_response(response.message)
        else:
            # List all conversations for user
            response = self.list_conversations_use_case.execute(
                type('Request', (), {'user_id': user_id})()
            )
            return self.success_response(response.data, response.message)
    
    def post(self, request) -> JsonResponse:
        """
        Create a new conversation.
        
        Args:
            request: HTTP request
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        import json
        data = json.loads(request.body)
        
        dto = CreateConversationDTO(
            user_id=str(request.user.id),
            title=data.get('title', 'New Conversation'),
            model_used=data.get('model_used')
        )
        
        response = self.create_conversation_use_case.execute(dto)
        
        if response.success:
            return self.success_response(response.data, response.message, status=201)
        return self.error_response(response.message, response.errors)


class MessageViewSet(BaseAPIView):
    """
    API viewset for message operations.
    """
    
    def __init__(self):
        super().__init__()
        self.conversation_repository = ConversationRepository()
        self.add_message_use_case = AddMessageUseCase(self.conversation_repository)
    
    def post(self, request, conversation_id: str) -> JsonResponse:
        """
        Add a message to a conversation.
        
        Args:
            request: HTTP request
            conversation_id: Conversation ID
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        import json
        data = json.loads(request.body)
        
        dto = AddMessageDTO(
            conversation_id=conversation_id,
            role=data.get('role', 'user'),
            content=data.get('content'),
            model_used=data.get('model_used')
        )
        
        response = self.add_message_use_case.execute(dto)
        
        if response.success:
            return self.success_response(response.data, response.message, status=201)
        return self.error_response(response.message, response.errors)
