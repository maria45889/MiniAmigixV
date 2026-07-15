"""
Base Use Case

Base class for all use cases following the Command pattern.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional


@dataclass
class UseCaseRequest:
    """
    Base request object for use cases.
    Contains input data for the use case.
    """
    pass


@dataclass
class UseCaseResponse:
    """
    Base response object for use cases.
    Contains output data from the use case.
    """
    success: bool
    message: str = ""
    data: Optional[dict] = None
    errors: Optional[list] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


TRequest = TypeVar('TRequest', bound=UseCaseRequest)
TResponse = TypeVar('TResponse', bound=UseCaseResponse)


class UseCase(ABC, Generic[TRequest, TResponse]):
    """
    Base class for all use cases.
    
    Use cases orchestrate business logic and coordinate between
    the domain layer and infrastructure layer.
    """
    
    @abstractmethod
    def execute(self, request: TRequest) -> TResponse:
        """
        Execute the use case.
        
        Args:
            request: Input data for the use case
            
        Returns:
            Response object with result data
        """
        pass
    
    def validate_request(self, request: TRequest) -> bool:
        """
        Validate the request before execution.
        
        Args:
            request: Request to validate
            
        Returns:
            bool: True if valid
        """
        return True
    
    def create_error_response(self, message: str, errors: list = None) -> UseCaseResponse:
        """
        Create an error response.
        
        Args:
            message: Error message
            errors: List of specific errors
            
        Returns:
            Error response
        """
        return UseCaseResponse(
            success=False,
            message=message,
            errors=errors or []
        )
    
    def create_success_response(self, message: str, data: dict = None) -> UseCaseResponse:
        """
        Create a success response.
        
        Args:
            message: Success message
            data: Response data
            
        Returns:
            Success response
        """
        return UseCaseResponse(
            success=True,
            message=message,
            data=data or {}
        )
