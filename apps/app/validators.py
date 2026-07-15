"""
Validators.

Input validation functions for various data types and operations.
"""

import re
from typing import Optional, List, Dict, Any
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator

from .exceptions import ValidationException


class BaseValidator:
    """Base validator class."""
    
    @staticmethod
    def validate_required(value: Any, field_name: str = "field"):
        """
        Validate that a value is present and not empty.
        
        Args:
            value: Value to validate
            field_name: Name of the field being validated
            
        Raises:
            ValidationException: If validation fails
        """
        if value is None:
            raise ValidationException(
                f"{field_name} is required",
                field=field_name
            )
        
        if isinstance(value, str) and not value.strip():
            raise ValidationException(
                f"{field_name} cannot be empty",
                field=field_name
            )
        
        if isinstance(value, (list, dict)) and len(value) == 0:
            raise ValidationException(
                f"{field_name} cannot be empty",
                field=field_name
            )
    
    @staticmethod
    def validate_length(value: str, min_length: int = 0, max_length: int = None, field_name: str = "field"):
        """
        Validate string length.
        
        Args:
            value: String to validate
            min_length: Minimum length
            max_length: Maximum length
            field_name: Name of the field being validated
            
        Raises:
            ValidationException: If validation fails
        """
        if len(value) < min_length:
            raise ValidationException(
                f"{field_name} must be at least {min_length} characters",
                field=field_name
            )
        
        if max_length and len(value) > max_length:
            raise ValidationException(
                f"{field_name} must not exceed {max_length} characters",
                field=field_name
            )


class UserValidator(BaseValidator):
    """Validator for user-related data."""
    
    @staticmethod
    def validate_username(username: str):
        """
        Validate username format.
        
        Args:
            username: Username to validate
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(username, "username")
        BaseValidator.validate_length(username, min_length=3, max_length=30, field_name="username")
        
        # Username should be alphanumeric with underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationException(
                "Username can only contain letters, numbers, and underscores",
                field="username"
            )
    
    @staticmethod
    def validate_email(email: str):
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(email, "email")
        
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            raise ValidationException(
                "Invalid email format",
                field="email"
            )
    
    @staticmethod
    def validate_password(password: str):
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(password, "password")
        BaseValidator.validate_length(password, min_length=8, field_name="password")
    
    @staticmethod
    def validate_registration_data(username: str, email: str, password: str):
        """
        Validate complete registration data.
        
        Args:
            username: Username
            email: Email
            password: Password
            
        Raises:
            ValidationException: If any validation fails
        """
        UserValidator.validate_username(username)
        UserValidator.validate_email(email)
        UserValidator.validate_password(password)


class ChatValidator(BaseValidator):
    """Validator for chat-related data."""
    
    @staticmethod
    def validate_message(message: str, imagen=None):
        """
        Validate chat message.
        
        Args:
            message: Message text
            imagen: Image file
            
        Raises:
            ValidationException: If validation fails
        """
        # At least one of message or image must be present
        if not message and not imagen:
            raise ValidationException(
                "At least a message or image is required",
                field="message"
            )
        
        if message and len(message) > 10000:
            raise ValidationException(
                "Message is too long (max 10000 characters)",
                field="message"
            )
    
    @staticmethod
    def validate_conversation_id(conversation_id: str):
        """
        Validate conversation ID.
        
        Args:
            conversation_id: Conversation ID
            
        Raises:
            ValidationException: If validation fails
        """
        if conversation_id:
            try:
                int(conversation_id)
            except (ValueError, TypeError):
                raise ValidationException(
                    "Invalid conversation ID",
                    field="conversation_id"
                )


class MusicValidator(BaseValidator):
    """Validator for music-related data."""
    
    @staticmethod
    def validate_playlist_name(name: str):
        """
        Validate playlist name.
        
        Args:
            name: Playlist name
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(name, "name")
        BaseValidator.validate_length(name, min_length=1, max_length=100, field_name="name")
    
    @staticmethod
    def validate_playlist_description(description: str):
        """
        Validate playlist description.
        
        Args:
            description: Playlist description
            
        Raises:
            ValidationException: If validation fails
        """
        if description and len(description) > 500:
            raise ValidationException(
                "Description is too long (max 500 characters)",
                field="description"
            )
    
    @staticmethod
    def validate_song_data(title: str, url: str):
        """
        Validate song data.
        
        Args:
            title: Song title
            url: Song URL
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(title, "title")
        BaseValidator.validate_required(url, "url")
        
        BaseValidator.validate_length(title, max_length=200, field_name="title")
        
        # Validate URL
        url_validator = URLValidator()
        try:
            url_validator(url)
        except ValidationError:
            raise ValidationException(
                "Invalid song URL",
                field="url"
            )


class EventValidator(BaseValidator):
    """Validator for event-related data."""
    
    @staticmethod
    def validate_event_title(title: str):
        """
        Validate event title.
        
        Args:
            title: Event title
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(title, "title")
        BaseValidator.validate_length(title, min_length=1, max_length=200, field_name="title")
    
    @staticmethod
    def validate_event_dates(start_date, end_date):
        """
        Validate event dates.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Raises:
            ValidationException: If validation fails
        """
        if start_date and end_date and start_date > end_date:
            raise ValidationException(
                "End date must be after start date",
                field="end_date"
            )
    
    @staticmethod
    def validate_event_data(title: str, start_date=None, end_date=None):
        """
        Validate complete event data.
        
        Args:
            title: Event title
            start_date: Start date
            end_date: End date
            
        Raises:
            ValidationException: If any validation fails
        """
        EventValidator.validate_event_title(title)
        EventValidator.validate_event_dates(start_date, end_date)


class FileValidator(BaseValidator):
    """Validator for file uploads."""
    
    @staticmethod
    def validate_image_file(file):
        """
        Validate image file.
        
        Args:
            file: Uploaded file
            
        Raises:
            ValidationException: If validation fails
        """
        if not file:
            return
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file.size > max_size:
            raise ValidationException(
                "Image file is too large (max 10MB)",
                field="image"
            )
        
        # Check file extension
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        import os
        ext = os.path.splitext(file.name)[1].lower()
        
        if ext not in allowed_extensions:
            raise ValidationException(
                f"Invalid image format. Allowed: {', '.join(allowed_extensions)}",
                field="image"
            )
    
    @staticmethod
    def validate_audio_file(file):
        """
        Validate audio file.
        
        Args:
            file: Uploaded file
            
        Raises:
            ValidationException: If validation fails
        """
        if not file:
            return
        
        # Check file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB
        if file.size > max_size:
            raise ValidationException(
                "Audio file is too large (max 50MB)",
                field="audio"
            )
        
        # Check file extension
        allowed_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a'}
        import os
        ext = os.path.splitext(file.name)[1].lower()
        
        if ext not in allowed_extensions:
            raise ValidationException(
                f"Invalid audio format. Allowed: {', '.join(allowed_extensions)}",
                field="audio"
            )


class StudyValidator(BaseValidator):
    """Validator for study-related data."""
    
    @staticmethod
    def validate_resource_title(title: str):
        """
        Validate resource title.
        
        Args:
            title: Resource title
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(title, "title")
        BaseValidator.validate_length(title, min_length=1, max_length=200, field_name="title")
    
    @staticmethod
    def validate_resource_url(url: str):
        """
        Validate resource URL.
        
        Args:
            url: Resource URL
            
        Raises:
            ValidationException: If validation fails
        """
        if url:
            url_validator = URLValidator()
            try:
                url_validator(url)
            except ValidationError:
                raise ValidationException(
                    "Invalid resource URL",
                    field="url"
                )
    
    @staticmethod
    def validate_category_name(name: str):
        """
        Validate category name.
        
        Args:
            name: Category name
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(name, "name")
        BaseValidator.validate_length(name, min_length=1, max_length=100, field_name="name")


class NotificationValidator(BaseValidator):
    """Validator for notification-related data."""
    
    @staticmethod
    def validate_notification_title(title: str):
        """
        Validate notification title.
        
        Args:
            title: Notification title
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(title, "title")
        BaseValidator.validate_length(title, min_length=1, max_length=200, field_name="title")
    
    @staticmethod
    def validate_notification_message(message: str):
        """
        Validate notification message.
        
        Args:
            message: Notification message
            
        Raises:
            ValidationException: If validation fails
        """
        BaseValidator.validate_required(message, "message")
        BaseValidator.validate_length(message, min_length=1, max_length=1000, field_name="message")
    
    @staticmethod
    def validate_notification_type(notification_type: str):
        """
        Validate notification type.
        
        Args:
            notification_type: Notification type
            
        Raises:
            ValidationException: If validation fails
        """
        valid_types = {'info', 'success', 'warning', 'error', 'system'}
        if notification_type not in valid_types:
            raise ValidationException(
                f"Invalid notification type. Valid: {', '.join(valid_types)}",
                field="notification_type"
            )


class GameValidator(BaseValidator):
    """Validator for game-related data."""
    
    @staticmethod
    def validate_score(score: int):
        """
        Validate game score.
        
        Args:
            score: Score value
            
        Raises:
            ValidationException: If validation fails
        """
        if score is None:
            return
        
        if not isinstance(score, (int, float)):
            raise ValidationException(
                "Score must be a number",
                field="score"
            )
        
        if score < 0:
            raise ValidationException(
                "Score cannot be negative",
                field="score"
            )
    
    @staticmethod
    def validate_game_id(game_id: int):
        """
        Validate game ID.
        
        Args:
            game_id: Game ID
            
        Raises:
            ValidationException: If validation fails
        """
        if game_id is None:
            return
        
        try:
            int(game_id)
        except (ValueError, TypeError):
            raise ValidationException(
                "Invalid game ID",
                field="game_id"
            )


class RequestValidator:
    """Validator for HTTP request data."""
    
    @staticmethod
    def validate_json_request(request):
        """
        Validate that request contains valid JSON.
        
        Args:
            request: HTTP request object
            
        Returns:
            Parsed JSON data
            
        Raises:
            ValidationException: If validation fails
        """
        import json
        try:
            return json.loads(request.body)
        except (json.JSONDecodeError, AttributeError):
            raise ValidationException(
                "Invalid JSON data",
                field="request_body"
            )
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]):
        """
        Validate that required fields are present in data.
        
        Args:
            data: Dictionary of data
            required_fields: List of required field names
            
        Raises:
            ValidationException: If any required field is missing
        """
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            raise ValidationException(
                f"Missing required fields: {', '.join(missing_fields)}",
                details={'missing_fields': missing_fields}
            )
