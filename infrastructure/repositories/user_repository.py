"""
User Repository

Concrete implementation for user data access using Django models.
"""

from typing import List, Optional
from django.contrib.auth import get_user_model

from .base_repository import BaseRepository
from core.entities.user import User, UserRole, Theme

UserModel = get_user_model()


class UserRepository(BaseRepository[User]):
    """
    Repository for User entities using Django ORM.
    """
    
    def save(self, entity: User) -> User:
        """Save a user entity."""
        django_user = self._to_django_model(entity)
        django_user.save()
        return self._to_entity(django_user)
    
    def find_by_id(self, entity_id: str) -> Optional[User]:
        """Find a user by ID."""
        try:
            django_user = UserModel.objects.get(id=entity_id)
            return self._to_entity(django_user)
        except UserModel.DoesNotExist:
            return None
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        try:
            django_user = UserModel.objects.get(email=email)
            return self._to_entity(django_user)
        except UserModel.DoesNotExist:
            return None
    
    def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username."""
        try:
            django_user = UserModel.objects.get(username=username)
            return self._to_entity(django_user)
        except UserModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[User]:
        """Find all users."""
        return [self._to_entity(u) for u in UserModel.objects.all()]
    
    def delete(self, entity_id: str) -> bool:
        """Delete a user by ID."""
        try:
            django_user = UserModel.objects.get(id=entity_id)
            django_user.delete()
            return True
        except UserModel.DoesNotExist:
            return False
    
    def exists(self, entity_id: str) -> bool:
        """Check if a user exists."""
        return UserModel.objects.filter(id=entity_id).exists()
    
    def exists_by_email(self, email: str) -> bool:
        """Check if a user with this email exists."""
        return UserModel.objects.filter(email=email).exists()
    
    def _to_django_model(self, entity: User) -> UserModel:
        """Convert domain entity to Django model."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=entity.role.value,
            theme=entity.theme.value,
            is_active=entity.is_active,
            avatar_url=entity.avatar_url,
            bio=entity.bio,
            phone=entity.phone,
            last_login=entity.last_login
        )
    
    def _to_entity(self, model: UserModel) -> User:
        """Convert Django model to domain entity."""
        return User(
            id=str(model.id),
            email=model.email,
            username=model.username,
            first_name=model.first_name or "",
            last_name=model.last_name or "",
            role=UserRole(model.role) if model.role else UserRole.USER,
            theme=Theme(model.theme) if model.theme else Theme.AUTO,
            is_active=model.is_active,
            avatar_url=model.avatar_url,
            bio=model.bio,
            phone=model.phone,
            last_login=model.last_login,
            created_at=model.date_joined if hasattr(model, 'date_joined') else None
        )
