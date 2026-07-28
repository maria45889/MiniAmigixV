# ============================================================================
# MÚSICA URLS
# ============================================================================

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteViewSet,
    ListeningHistoryViewSet,
    MusicSettingsViewSet,
    PlaylistViewSet,
    SongViewSet,
)

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'history', ListeningHistoryViewSet, basename='listeninghistory')
router.register(r'settings', MusicSettingsViewSet, basename='musicsettings')

urlpatterns = [
    path('', include(router.urls)),
]
