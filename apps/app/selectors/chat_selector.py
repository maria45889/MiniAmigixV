"""
Chat selector.

Database queries for chat operations.
"""

from ..models import ConversacionChat, MensajeChat


class ChatSelector:
    """Selector for chat-related queries."""
    
    @staticmethod
    def get_by_user_and_id(user, conversation_id: str):
        """Get conversation by user and ID."""
        return ConversacionChat.objects.filter(usuario=user, id=conversation_id).first()
    
    @staticmethod
    def get_first_by_user(user):
        """Get first conversation for user."""
        return ConversacionChat.objects.filter(usuario=user).first()
    
    @staticmethod
    def create_for_user(user, title: str = 'Chat Principal'):
        """Create a new conversation for user."""
        return ConversacionChat.objects.create(usuario=user, titulo=title)
    
    @staticmethod
    def get_all_by_user(user):
        """Get all conversations for user ordered by update date."""
        return ConversacionChat.objects.filter(usuario=user).select_related('usuario').order_by('-fecha_actualizacion')
    
    @staticmethod
    def get_or_create_main(user):
        """Get or create main conversation for user."""
        conversation = ChatSelector.get_first_by_user(user)
        if not conversation:
            conversation = ChatSelector.create_for_user(user)
        return conversation
    
    @staticmethod
    def count_by_user(user):
        """Count conversations for user."""
        return ConversacionChat.objects.filter(usuario=user).count()
    
    @staticmethod
    def create_message(conversation, is_user: bool, text: str, image=None):
        """Create a message for a conversation."""
        return MensajeChat.objects.create(
            conversacion=conversation,
            es_usuario=is_user,
            texto=text,
            imagen=image
        )
    
    @staticmethod
    def get_recent_messages(conversation, limit: int = 10):
        """Get recent messages from conversation (most recent first)."""
        return MensajeChat.objects.filter(
            conversacion=conversation
        ).order_by('-fecha_creacion')[:limit]
    
    @staticmethod
    def get_recent_chronological(conversation, limit: int = 10):
        """Get recent messages in chronological order."""
        return list(ChatSelector.get_recent_messages(conversation, limit))[::-1]
    
    @staticmethod
    def get_all_messages(conversation):
        """Get all messages for a conversation."""
        return conversation.mensajes.all().select_related('conversacion').order_by('fecha_creacion')
