from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField()

    def __str__(self):
        return self.titulo
