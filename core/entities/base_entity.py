"""
Base Entity

All domain entities inherit from this base class.
Provides common functionality like equality, identity, and validation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(kw_only=True)
class BaseEntity(ABC):
    """
    Base class for all domain entities.
    
    Entities have identity and lifecycle.
    """
    id: str = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate the entity's state.
        
        Returns:
            bool: True if valid, False otherwise
        """
        pass
    
    def mark_as_updated(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
