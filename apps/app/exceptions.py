"""
Custom exceptions.

Application-specific exceptions for better error handling.
"""


class AppException(Exception):
    """Base exception for application errors."""
    
    def __init__(self, message: str, code: str = None, details: dict = None):
        """
        Initialize application exception.
        
        Args:
            message: Error message
            code: Error code for programmatic handling
            details: Additional error details
        """
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    """Exception for validation errors."""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        """
        Initialize validation exception.
        
        Args:
            message: Error message
            field: Field that failed validation
            details: Additional error details
        """
        if field:
            details = details or {}
            details['field'] = field
        super().__init__(message, code='VALIDATION_ERROR', details=details)


class AuthenticationException(AppException):
    """Exception for authentication errors."""
    
    def __init__(self, message: str = "Authentication failed", details: dict = None):
        """
        Initialize authentication exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code='AUTH_ERROR', details=details)


class AuthorizationException(AppException):
    """Exception for authorization errors."""
    
    def __init__(self, message: str = "Access denied", details: dict = None):
        """
        Initialize authorization exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code='AUTHORIZATION_ERROR', details=details)


class NotFoundException(AppException):
    """Exception for resource not found errors."""
    
    def __init__(self, resource_type: str = "Resource", resource_id: str = None, details: dict = None):
        """
        Initialize not found exception.
        
        Args:
            resource_type: Type of resource not found
            resource_id: ID of resource not found
            details: Additional error details
        """
        message = f"{resource_type} not found"
        if resource_id:
            message = f"{resource_type} with ID '{resource_id}' not found"
        
        if resource_id:
            details = details or {}
            details['resource_type'] = resource_type
            details['resource_id'] = resource_id
        
        super().__init__(message, code='NOT_FOUND', details=details)


class ConflictException(AppException):
    """Exception for conflict errors (e.g., duplicate resources)."""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        """
        Initialize conflict exception.
        
        Args:
            message: Error message
            field: Field that caused conflict
            details: Additional error details
        """
        if field:
            details = details or {}
            details['field'] = field
        super().__init__(message, code='CONFLICT_ERROR', details=details)


class ExternalServiceException(AppException):
    """Exception for external service errors."""
    
    def __init__(self, service_name: str, message: str = "External service error", details: dict = None):
        """
        Initialize external service exception.
        
        Args:
            service_name: Name of the external service
            message: Error message
            details: Additional error details
        """
        details = details or {}
        details['service'] = service_name
        super().__init__(message, code='EXTERNAL_SERVICE_ERROR', details=details)


class AIServiceException(ExternalServiceException):
    """Exception for AI service errors."""
    
    def __init__(self, message: str = "AI service error", details: dict = None):
        """
        Initialize AI service exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__('AI Service', message, details)


class WeatherServiceException(ExternalServiceException):
    """Exception for weather service errors."""
    
    def __init__(self, message: str = "Weather service error", details: dict = None):
        """
        Initialize weather service exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__('Weather Service', message, details)


class YouTubeServiceException(ExternalServiceException):
    """Exception for YouTube service errors."""
    
    def __init__(self, message: str = "YouTube service error", details: dict = None):
        """
        Initialize YouTube service exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__('YouTube Service', message, details)


class FileUploadException(AppException):
    """Exception for file upload errors."""
    
    def __init__(self, message: str = "File upload error", details: dict = None):
        """
        Initialize file upload exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code='FILE_UPLOAD_ERROR', details=details)


class DatabaseException(AppException):
    """Exception for database errors."""
    
    def __init__(self, message: str = "Database error", details: dict = None):
        """
        Initialize database exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code='DATABASE_ERROR', details=details)


class ConfigurationException(AppException):
    """Exception for configuration errors."""
    
    def __init__(self, message: str = "Configuration error", setting: str = None, details: dict = None):
        """
        Initialize configuration exception.
        
        Args:
            message: Error message
            setting: Setting that caused the error
            details: Additional error details
        """
        if setting:
            details = details or {}
            details['setting'] = setting
        super().__init__(message, code='CONFIGURATION_ERROR', details=details)


class RateLimitException(AppException):
    """Exception for rate limit errors."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None, details: dict = None):
        """
        Initialize rate limit exception.
        
        Args:
            message: Error message
            retry_after: Seconds to wait before retry
            details: Additional error details
        """
        if retry_after:
            details = details or {}
            details['retry_after'] = retry_after
        super().__init__(message, code='RATE_LIMIT_EXCEEDED', details=details)


class ConversationException(AppException):
    """Exception for conversation-related errors."""
    
    def __init__(self, message: str = "Conversation error", conversation_id: str = None, details: dict = None):
        """
        Initialize conversation exception.
        
        Args:
            message: Error message
            conversation_id: ID of the conversation
            details: Additional error details
        """
        if conversation_id:
            details = details or {}
            details['conversation_id'] = conversation_id
        super().__init__(message, code='CONVERSATION_ERROR', details=details)


class MusicException(AppException):
    """Exception for music-related errors."""
    
    def __init__(self, message: str = "Music service error", details: dict = None):
        """
        Initialize music exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code='MUSIC_ERROR', details=details)


class GameException(AppException):
    """Exception for game-related errors."""
    
    def __init__(self, message: str = "Game error", details: dict = None):
        """
        Initialize game exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code='GAME_ERROR', details=details)


class StudyException(AppException):
    """Exception for study-related errors."""
    
    def __init__(self, message: str = "Study service error", details: dict = None):
        """
        Initialize study exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, code='STUDY_ERROR', details=details)
