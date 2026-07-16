"""
Presentation Layer

This layer handles HTTP requests, responses, and API interfaces.
It contains views, serializers, and controllers.
"""

from .api import BaseAPIView
from .serializers import Serializer

__all__ = ['BaseAPIView', 'Serializer']
