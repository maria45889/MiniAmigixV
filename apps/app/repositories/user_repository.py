"""
User repository.

Data access layer for user operations.
"""

from django.contrib.auth.models import User


class UserRepository:
    """Repository for user data access."""
    
    @staticmethod
    def save_user(user):
        """Save user to database."""
        user.save()
        return user
    
    @staticmethod
    def delete_user(user_id: int):
        """Delete user."""
        user = User.objects.get(id=user_id)
        user.delete()
