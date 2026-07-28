from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SongViewSet, PlaylistViewSet, FavoriteViewSet,
    ListeningHistoryViewSet, MusicSettingsViewSet
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
