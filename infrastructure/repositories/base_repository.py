"""
Base Repository

Abstract base class for all repositories.
Provides common CRUD operations.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Base repository with common CRUD operations.
    
    Repositories abstract the data access layer and provide
    a collection-like interface for domain entities.
    """
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save an entity.
        
        Args:
            entity: Entity to save
            
        Returns:
            Saved entity
        """
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """
        Find an entity by its ID.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Find all entities.
        
        Returns:
            List of all entities
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity by ID.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            True if deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """
        Check if an entity exists.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            True if exists, False otherwise
        """
        pass
