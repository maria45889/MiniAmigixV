"""
Auth service.

Business logic for authentication operations.
"""

import logging
from typing import Optional

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from ..selectors.auth_selector import AuthSelector
from ..validators import UserValidator
from ..exceptions import ValidationException, AuthenticationException
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def register_user(username: str, email: str, password: str, password_confirm: str) -> tuple[User, Optional[str]]:
        """
        Register a new user.
        
        Args:
            username: Username
            email: Email address
            password: Password
            password_confirm: Password confirmation
            
        Returns:
            Tuple of (user, error_message)
        """
        # Validate passwords match
        if password != password_confirm:
            return None, "Las contraseñas no coinciden"
        
        # Validate registration data
        try:
            UserValidator.validate_registration_data(username, email, password)
        except ValidationException as e:
            return None, e.message
        
        # Check if username exists
        if AuthSelector.username_exists(username):
            return None, "El usuario ya existe"
        
        # Check if email exists
        if AuthSelector.email_exists(email):
            return None, "El email ya está registrado"
        
        # Create user
        try:
            user = AuthSelector.create_user(username, email, password)
            LogHelper.log_info(logger, f"Usuario registrado exitosamente: {username}")
            return user, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al crear usuario: {str(e)}", exc_info=True)
            return None, "Error al crear usuario"
    
    @staticmethod
    def login_user(request, username: str, password: str) -> tuple[bool, Optional[str]]:
        """
        Login a user.
        
        Args:
            request: HTTP request
            username: Username
            password: Password
            
        Returns:
            Tuple of (success, error_message)
        """
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return False, "Credenciales inválidas"
        
        if not user.is_active:
            return False, "Usuario desactivado"
        
        login(request, user)
        LogHelper.log_info(logger, f"Usuario logueado exitosamente: {username}")
        return True, None
    
    @staticmethod
    def logout_user(request):
        """Logout a user."""
        from django.contrib.auth import logout
        logout(request)
        LogHelper.log_info(logger, "Usuario deslogueado")
