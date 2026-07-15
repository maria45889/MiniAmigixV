"""
Infrastructure Layer

This layer contains external concerns like databases, APIs, and frameworks.
It implements interfaces defined in the domain layer.
"""

from .repositories import BaseRepository
from .external_services import ExternalService

__all__ = ['BaseRepository', 'ExternalService']
