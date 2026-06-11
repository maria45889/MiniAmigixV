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

    def __str__(self):
        return self.usuario.username
