"""
User Domain Service

Business logic related to users that doesn't belong in the entity.
"""

from typing import List, Optional
from ..entities.user import User, UserRole


class UserService:
    """
    Domain service for user-related business logic.
    """
    
    @staticmethod
    def can_promote_to_admin(current_user: User, target_user: User) -> bool:
        """
        Check if current user can promote target user to admin.
        
        Args:
            current_user: User attempting the promotion
            target_user: User to be promoted
            
        Returns:
            bool: True if promotion is allowed
        """
        return current_user.is_admin() and target_user.role != UserRole.ADMIN
    
    @staticmethod
    def generate_username_from_email(email: str) -> str:
        """
        Generate a username from email address.
        
        Args:
            email: User's email address
            
        Returns:
            str: Generated username
        """
        local_part = email.split('@')[0]
        # Remove special characters and numbers
        username = ''.join(c for c in local_part if c.isalnum())
        return username.lower()
    
    @staticmethod
    def is_valid_username(username: str) -> bool:
        """
        Validate username format.
        
        Args:
            username: Username to validate
            
        Returns:
            bool: True if valid
        """
        if not username or len(username) < 3:
            return False
        if len(username) > 30:
            return False
        return username.isalnum() or '_' in username
