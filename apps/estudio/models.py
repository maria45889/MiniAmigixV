from django.db import models
from django.contrib.auth.models import User
import uuid

class Nota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notas')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
    
    def __str__(self):
        return self.contenido[:50] + '...' if len(self.contenido) > 50 else self.contenido

class Resumen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumenes')
    texto_original = models.TextField()
    resumen = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Resumen'
        verbose_name_plural = 'Resúmenes'
    
    def __str__(self):
        return f"Resumen del {self.fecha_creacion.strftime('%d/%m/%Y')}"
