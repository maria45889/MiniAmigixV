from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TranslationCache(models.Model):
    """Modelo para cachear traducciones y evitar llamadas excesivas a la API"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    texto_original = models.TextField()
    texto_traducido = models.TextField()
    idioma_origen = models.CharField(max_length=10, help_text='Código ISO del idioma de origen (ej: es, en, fr)')
    idioma_destino = models.CharField(max_length=10, help_text='Código ISO del idioma de destino (ej: es, en, fr)')
    idioma_detectado = models.CharField(max_length=10, null=True, blank=True, help_text='Idioma detectado automáticamente')
    
    fecha_consulta = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField()
    
    def __str__(self):
        return f"{self.idioma_origen} -> {self.idioma_destino}: {self.texto_original[:50]}..."
    
    class Meta:
        ordering = ['-fecha_consulta']
        verbose_name = 'Caché de Traducción'
        verbose_name_plural = 'Cachés de Traducción'
        unique_together = ['texto_original', 'idioma_origen', 'idioma_destino']
    
    def esta_expirado(self):
        return timezone.now() > self.fecha_expiracion
