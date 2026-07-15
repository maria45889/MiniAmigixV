"""
Use Cases

Application use cases that orchestrate business logic.
Each use case represents a specific user interaction or system operation.
"""

from .base_use_case import UseCase, UseCaseRequest, UseCaseResponse
from .user_use_cases import (
    CreateUserUseCase,
    UpdateUserProfileUseCase,
    GetUserUseCase,
    DeleteUserUseCase
)
from .conversation_use_cases import (
    CreateConversationUseCase,
    AddMessageUseCase,
    GetConversationUseCase,
    ListConversationsUseCase
)
from .event_use_cases import (
    CreateEventUseCase,
    UpdateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    DeleteEventUseCase
)
from .notification_use_cases import (
    CreateNotificationUseCase,
    MarkNotificationAsReadUseCase,
    ListNotificationsUseCase
)

__all__ = [
    'UseCase',
    'UseCaseRequest',
    'UseCaseResponse',
    'CreateUserUseCase',
    'UpdateUserProfileUseCase',
    'GetUserUseCase',
    'DeleteUserUseCase',
    'CreateConversationUseCase',
    'AddMessageUseCase',
    'GetConversationUseCase',
    'ListConversationsUseCase',
    'CreateEventUseCase',
    'UpdateEventUseCase',
    'GetEventUseCase',
    'ListEventsUseCase',
    'DeleteEventUseCase',
    'CreateNotificationUseCase',
    'MarkNotificationAsReadUseCase',
    'ListNotificationsUseCase'
]
