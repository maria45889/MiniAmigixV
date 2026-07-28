from django.contrib import admin
from .models import Game, Score, Achievement, UserAchievement, GameSession, UserStats


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'icono', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['categoria', 'activo']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'juego', 'puntuacion', 'nivel', 'fecha']
    search_fields = ['usuario__username', 'juego__nombre']
    list_filter = ['juego', 'fecha']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'puntos_xp', 'juego', 'activo']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['juego', 'activo']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'logro', 'fecha_desbloqueo']
    search_fields = ['usuario__username', 'logro__nombre']
    list_filter = ['fecha_desbloqueo']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'juego', 'inicio', 'fin', 'puntuacion_final', 'gano']
    search_fields = ['usuario__username', 'juego__nombre']
    list_filter = ['juego', 'gano', 'inicio']


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'total_puntos_xp', 'total_monedas', 'juegos_completados', 
                    'racha_dias', 'nivel', 'insignia']
    search_fields = ['usuario__username']
    list_filter = ['nivel', 'racha_dias']
