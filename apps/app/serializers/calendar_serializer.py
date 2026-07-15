"""
Calendar serializers.
"""

from rest_framework import serializers
from eventos.models import Evento


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""
    
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'descripcion', 'fecha', 'hora', 'ubicacion', 'tipo', 'completado']
        read_only_fields = ['id']
