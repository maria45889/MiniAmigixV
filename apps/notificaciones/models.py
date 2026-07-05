from django.db import models
from django.contrib.auth.models import User

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ('info', 'Información'),
        ('success', 'Éxito'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('evento', 'Evento'),
        ('chat_ia', 'Chat IA'),
        ('musica', 'Música'),
        ('estudio', 'Estudio'),
        ('soporte', 'Soporte'),
        ('sistema', 'Sistema'),
    ], default='info')
    categoria = models.CharField(max_length=50, choices=[
        ('chat_ia', 'Chat IA'),
        ('musica', 'Música'),
        ('estudio', 'Estudio'),
        ('evento', 'Eventos'),
        ('soporte', 'Soporte'),
        ('sistema', 'Sistema'),
        ('clima', 'Clima'),
        ('traductor', 'Traductor'),
        ('juegos', 'Juegos'),
    ], default='sistema')
    prioridad = models.CharField(max_length=20, choices=[
        ('alta', 'Alta'),
        ('normal', 'Normal'),
        ('baja', 'Baja'),
    ], default='normal')
    leida = models.BooleanField(default=False)
    fijada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        ordering = ['-fijada', '-prioridad', '-fecha_creacion']
