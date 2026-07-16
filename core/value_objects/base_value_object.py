"""
Base Value Object

Immutable objects defined by their attributes rather than identity.
"""

from abc import ABC


class ValueObject(ABC):
    """Base class for domain value objects."""
