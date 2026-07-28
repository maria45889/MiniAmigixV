# ============================================================================
# JUEGOS URLS
# ============================================================================

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AchievementViewSet,
    GameSessionViewSet,
    GameViewSet,
    ScoreViewSet,
    TicTacToeViewSet,
    UserStatsViewSet,
)

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'scores', ScoreViewSet, basename='score')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'sessions', GameSessionViewSet, basename='gamesession')
router.register(r'stats', UserStatsViewSet, basename='userstats')
router.register(r'tictactoe', TicTacToeViewSet, basename='tictactoe')

urlpatterns = [
    path('', include(router.urls)),
]
