from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Nota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notas')
    titulo = models.CharField(max_length=200, blank=True, default='', help_text='Título de la nota')
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
        titulo_display = self.titulo if self.titulo else self.contenido[:50]
        return titulo_display + '...' if len(titulo_display) > 50 else titulo_display

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

class UserProfile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_amigis')
    xp = models.IntegerField(default=0, help_text='Puntos de experiencia')
    nivel = models.IntegerField(default=1, help_text='Nivel actual del usuario')
    monedas = models.IntegerField(default=100, help_text='Monedas Amigis')
    racha_actual = models.IntegerField(default=0, help_text='Días consecutivos de actividad')
    racha_maxima = models.IntegerField(default=0, help_text='Racha máxima histórica')
    misiones_completadas = models.IntegerField(default=0, help_text='Total de misiones completadas')
    fecha_ultima_actividad = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil Amigis'
        verbose_name_plural = 'Perfiles Amigis'
    
    def __str__(self):
        return f"{self.usuario.username} - Nivel {self.nivel} - {self.monedas} monedas"
    
    def agregar_xp(self, cantidad):
        self.xp += cantidad
        xp_para_nivel = self.nivel * 100
        while self.xp >= xp_para_nivel:
            self.xp -= xp_para_nivel
            self.nivel += 1
            xp_para_nivel = self.nivel * 100
        self.save()
    
    def agregar_monedas(self, cantidad):
        self.monedas += cantidad
        self.save()

class MetaDiaria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas_diarias')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)
    orden = models.IntegerField(default=0, help_text='Orden de visualización')
    
    class Meta:
        ordering = ['orden', '-fecha']
        verbose_name = 'Meta Diaria'
        verbose_name_plural = 'Metas Diarias'
        unique_together = ['usuario', 'titulo', 'fecha']
    
    def __str__(self):
        estado = "✓" if self.completada else "☐"
        return f"{estado} {self.titulo} - {self.fecha.strftime('%d/%m/%Y')}"

class Mision(models.Model):
    CATEGORIAS = [
        ('curiosidad', '🧠 Algo curioso'),
        ('vida', '💰 Algo para mi vida'),
        ('practico', '🍳 Algo práctico'),
        ('creativo', '🎨 Algo creativo'),
        ('mundo', '🌎 Algo del mundo'),
        ('habilidades', '🗣️ Algo para mejorar mis habilidades'),
        ('sorprendeme', '🎲 Sorpréndeme'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    xp_recompensa = models.IntegerField(default=50)
    monedas_recompensa = models.IntegerField(default=20)
    dificultad = models.CharField(max_length=20, choices=[
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
    ], default='facil')
    contenido_interactivo = models.JSONField(default=dict, help_text='Contenido de la misión en formato JSON')
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Misión Amigis'
        verbose_name_plural = 'Misiones Amigis'
    
    def __str__(self):
        return f"{self.titulo} - {self.get_categoria_display()}"

class MisionCompletada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='misiones_completadas')
    mision = models.ForeignKey(Mision, on_delete=models.CASCADE, related_name='completaciones')
    fecha_completacion = models.DateTimeField(auto_now_add=True)
    xp_ganado = models.IntegerField()
    monedas_ganadas = models.IntegerField()
    
    class Meta:
        ordering = ['-fecha_completacion']
        verbose_name = 'Misión Completada'
        verbose_name_plural = 'Misiones Completadas'
        unique_together = ['usuario', 'mision']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.mision.titulo}"

class LeccionRapida(models.Model):
    titulo = models.CharField(max_length=200)
    pregunta = models.CharField(max_length=300)
    contenido = models.TextField(help_text='Contenido educativo breve')
    tiempo_estimado_minutos = models.IntegerField(default=5)
    categoria = models.CharField(max_length=50, default='general')
    xp_recompensa = models.IntegerField(default=30)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Lección Rápida'
        verbose_name_plural = 'Lecciones Rápidas'
    
    def __str__(self):
        return f"{self.titulo} ({self.tiempo_estimado_minutos} min)"

class Insignia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='🏆')
    xp_requerido = models.IntegerField(default=0)
    misiones_requeridas = models.IntegerField(default=0)
    condicion_especial = models.TextField(blank=True, null=True, help_text='Condición especial para obtener la insignia')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Insignia'
        verbose_name_plural = 'Insignias'
    
    def __str__(self):
        return f"{self.icono} {self.nombre}"

class InsigniaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insignias')
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE, related_name='ganadores')
    fecha_obtenida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_obtenida']
        verbose_name = 'Insignia de Usuario'
        verbose_name_plural = 'Insignias de Usuarios'
        unique_together = ['usuario', 'insignia']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.insignia.nombre}"

class Accesorio(models.Model):
    CATEGORIAS = [
        ('ropa', '👕 Ropa'),
        ('accesorios', '🎮 Accesorios'),
        ('decoracion', '🏠 Decoración'),
        ('especial', '✨ Especial'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='🎁')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.IntegerField(default=50)
    xp_requerido = models.IntegerField(default=0, help_text='XP mínimo requerido para comprar')
    limitado = models.BooleanField(default=False, help_text='Si es un artículo limitado')
    stock = models.IntegerField(default=0, help_text='Stock disponible si es limitado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['precio', 'nombre']
        verbose_name = 'Accesorio'
        verbose_name_plural = 'Accesorios'
    
    def __str__(self):
        return f"{self.icono} {self.nombre} - {self.precio} monedas"

class AccesorioUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accesorios')
    accesorio = models.ForeignKey(Accesorio, on_delete=models.CASCADE, related_name='propietarios')
    fecha_compra = models.DateTimeField(auto_now_add=True)
    equipado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_compra']
        verbose_name = 'Accesorio de Usuario'
        verbose_name_plural = 'Accesorios de Usuarios'
        unique_together = ['usuario', 'accesorio']
    
    def __str__(self):
        estado = "Equipado" if self.equipado else "No equipado"
        return f"{self.usuario.username} - {self.accesorio.nombre} ({estado})"
