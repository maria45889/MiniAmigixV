from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Nota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notas')
    contenido = models.TextField()
    color = models.CharField(max_length=7, default='#fef08a', help_text='Color de la nota en formato HEX')
    fijada = models.BooleanField(default=False, help_text='Si la nota está fijada arriba')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fijada', '-fecha_creacion']
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

class StudyCategory(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    icono = models.CharField(max_length=50, default='📚')
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría de Estudio'
        verbose_name_plural = 'Categorías de Estudio'

class StudyResource(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recursos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField()
    categoria = models.ForeignKey(StudyCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='recursos')
    tipo_recurso = models.CharField(max_length=50, choices=[
        ('nota', 'Nota'),
        ('resumen', 'Resumen'),
        ('guia', 'Guía'),
        ('ejercicio', 'Ejercicio'),
        ('video', 'Video'),
        ('enlace', 'Enlace'),
    ], default='nota')
    etiquetas = models.CharField(max_length=200, blank=True, null=True, help_text='Etiquetas separadas por comas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    es_publico = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Recurso de Estudio'
        verbose_name_plural = 'Recursos de Estudio'

class StudyProgress(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progreso_estudio')
    recurso = models.ForeignKey(StudyResource, on_delete=models.CASCADE, related_name='progreso')
    porcentaje_completado = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    ultima_actividad = models.DateTimeField(auto_now=True)
    notas_usuario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.recurso.titulo}: {self.porcentaje_completado}%"

    class Meta:
        ordering = ['-ultima_actividad']
        verbose_name = 'Progreso de Estudio'
        verbose_name_plural = 'Progresos de Estudio'
        unique_together = ['usuario', 'recurso']

class StudySession(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sesiones_estudio')
    duracion_segundos = models.IntegerField(default=0)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    tipo_sesion = models.CharField(max_length=20, choices=[
        ('cronometro', 'Cronómetro'),
        ('pomodoro', 'Pomodoro'),
        ('temporizador', 'Temporizador'),
    ], default='cronometro')

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_sesion} - {self.fecha_inicio.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Sesión de Estudio'
        verbose_name_plural = 'Sesiones de Estudio'

class PomodoroSession(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoros')
    duracion_minutos = models.IntegerField(default=25)
    completado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=[
        ('trabajo', 'Trabajo'),
        ('descanso_corto', 'Descanso Corto'),
        ('descanso_largo', 'Descanso Largo'),
    ], default='trabajo')

    def __str__(self):
        estado = "Completado" if self.completado else "No completado"
        return f"{self.usuario.username} - {self.tipo} - {estado} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Sesión Pomodoro'
        verbose_name_plural = 'Sesiones Pomodoro'

class DailyStats(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estadisticas_diarias')
    fecha = models.DateField(unique=True)
    tiempo_estudiado_segundos = models.IntegerField(default=0)
    pomodoros_completados = models.IntegerField(default=0)
    notas_creadas = models.IntegerField(default=0)
    resumenes_creados = models.IntegerField(default=0)
    racha_dias = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha} - {self.tiempo_estudiado_segundos // 60} min"

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Estadística Diaria'
        verbose_name_plural = 'Estadísticas Diarias'
        unique_together = ['usuario', 'fecha']
