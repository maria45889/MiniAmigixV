from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField()
    notificacion_1dia_enviada = models.BooleanField(default=False)
    notificacion_1hora_enviada = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
