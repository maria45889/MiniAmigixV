"""
Email Value Object

Represents a validated email address.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    """
    Email value object with validation.
    """
    address: str
    
    def __post_init__(self):
        if not self._is_valid():
            raise ValueError(f"Invalid email address: {self.address}")
    
    def _is_valid(self) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.address) is not None
    
    def __str__(self) -> str:
        return self.address
    
    @property
    def domain(self) -> str:
        """Extract domain from email."""
        return self.address.split('@')[1]
    
    @property
    def local_part(self) -> str:
        """Extract local part from email."""
        return self.address.split('@')[0]
