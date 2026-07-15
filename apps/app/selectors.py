"""
Selectors for database queries.

Contains all ORM queries separated from views for better organization.
"""

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from .models import (
    ConversacionChat, MensajeChat, Cancion, Playlist, 
    Favorite, Game, Score, Achievement, UserAchievement,
    EstadoAnimo, RecomendacionEntretenimiento
)
from eventos.models import Evento
from notificaciones.models import Notificacion
from estudio.models import StudyResource, StudyCategory, StudyProgress


class UserSelectors:
    """Selectors for User model queries."""
    
    @staticmethod
    def username_exists(username: str) -> bool:
        """Check if a username exists."""
        return User.objects.filter(username=username).exists()
    
    @staticmethod
    def email_exists(email: str) -> bool:
        """Check if an email exists."""
        return User.objects.filter(email=email).exists()
    
    @staticmethod
    def get_by_username(username: str):
        """Get user by username."""
        return User.objects.filter(username=username).first()
    
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        """Create a new user."""
        return User.objects.create_user(username=username, email=email, password=password)


class SiteSelectors:
    """Selectors for Site and SocialApp queries."""
    
    @staticmethod
    def get_current_site():
        """Get the current site."""
        return Site.objects.get_current()
    
    @staticmethod
    def get_google_social_apps(site):
        """Get Google OAuth apps for the current site."""
        return SocialApp.objects.filter(sites=site, provider='google')


class ConversationSelectors:
    """Selectors for ConversationChat model queries."""
    
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
        return ConversacionChat.objects.filter(usuario=user).order_by('-fecha_actualizacion')
    
    @staticmethod
    def get_or_create_main(user):
        """Get or create main conversation for user."""
        conversation = ConversationSelectors.get_first_by_user(user)
        if not conversation:
            conversation = ConversationSelectors.create_for_user(user)
        return conversation


class MessageSelectors:
    """Selectors for MensajeChat model queries."""
    
    @staticmethod
    def create_for_conversation(conversation, is_user: bool, text: str, image=None):
        """Create a message for a conversation."""
        return MensajeChat.objects.create(
            conversacion=conversation,
            es_usuario=is_user,
            texto=text,
            imagen=image
        )
    
    @staticmethod
    def get_recent_by_conversation(conversation, limit: int = 10):
        """Get recent messages from conversation (most recent first)."""
        return MensajeChat.objects.filter(
            conversacion=conversation
        ).order_by('-fecha_creacion')[:limit]
    
    @staticmethod
    def get_recent_chronological(conversation, limit: int = 10):
        """Get recent messages in chronological order."""
        return list(ConversationSelectors.get_recent_by_conversation(conversation, limit))[::-1]
    
    @staticmethod
    def get_all_by_conversation(conversation):
        """Get all messages for a conversation."""
        return conversation.mensajes.all().order_by('fecha_creacion')


class EventSelectors:
    """Selectors for Evento model queries."""
    
    @staticmethod
    def get_upcoming_events(days: int = 5):
        """Get events in the next N days."""
        from datetime import date, timedelta
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=days)
        return Evento.objects.filter(fecha__gte=hoy, fecha__lte=fecha_limite).order_by('fecha')
    
    @staticmethod
    def get_for_clock_widget(days: int = 3, limit: int = 3):
        """Get events for the clock widget."""
        return EventSelectors.get_upcoming_events(days)[:limit]
    
    @staticmethod
    def count_all():
        """Count all events."""
        return Evento.objects.count()


class NotificationSelectors:
    """Selectors for Notificacion model queries."""
    
    @staticmethod
    def create_for_user(user, title: str, message: str, notification_type: str = 'info', link: str = ''):
        """Create a notification for user."""
        return Notificacion.objects.create(
            usuario=user,
            titulo=title,
            mensaje=message,
            tipo=notification_type,
            enlace=link
        )


class MusicSelectors:
    """Selectors for music-related models."""
    
    @staticmethod
    def get_recent_songs(user, limit: int = 20):
        """Get recent songs for user."""
        return Cancion.objects.filter(usuario=user).order_by('-fecha_agregada')[:limit]
    
    @staticmethod
    def get_playlists(user):
        """Get all playlists for user."""
        return Playlist.objects.filter(usuario=user).order_by('-fecha_actualizacion')
    
    @staticmethod
    def get_playlist_by_id(playlist_id: int, user):
        """Get playlist by ID and user."""
        return Playlist.objects.get(id=playlist_id, usuario=user)
    
    @staticmethod
    def get_song_by_id(song_id: int, user):
        """Get song by ID and user."""
        return Cancion.objects.get(id=song_id, usuario=user)
    
    @staticmethod
    def create_playlist(user, name: str, description: str = ''):
        """Create a new playlist."""
        return Playlist.objects.create(
            usuario=user,
            nombre=name,
            descripcion=description
        )
    
    @staticmethod
    def get_favorites(user):
        """Get favorite songs for user."""
        favoritos_canciones = Favorite.objects.filter(usuario=user).select_related('cancion')
        return [fav.cancion for fav in favoritos_canciones]
    
    @staticmethod
    def get_or_create_favorite(user, song):
        """Get or create favorite for user and song."""
        return Favorite.objects.get_or_create(usuario=user, cancion=song)
    
    @staticmethod
    def count_songs(user):
        """Count songs for user."""
        return Cancion.objects.filter(usuario=user).count()


class GameSelectors:
    """Selectors for game-related models."""
    
    @staticmethod
    def get_active_games():
        """Get all active games."""
        return Game.objects.filter(activo=True)
    
    @staticmethod
    def get_scores(user):
        """Get scores for user."""
        return Score.objects.filter(usuario=user).select_related('juego')
    
    @staticmethod
    def get_achievements(user):
        """Get achievements for user."""
        return UserAchievement.objects.filter(usuario=user).select_related('logro')
    
    @staticmethod
    def scores_exist(user):
        """Check if user has any scores."""
        return Score.objects.filter(usuario=user).exists()


class StudySelectors:
    """Selectors for study-related models."""
    
    @staticmethod
    def get_all_categories():
        """Get all study categories."""
        return StudyCategory.objects.all()
    
    @staticmethod
    def get_resources(user):
        """Get resources for user."""
        return StudyResource.objects.filter(usuario=user).select_related('categoria')
    
    @staticmethod
    def get_progress(user):
        """Get study progress for user."""
        return StudyProgress.objects.filter(usuario=user).select_related('recurso')
