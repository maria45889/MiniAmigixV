"""
Timezone Value Object

Represents a timezone with validation.
"""

from dataclasses import dataclass
from datetime import datetime
import pytz


@dataclass(frozen=True)
class Timezone:
    """
    Timezone value object with validation.
    """
    name: str
    
    def __post_init__(self):
        if not self._is_valid():
            raise ValueError(f"Invalid timezone: {self.name}")
    
    def _is_valid(self) -> bool:
        """Validate timezone."""
        return self.name in pytz.all_timezones
    
    def __str__(self) -> str:
        return self.name
    
    def convert_to_utc(self, dt: datetime) -> datetime:
        """Convert datetime from this timezone to UTC."""
        tz = pytz.timezone(self.name)
        if dt.tzinfo is None:
            dt = tz.localize(dt)
        return dt.astimezone(pytz.UTC)
    
    def convert_from_utc(self, dt: datetime) -> datetime:
        """Convert datetime from UTC to this timezone."""
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)
        return dt.astimezone(pytz.timezone(self.name))
