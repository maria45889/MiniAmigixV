from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CategoriaEvento(models.TextChoices):
    PERSONAL = 'personal', '🎂 Personal'
    TRABAJO = 'trabajo', '💼 Trabajo'
    ESTUDIOS = 'estudios', '📚 Estudios'
    SALUD = 'salud', '🏥 Salud'
    FIESTA = 'fiesta', '🎉 Fiesta'
    OTRO = 'otro', '📌 Otro'

class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField()
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaEvento.choices,
        default=CategoriaEvento.PERSONAL,
        help_text='Categoría del evento'
    )
    ubicacion = models.CharField(max_length=200, blank=True, null=True, help_text='Ubicación del evento')
    recordatorio_activo = models.BooleanField(default=True, help_text='Activar recordatorio')
    recordatorio_minutos_antes = models.IntegerField(
        default=30,
        help_text='Minutos antes del evento para el recordatorio'
    )
    notificacion_1dia_enviada = models.BooleanField(default=False)
    notificacion_1hora_enviada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    def get_categoria_emoji(self):
        return dict(CategoriaEvento.choices).get(self.categoria, '').split(' ')[0] if self.categoria else '📌'

    def get_categoria_color(self):
        colors = {
            'personal': '#ec4899',  # Rosa
            'trabajo': '#3b82f6',   # Azul
            'estudios': '#8b5cf6',  # Morado
            'salud': '#22c55e',     # Verde
            'fiesta': '#f97316',    # Naranja
            'otro': '#64748b'       # Gris
        }
        return colors.get(self.categoria, '#64748b')

    class Meta:
        ordering = ['fecha']
