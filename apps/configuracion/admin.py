from django.contrib import admin
from .models import SystemSettings, FeatureFlag, ThemeSettings, NotificationSettings, SecuritySettings, UserActivityLog


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'maintenance_mode', 'allow_registration', 'default_theme', 'default_language', 'updated_at']
    list_filter = ['maintenance_mode', 'allow_registration', 'default_theme', 'default_language']
    search_fields = ['site_name', 'site_description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información General', {
            'fields': ('site_name', 'site_description')
        }),
        ('Modo Mantenimiento', {
            'fields': ('maintenance_mode', 'maintenance_message')
        }),
        ('Registro de Usuarios', {
            'fields': ('allow_registration', 'max_users')
        }),
        ('Configuraciones por Defecto', {
            'fields': ('default_theme', 'default_language')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'primary_color', 'secondary_color', 'is_default', 'is_active', 'created_at']
    list_filter = ['is_default', 'is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['is_default', 'is_active']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Información del Tema', {
            'fields': ('name', 'is_default', 'is_active')
        }),
        ('Colores', {
            'fields': ('primary_color', 'secondary_color', 'background_color', 'text_color')
        }),
        ('Creación', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ['email_enabled', 'push_enabled', 'sms_enabled', 'updated_at']
    list_filter = ['email_enabled', 'push_enabled', 'sms_enabled']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Tipos de Notificación', {
            'fields': ('email_enabled', 'push_enabled', 'sms_enabled')
        }),
        ('Configuración Email', {
            'fields': ('email_host', 'email_port', 'email_use_tls', 'email_host_user', 'email_host_password')
        }),
        ('API Keys', {
            'fields': ('push_api_key', 'sms_api_key')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SecuritySettings)
class SecuritySettingsAdmin(admin.ModelAdmin):
    list_display = ['max_login_attempts', 'lockout_duration', 'password_min_length', 'two_factor_enabled', 'updated_at']
    list_filter = ['two_factor_enabled', 'password_require_uppercase', 'password_require_lowercase', 'password_require_numbers', 'password_require_special']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Intentos de Login', {
            'fields': ('max_login_attempts', 'lockout_duration')
        }),
        ('Requisitos de Contraseña', {
            'fields': ('password_min_length', 'password_require_uppercase', 'password_require_lowercase', 'password_require_numbers', 'password_require_special')
        }),
        ('Sesión y 2FA', {
            'fields': ('session_timeout', 'two_factor_enabled')
        }),
        ('Control de IPs', {
            'fields': ('ip_whitelist', 'ip_blacklist')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'ip_address', 'description']
    readonly_fields = ['user', 'action', 'ip_address', 'user_agent', 'description', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Solo lectura, los logs se crean automáticamente
    
    def has_change_permission(self, request, obj=None):
        return False  # Solo lectura
