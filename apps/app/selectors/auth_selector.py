"""
Auth selector.

Database queries for authentication operations.
"""

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class AuthSelector:
    """Selector for authentication-related queries."""
    
    @staticmethod
    def username_exists(username: str) -> bool:
        """Check if a username exists."""
        return User.objects.filter(username=username).exists()
    
    @staticmethod
    def email_exists(email: str) -> bool:
        """Check if an email exists."""
        return User.objects.filter(email=email).exists()
    
    @staticmethod
    def get_by_username(username: str):
        """Get user by username."""
        return User.objects.filter(username=username).first()
    
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        """Create a new user."""
        return User.objects.create_user(username=username, email=email, password=password)
    
    @staticmethod
    def get_current_site():
        """Get the current site."""
        try:
            return Site.objects.get_current()
        except Exception:
            return None
    
    @staticmethod
    def get_google_social_apps(site):
        """Get all social OAuth apps for the current site."""
        if not site:
            return SocialApp.objects.none()
        try:
            return SocialApp.objects.filter(sites=site)
        except Exception:
            return SocialApp.objects.none()
