"""
User Use Cases

Application use cases for user-related operations.
"""

from dataclasses import dataclass
from typing import Optional

from .base_use_case import UseCase, UseCaseRequest, UseCaseResponse
from application.dto.user_dto import CreateUserDTO, UpdateUserDTO
from infrastructure.repositories.user_repository import UserRepository
from core.entities.user import User, UserRole, Theme
from core.services.user_service import UserService


@dataclass
class CreateUserRequest(UseCaseRequest):
    """Request for creating a user."""
    email: str
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""


@dataclass
class UpdateUserRequest(UseCaseRequest):
    """Request for updating a user."""
    user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    theme: Optional[str] = None
    avatar_url: Optional[str] = None


@dataclass
class GetUserRequest(UseCaseRequest):
    """Request for getting a user."""
    user_id: str


@dataclass
class DeleteUserRequest(UseCaseRequest):
    """Request for deleting a user."""
    user_id: str


class CreateUserUseCase(UseCase[CreateUserRequest, UseCaseResponse]):
    """Use case for creating a new user."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, request: CreateUserRequest) -> UseCaseResponse:
        """Execute the create user use case."""
        # Validate email uniqueness
        if self.repository.exists_by_email(request.email):
            return self.create_error_response(
                "Email already exists",
                [{"email": "A user with this email already exists"}]
            )
        
        # Validate username
        if not UserService.is_valid_username(request.username):
            return self.create_error_response(
                "Invalid username",
                [{"username": "Username must be at least 3 characters and contain only alphanumeric characters"}]
            )
        
        # Create user entity
        user = User(
            email=request.email,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name
        )
        
        # Validate entity
        if not user.validate():
            return self.create_error_response("Invalid user data")
        
        # Save user
        saved_user = self.repository.save(user)
        
        return self.create_success_response(
            "User created successfully",
            {
                "id": saved_user.id,
                "email": saved_user.email,
                "username": saved_user.username
            }
        )


class UpdateUserProfileUseCase(UseCase[UpdateUserRequest, UseCaseResponse]):
    """Use case for updating user profile."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, request: UpdateUserRequest) -> UseCaseResponse:
        """Execute the update user use case."""
        # Find user
        user = self.repository.find_by_id(request.user_id)
        if not user:
            return self.create_error_response("User not found")
        
        # Update fields
        if request.first_name is not None:
            user.first_name = request.first_name
        if request.last_name is not None:
            user.last_name = request.last_name
        if request.bio is not None:
            user.bio = request.bio
        if request.phone is not None:
            user.phone = request.phone
        if request.theme is not None:
            try:
                user.theme = Theme(request.theme)
            except ValueError:
                return self.create_error_response("Invalid theme value")
        if request.avatar_url is not None:
            user.avatar_url = request.avatar_url
        
        # Validate and save
        if not user.validate():
            return self.create_error_response("Invalid user data")
        
        saved_user = self.repository.save(user)
        
        return self.create_success_response(
            "Profile updated successfully",
            {
                "id": saved_user.id,
                "email": saved_user.email,
                "username": saved_user.username,
                "first_name": saved_user.first_name,
                "last_name": saved_user.last_name
            }
        )


class GetUserUseCase(UseCase[GetUserRequest, UseCaseResponse]):
    """Use case for getting a user."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, request: GetUserRequest) -> UseCaseResponse:
        """Execute the get user use case."""
        user = self.repository.find_by_id(request.user_id)
        
        if not user:
            return self.create_error_response("User not found")
        
        return self.create_success_response(
            "User retrieved successfully",
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
                "theme": user.theme.value,
                "is_active": user.is_active,
                "avatar_url": user.avatar_url,
                "bio": user.bio,
                "phone": user.phone
            }
        )


class DeleteUserUseCase(UseCase[DeleteUserRequest, UseCaseResponse]):
    """Use case for deleting a user."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, request: DeleteUserRequest) -> UseCaseResponse:
        """Execute the delete user use case."""
        if not self.repository.exists(request.user_id):
            return self.create_error_response("User not found")
        
        success = self.repository.delete(request.user_id)
        
        if success:
            return self.create_success_response("User deleted successfully")
        return self.create_error_response("Failed to delete user")
