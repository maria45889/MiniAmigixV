from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class WeatherCache(models.Model):
    """Modelo para cachear consultas del clima y evitar llamadas excesivas a la API"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='ES')
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    
    # Datos del clima actual
    temperatura = models.FloatField(help_text='Temperatura en Celsius')
    sensacion_termica = models.FloatField(null=True, blank=True)
    humedad = models.IntegerField(null=True, blank=True)
    presion = models.IntegerField(null=True, blank=True)
    viento_velocidad = models.FloatField(null=True, blank=True)
    viento_direccion = models.IntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length=200)
    icono = models.CharField(max_length=200, null=True, blank=True)
    
    # Datos adicionales
    temp_max = models.FloatField(null=True, blank=True, help_text='Temperatura máxima del día')
    temp_min = models.FloatField(null=True, blank=True, help_text='Temperatura mínima del día')
    visibilidad = models.FloatField(null=True, blank=True, help_text='Visibilidad en km')
    uv_index = models.IntegerField(null=True, blank=True, help_text='Índice UV')
    probabilidad_lluvia = models.IntegerField(null=True, blank=True, help_text='Probabilidad de lluvia %')
    amanecer = models.TimeField(null=True, blank=True, help_text='Hora de amanecer')
    atardecer = models.TimeField(null=True, blank=True, help_text='Hora de atardecer')
    
    # Datos del pronóstico (JSON)
    pronostico = models.JSONField(default=dict, help_text='Pronóstico para los próximos días')
    
    fecha_consulta = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField()
    
    def __str__(self):
        return f"{self.ciudad}, {self.pais} - {self.temperatura}°C"
    
    class Meta:
        ordering = ['-fecha_consulta']
        verbose_name = 'Caché de Clima'
        verbose_name_plural = 'Cachés de Clima'
    
    def esta_expirado(self):
        return timezone.now() > self.fecha_expiracion
    
    def guardar_pronostico(self, pronostico_data):
        """Guarda los datos del pronóstico en formato JSON"""
        self.pronostico = pronostico_data
        self.save()
