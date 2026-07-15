from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SystemSettings(models.Model):
    """Configuraciones globales del sistema"""
    site_name = models.CharField(max_length=100, default='MiniAmigixV')
    site_description = models.TextField(blank=True)
    maintenance_mode = models.BooleanField(default=False, help_text="Activar modo mantenimiento")
    maintenance_message = models.TextField(blank=True, help_text="Mensaje mostrado durante mantenimiento")
    allow_registration = models.BooleanField(default=True, help_text="Permitir nuevos registros")
    max_users = models.IntegerField(null=True, blank=True, help_text="Límite de usuarios (null = sin límite)")
    default_theme = models.CharField(max_length=20, default='dark', choices=[('light', 'Claro'), ('dark', 'Oscuro')])
    default_language = models.CharField(max_length=10, default='es', choices=[('es', 'Español'), ('en', 'English')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
    
    def __str__(self):
        return self.site_name


class FeatureFlag(models.Model):
    """Banderas de características para activar/desactivar funcionalidades"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bandera de Característica"
        verbose_name_plural = "Banderas de Características"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({'Activo' if self.is_active else 'Inactivo'})"


class ThemeSettings(models.Model):
    """Configuraciones de temas personalizados"""
    name = models.CharField(max_length=100, unique=True)
    primary_color = models.CharField(max_length=7, default='#6366f1', help_text="Color primario en HEX")
    secondary_color = models.CharField(max_length=7, default='#8b5cf6', help_text="Color secundario en HEX")
    background_color = models.CharField(max_length=7, default='#0f172a', help_text="Color de fondo en HEX")
    text_color = models.CharField(max_length=7, default='#f8fafc', help_text="Color de texto en HEX")
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Configuración de Tema"
        verbose_name_plural = "Configuraciones de Temas"
    
    def __str__(self):
        return self.name


class NotificationSettings(models.Model):
    """Configuraciones globales de notificaciones"""
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=False)
    sms_enabled = models.BooleanField(default=False)
    email_host = models.CharField(max_length=255, blank=True)
    email_port = models.IntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_host_user = models.EmailField(blank=True)
    email_host_password = models.CharField(max_length=255, blank=True)
    push_api_key = models.CharField(max_length=255, blank=True)
    sms_api_key = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Notificaciones"
        verbose_name_plural = "Configuraciones de Notificaciones"
    
    def __str__(self):
        return "Configuración de Notificaciones Globales"


class SecuritySettings(models.Model):
    """Configuraciones de seguridad del sistema"""
    max_login_attempts = models.IntegerField(default=5, help_text="Intentos máximos de login")
    lockout_duration = models.IntegerField(default=30, help_text="Duración de bloqueo en minutos")
    password_min_length = models.IntegerField(default=8, help_text="Longitud mínima de contraseña")
    password_require_uppercase = models.BooleanField(default=True)
    password_require_lowercase = models.BooleanField(default=True)
    password_require_numbers = models.BooleanField(default=True)
    password_require_special = models.BooleanField(default=True)
    session_timeout = models.IntegerField(default=60, help_text="Tiempo de sesión en minutos")
    two_factor_enabled = models.BooleanField(default=False)
    ip_whitelist = models.TextField(blank=True, help_text="Lista blanca de IPs (una por línea)")
    ip_blacklist = models.TextField(blank=True, help_text="Lista negra de IPs (una por línea)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Seguridad"
        verbose_name_plural = "Configuraciones de Seguridad"
    
    def __str__(self):
        return "Configuración de Seguridad"


class UserActivityLog(models.Model):
    """Registro de actividad de usuarios"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Cambio de Contraseña'),
        ('profile_update', 'Actualización de Perfil'),
        ('settings_change', 'Cambio de Configuración'),
        ('api_access', 'Acceso a API'),
        ('file_upload', 'Subida de Archivo'),
        ('file_download', 'Descarga de Archivo'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
