"""
Base Serializer

Base class for converting objects to and from API representations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class Serializer(ABC):
    """Base serializer for API data conversion."""

    @abstractmethod
    def serialize(self, obj: Any) -> Dict:
        """Convert an object to a dictionary."""
        pass
