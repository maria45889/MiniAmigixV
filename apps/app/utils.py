"""
Utility functions.

Helper functions used across the application.
"""

import json
import logging
from typing import Any, Dict, Optional
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class JsonResponseHelper:
    """Helper for creating JSON responses."""
    
    @staticmethod
    def success_response(data: Any = None, message: str = "Success", status: int = 200) -> JsonResponse:
        """Create a success JSON response."""
        return JsonResponse({
            'success': True,
            'message': message,
            'data': data
        }, status=status)
    
    @staticmethod
    def error_response(message: str, errors: list = None, status: int = 400) -> JsonResponse:
        """Create an error JSON response."""
        return JsonResponse({
            'success': False,
            'message': message,
            'errors': errors or []
        }, status=status)
    
    @staticmethod
    def not_found_response(message: str = "Resource not found") -> JsonResponse:
        """Create a not found JSON response."""
        return JsonResponseHelper.error_response(message, status=404)
    
    @staticmethod
    def unauthorized_response(message: str = "Unauthorized") -> JsonResponse:
        """Create an unauthorized JSON response."""
        return JsonResponseHelper.error_response(message, status=401)
    
    @staticmethod
    def forbidden_response(message: str = "Forbidden") -> JsonResponse:
        """Create a forbidden JSON response."""
        return JsonResponseHelper.error_response(message, status=403)


class RequestParser:
    """Helper for parsing request data."""
    
    @staticmethod
    def parse_json_body(request) -> Optional[Dict]:
        """
        Parse JSON body from request.
        
        Args:
            request: HTTP request object
            
        Returns:
            Parsed JSON data or None if error
        """
        try:
            return json.loads(request.body)
        except (json.JSONDecodeError, AttributeError):
            return None
    
    @staticmethod
    def parse_form_data(request) -> Dict:
        """
        Parse form data from request.
        
        Args:
            request: HTTP request object
            
        Returns:
            Dictionary with form data
        """
        return {
            'message': request.POST.get('message', ''),
            'conversation_id': request.POST.get('conversation_id'),
            'imagen': request.FILES.get('imagen')
        }


class ContentHelper:
    """Helper for content processing."""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """
        Truncate text to maximum length.
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + suffix
    
    @staticmethod
    def format_notification_message(response: str, max_length: int = 100) -> str:
        """
        Format notification message from AI response.
        
        Args:
            response: AI response text
            max_length: Maximum length
            
        Returns:
            Formatted notification message
        """
        return f'MiniAmigix ha respondido: "{ContentHelper.truncate_text(response, max_length)}..."'
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe storage.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        import re
        # Remove special characters except dots, underscores, hyphens
        sanitized = re.sub(r'[^\w\-_.]', '_', filename)
        return sanitized


class AdminHelper:
    """Helper for admin-related operations."""
    
    @staticmethod
    def is_admin_user(user, allowed_admins: list = None) -> bool:
        """
        Check if user is admin based on email.
        
        Args:
            user: User object
            allowed_admins: List of allowed admin emails
            
        Returns:
            True if user is admin
        """
        from django.conf import settings
        
        if allowed_admins is None:
            allowed_admins = getattr(settings, 'ADMIN_EMAILS', ['miniamigixv@gmail.com'])
        
        if isinstance(allowed_admins, str):
            allowed_admins = [allowed_admins]
        
        allowed_admins = [email.strip().lower() for email in allowed_admins if email]
        user_email = (getattr(user, 'email', '') or '').strip().lower()
        
        return bool(user and user.is_authenticated and user_email in allowed_admins)


class LogHelper:
    """Helper for logging operations."""
    
    @staticmethod
    def log_error(logger_obj, message: str, exc_info: bool = False):
        """Log error message."""
        logger_obj.error(message, exc_info=exc_info)
    
    @staticmethod
    def log_warning(logger_obj, message: str):
        """Log warning message."""
        logger_obj.warning(message)
    
    @staticmethod
    def log_info(logger_obj, message: str):
        """Log info message."""
        logger_obj.info(message)
    
    @staticmethod
    def log_success(logger_obj, message: str):
        """Log success message."""
        logger_obj.info(f"✓ {message}")


class ValidationHelper:
    """Helper for validation operations."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email string
            
        Returns:
            True if valid
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_username(username: str) -> bool:
        """
        Validate username format.
        
        Args:
            username: Username string
            
        Returns:
            True if valid
        """
        if not username or len(username) < 3:
            return False
        if len(username) > 30:
            return False
        return username.isalnum() or '_' in username
    
    @staticmethod
    def is_required_field(value: Any) -> bool:
        """
        Check if field has a value.
        
        Args:
            value: Field value
            
        Returns:
            True if field has value
        """
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, (list, dict)) and len(value) == 0:
            return False
        return True


class DateTimeHelper:
    """Helper for date/time operations."""
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """
        Format duration in seconds to human-readable string.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    @staticmethod
    def get_time_ago(datetime_obj) -> str:
        """
        Get human-readable time ago string.
        
        Args:
            datetime_obj: DateTime object
            
        Returns:
            Time ago string
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not datetime_obj:
            return "Never"
        
        now = timezone.now()
        diff = now - datetime_obj
        
        if diff < timedelta(minutes=1):
            return "Just now"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff < timedelta(weeks=1):
            days = diff.days
            return f"{days} day{'s' if days > 1 else ''} ago"
        else:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"


class FileHelper:
    """Helper for file operations."""
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Get file extension from filename.
        
        Args:
            filename: Filename
            
        Returns:
            File extension (without dot)
        """
        if '.' not in filename:
            return ''
        return filename.rsplit('.', 1)[1].lower()
    
    @staticmethod
    def is_image_file(filename: str) -> bool:
        """
        Check if file is an image.
        
        Args:
            filename: Filename
            
        Returns:
            True if image file
        """
        image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'}
        return FileHelper.get_file_extension(filename) in image_extensions
    
    @staticmethod
    def is_audio_file(filename: str) -> bool:
        """
        Check if file is an audio file.
        
        Args:
            filename: Filename
            
        Returns:
            True if audio file
        """
        audio_extensions = {'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'}
        return FileHelper.get_file_extension(filename) in audio_extensions


class PaginationHelper:
    """Helper for pagination operations."""
    
    @staticmethod
    def get_pagination_data(page: int, per_page: int, total_items: int) -> Dict:
        """
        Get pagination metadata.
        
        Args:
            page: Current page number
            per_page: Items per page
            total_items: Total number of items
            
        Returns:
            Dictionary with pagination data
        """
        total_pages = (total_items + per_page - 1) // per_page
        has_next = page < total_pages
        has_prev = page > 1
        
        return {
            'page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': total_pages,
            'has_next': has_next,
            'has_prev': has_prev,
            'next_page': page + 1 if has_next else None,
            'prev_page': page - 1 if has_prev else None
        }
    
    @staticmethod
    def get_slice(page: int, per_page: int) -> slice:
        """
        Get slice for pagination.
        
        Args:
            page: Current page number
            per_page: Items per page
            
        Returns:
            Slice object
        """
        start = (page - 1) * per_page
        end = start + per_page
        return slice(start, end)
