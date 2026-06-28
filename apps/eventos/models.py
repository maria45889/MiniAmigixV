from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField()
    notificacion_1dia_enviada = models.BooleanField(default=False)
    notificacion_1hora_enviada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        ordering = ['fecha']
