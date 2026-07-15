"""
User API Views

API endpoints for user-related operations.
"""

from typing import Dict
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .base_view import BaseAPIView
from application.use_cases.user_use_cases import (
    CreateUserUseCase,
    UpdateUserProfileUseCase,
    GetUserUseCase,
    DeleteUserUseCase
)
from application.dto.user_dto import CreateUserDTO, UpdateUserDTO
from infrastructure.repositories.user_repository import UserRepository


class UserViewSet(BaseAPIView):
    """
    API viewset for user operations.
    """
    
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()
        self.create_user_use_case = CreateUserUseCase(self.user_repository)
        self.get_user_use_case = GetUserUseCase(self.user_repository)
        self.update_user_use_case = UpdateUserProfileUseCase(self.user_repository)
        self.delete_user_use_case = DeleteUserUseCase(self.user_repository)
    
    def get(self, request, user_id: str = None) -> JsonResponse:
        """
        Get user(s).
        
        Args:
            request: HTTP request
            user_id: Optional user ID
            
        Returns:
            JsonResponse
        """
        if user_id:
            # Get single user
            response = self.get_user_use_case.execute(
                type('Request', (), {'user_id': user_id})()
            )
            if response.success:
                return self.success_response(response.data, response.message)
            return self.not_found_response(response.message)
        else:
            # Get current user from request
            if request.user.is_authenticated:
                response = self.get_user_use_case.execute(
                    type('Request', (), {'user_id': str(request.user.id)})()
                )
                if response.success:
                    return self.success_response(response.data, response.message)
            return self.unauthorized_response()
    
    def post(self, request) -> JsonResponse:
        """
        Create a new user.
        
        Args:
            request: HTTP request
            
        Returns:
            JsonResponse
        """
        import json
        data = json.loads(request.body)
        
        dto = CreateUserDTO(
            email=data.get('email'),
            username=data.get('username'),
            password=data.get('password'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        
        response = self.create_user_use_case.execute(dto)
        
        if response.success:
            return self.success_response(response.data, response.message, status=201)
        return self.error_response(response.message, response.errors, status=400)
    
    def put(self, request, user_id: str) -> JsonResponse:
        """
        Update a user.
        
        Args:
            request: HTTP request
            user_id: User ID to update
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated:
            return self.unauthorized_response()
        
        import json
        data = json.loads(request.body)
        
        dto = UpdateUserDTO(
            user_id=user_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            bio=data.get('bio'),
            phone=data.get('phone'),
            theme=data.get('theme'),
            avatar_url=data.get('avatar_url')
        )
        
        response = self.update_user_use_case.execute(dto)
        
        if response.success:
            return self.success_response(response.data, response.message)
        return self.error_response(response.message, response.errors)
    
    def delete(self, request, user_id: str) -> JsonResponse:
        """
        Delete a user.
        
        Args:
            request: HTTP request
            user_id: User ID to delete
            
        Returns:
            JsonResponse
        """
        if not request.user.is_authenticated or not request.user.is_staff:
            return self.forbidden_response()
        
        response = self.delete_user_use_case.execute(
            type('Request', (), {'user_id': user_id})()
        )
        
        if response.success:
            return self.success_response(None, response.message)
        return self.error_response(response.message)


class UserDetailView(UserViewSet):
    """
    API view for single user operations.
    """
    
    def get(self, request, user_id: str) -> JsonResponse:
        """Get a single user by ID."""
        return super().get(request, user_id)
    
    def put(self, request, user_id: str) -> JsonResponse:
        """Update a single user."""
        return super().put(request, user_id)
    
    def delete(self, request, user_id: str) -> JsonResponse:
        """Delete a single user."""
        return super().delete(request, user_id)
