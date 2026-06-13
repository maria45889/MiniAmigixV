from django.db import models
from django.contrib.auth.models import User

class TicketSoporte(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=[
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ], default='media')
    estado = models.CharField(max_length=20, choices=[
        ('abierto', 'Abierto'),
        ('en_proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ], default='abierto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(blank=True, null=True)
    respuesta_admin = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    respondido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_respondidos')

    def __str__(self):
        return f"{self.asunto} - {self.estado}"

    class Meta:
        ordering = ['-fecha_creacion']
