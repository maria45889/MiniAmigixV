"""
User selector.

Database queries for user operations.
"""

from django.contrib.auth.models import User


class UserSelector:
    """Selector for user-related queries."""
    
    @staticmethod
    def get_by_id(user_id: int):
        """Get user by ID."""
        return User.objects.filter(id=user_id).first()
    
    @staticmethod
    def get_by_email(email: str):
        """Get user by email."""
        return User.objects.filter(email=email).first()
    
    @staticmethod
    def update_user(user, **kwargs):
        """Update user fields."""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.save()
    
    @staticmethod
    def deactivate_user(user):
        """Deactivate user."""
        user.is_active = False
        user.save()
    
    @staticmethod
    def activate_user(user):
        """Activate user."""
        user.is_active = True
        user.save()
