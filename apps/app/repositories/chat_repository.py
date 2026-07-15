"""
Chat repository.

Data access layer for chat operations.
"""

from ..models import ConversacionChat, MensajeChat


class ChatRepository:
    """Repository for chat data access."""
    
    @staticmethod
    def save_conversation(conversation):
        """Save conversation to database."""
        conversation.save()
        return conversation
    
    @staticmethod
    def delete_conversation(conversation_id: int, user):
        """Delete conversation."""
        conversation = ConversacionChat.objects.get(id=conversation_id, usuario=user)
        conversation.delete()
    
    @staticmethod
    def save_message(message):
        """Save message to database."""
        message.save()
        return message
