from django.db import models
from django.contrib.auth.models import User

class Sugerencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=[
        ('mejora', 'Mejora'),
        ('bug', 'Error/bug'),
        ('nueva_funcionalidad', 'Nueva funcionalidad'),
        ('otro', 'Otro'),
    ], default='mejora')
    estado = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ], default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.estado}"

    class Meta:
        ordering = ['-fecha_creacion']
