"""
Base API View

Base class for all API views with common functionality.
"""

from abc import ABC
from typing import Any, Dict
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class BaseAPIView(View, ABC):
    """
    Base API view with common response methods.
    """
    
    def success_response(self, data: Any = None, message: str = "Success", status: int = 200) -> JsonResponse:
        """
        Create a success response.
        
        Args:
            data: Response data
            message: Success message
            status: HTTP status code
            
        Returns:
            JsonResponse
        """
        return JsonResponse({
            'success': True,
            'message': message,
            'data': data
        }, status=status)
    
    def error_response(self, message: str, errors: list = None, status: int = 400) -> JsonResponse:
        """
        Create an error response.
        
        Args:
            message: Error message
            errors: List of specific errors
            status: HTTP status code
            
        Returns:
            JsonResponse
        """
        return JsonResponse({
            'success': False,
            'message': message,
            'errors': errors or []
        }, status=status)
    
    def not_found_response(self, message: str = "Resource not found") -> JsonResponse:
        """
        Create a not found response.
        
        Args:
            message: Error message
            
        Returns:
            JsonResponse
        """
        return self.error_response(message, status=404)
    
    def unauthorized_response(self, message: str = "Unauthorized") -> JsonResponse:
        """
        Create an unauthorized response.
        
        Args:
            message: Error message
            
        Returns:
            JsonResponse
        """
        return self.error_response(message, status=401)
    
    def forbidden_response(self, message: str = "Forbidden") -> JsonResponse:
        """
        Create a forbidden response.
        
        Args:
            message: Error message
            
        Returns:
            JsonResponse
        """
        return self.error_response(message, status=403)
    
    def server_error_response(self, message: str = "Internal server error") -> JsonResponse:
        """
        Create a server error response.
        
        Args:
            message: Error message
            
        Returns:
            JsonResponse
        """
        return self.error_response(message, status=500)
