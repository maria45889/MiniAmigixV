from django.db import models
from django.contrib.auth.models import User

class Visitante(models.Model):
    """Modelo para guardar información de visitantes que envían sugerencias sin cuenta"""
    nombre = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    fecha_primera_interaccion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_interaccion = models.DateTimeField(auto_now=True)
    total_sugerencias = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.email or 'Sin email'})"

    class Meta:
        ordering = ['-fecha_ultima_interaccion']
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

class Sugerencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    visitante = models.ForeignKey(Visitante, on_delete=models.SET_NULL, null=True, blank=True, related_name='sugerencias')
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
    respuesta_admin = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    respondido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sugerencias_respondidas')

    def __str__(self):
        return f"{self.titulo} - {self.estado}"

    class Meta:
        ordering = ['-fecha_creacion']
