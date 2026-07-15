"""
Coordinates Value Object

Represents geographic coordinates.
"""

from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt


@dataclass(frozen=True)
class Coordinates:
    """
    Geographic coordinates value object.
    """
    latitude: float
    longitude: float
    
    def __post_init__(self):
        if not self._is_valid():
            raise ValueError(
                f"Invalid coordinates: lat={self.latitude}, lon={self.longitude}"
            )
    
    def _is_valid(self) -> bool:
        """Validate coordinates."""
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180
    
    def distance_to(self, other: 'Coordinates') -> float:
        """
        Calculate distance to another coordinates using Haversine formula.
        
        Returns:
            float: Distance in kilometers
        """
        R = 6371  # Earth's radius in km
        
        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(other.latitude), radians(other.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        
        return R * c
    
    def __str__(self) -> str:
        return f"({self.latitude}, {self.longitude})"
