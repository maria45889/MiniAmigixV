"""
Value Objects

Immutable objects that represent descriptive aspects of the domain.
They have no identity and are defined by their attributes.
"""

from .email import Email
from .timezone import Timezone
from .coordinates import Coordinates

__all__ = ['Email', 'Timezone', 'Coordinates']
