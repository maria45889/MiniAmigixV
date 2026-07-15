"""
Chat serializers.
"""

from rest_framework import serializers
from ..models import ConversacionChat, MensajeChat


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    
    class Meta:
        model = MensajeChat
        fields = ['id', 'texto', 'es_usuario', 'imagen', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


class ChatSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model."""
    
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ConversacionChat
        fields = ['id', 'titulo', 'fecha_creacion', 'fecha_actualizacion', 'messages', 'message_count']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_message_count(self, obj):
        return obj.mensajes.count()
