from django.contrib import admin
from .models import Perfil, UserActivity, ProfileAchievement, UserProfileAchievement

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tema', 'idioma', 'nivel', 'experiencia', 'notificaciones_push']
    list_filter = ['tema', 'idioma', 'notificaciones_push', 'color_acento']
    search_fields = ['usuario__username', 'bio', 'ubicacion']

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo_actividad', 'fecha']
    list_filter = ['tipo_actividad', 'fecha']
    search_fields = ['usuario__username', 'descripcion']

@admin.register(ProfileAchievement)
class ProfileAchievementAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'tipo', 'puntos_requeridos']
    list_filter = ['tipo']
    search_fields = ['nombre', 'descripcion']

@admin.register(UserProfileAchievement)
class UserProfileAchievementAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'logro', 'fecha_desbloqueado']
    list_filter = ['fecha_desbloqueado']
    search_fields = ['usuario__username', 'logro__nombre']
