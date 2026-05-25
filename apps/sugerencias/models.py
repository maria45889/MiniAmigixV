from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Sugerencia(models.Model):
    SUGERENCIA_TIPOS = [
        ('idea', 'Idea'),
        ('mejora', 'Mejora'),
        ('reporte', 'Reporte de Error'),
        ('pregunta', 'Pregunta'),
        ('elogio', 'Elogio'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sugerencias')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=SUGERENCIA_TIPOS, default='idea')
    creado_en = models.DateTimeField(default=timezone.now)
    respuesta = models.TextField(blank=True, null=True)
    respondido_en = models.DateTimeField(blank=True, null=True)
    respondido_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sugerencias_respondidas'
    )

    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('en_revision', 'En Revisión'),
            ('resuelta', 'Resuelta'),
            ('rechazada', 'Rechazada')
        ],
        default='pendiente'
    )
    
    class Meta:
        ordering = ['-creado_en']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"