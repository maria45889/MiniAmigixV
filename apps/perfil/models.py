from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    tema = models.CharField(max_length=10, choices=[
        ('dark', 'Oscuro'),
        ('light', 'Claro'),
    ], default='dark')
    idioma = models.CharField(max_length=10, default='es')
    fecha_nacimiento = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    notificaciones_email = models.BooleanField(default=True)
    notificaciones_push = models.BooleanField(default=False)
    perfil_publico = models.BooleanField(default=True)
    # Accesibilidad
    tamano_fuente = models.CharField(max_length=10, choices=[
        ('small', 'Pequeño'),
        ('normal', 'Normal'),
        ('large', 'Grande'),
    ], default='normal')
    animaciones = models.BooleanField(default=True)
    sonidos = models.BooleanField(default=True)
    # Sesión
    actividad_en_linea = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username
