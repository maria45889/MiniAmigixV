from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Game(models.Model):
    """Modelo para representar un juego"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=[
        ('clasico', 'Clásico'),
        ('ia', 'Juego con IA'),
        ('educativo', 'Educativo'),
        ('arcade', 'Arcade'),
    ])
    icono = models.CharField(max_length=50, default='🎮')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.icono} {self.nombre}"
    
    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'


class Score(models.Model):
    """Modelo para representar puntuaciones de juegos"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puntuaciones')
    juego = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='puntuaciones')
    puntuacion = models.IntegerField()
    nivel = models.IntegerField(default=1)
    tiempo_jugado = models.IntegerField(default=0, help_text='Tiempo en segundos')
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.juego.nombre}: {self.puntuacion}"
    
    class Meta:
        ordering = ['-puntuacion', '-fecha']
        verbose_name = 'Puntuación'
        verbose_name_plural = 'Puntuaciones'
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'juego', 'fecha'],
                name='unique_user_game_date'
            )
        ]


class Achievement(models.Model):
    """Modelo para representar logros desbloqueables"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='🏅')
    puntos_xp = models.IntegerField(default=0, help_text='Puntos de experiencia otorgados')
    juego = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='logros', null=True, blank=True)
    condicion = models.JSONField(default=dict, help_text='Condiciones para desbloquear el logro')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.icono} {self.nombre}"
    
    class Meta:
        ordering = ['puntos_xp', 'nombre']
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'


class UserAchievement(models.Model):
    """Modelo para representar logros desbloqueados por usuarios"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logros_desbloqueados')
    logro = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='usuarios_desbloqueados')
    fecha_desbloqueo = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.logro.nombre}"
    
    class Meta:
        ordering = ['-fecha_desbloqueo']
        verbose_name = 'Logro de Usuario'
        verbose_name_plural = 'Logros de Usuarios'
        unique_together = ['usuario', 'logro']


class GameSession(models.Model):
    """Modelo para registrar sesiones de juego"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sesiones_juego')
    juego = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sesiones')
    inicio = models.DateTimeField(auto_now_add=True)
    fin = models.DateTimeField(null=True, blank=True)
    puntuacion_final = models.IntegerField(null=True, blank=True)
    nivel_alcanzado = models.IntegerField(default=1)
    gano = models.BooleanField(null=True, blank=True)
    
    def duracion(self):
        if self.fin:
            return (self.fin - self.inicio).total_seconds()
        return None
    
    def __str__(self):
        return f"{self.usuario.username} - {self.juego.nombre} ({self.inicio})"
    
    class Meta:
        ordering = ['-inicio']
        verbose_name = 'Sesión de Juego'
        verbose_name_plural = 'Sesiones de Juego'


class UserStats(models.Model):
    """Modelo para estadísticas generales del usuario en juegos"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estadisticas_juegos')
    total_puntos_xp = models.IntegerField(default=0)
    total_monedas = models.IntegerField(default=0)
    juegos_completados = models.IntegerField(default=0)
    racha_dias = models.IntegerField(default=0)
    ultima_jugada = models.DateField(null=True, blank=True)
    nivel = models.IntegerField(default=1)
    insignia = models.CharField(max_length=100, default='Novato')
    
    def __str__(self):
        return f"Estadísticas de {self.usuario.username}"
    
    class Meta:
        verbose_name = 'Estadísticas de Usuario'
        verbose_name_plural = 'Estadísticas de Usuarios'
    
    def agregar_xp(self, xp):
        self.total_puntos_xp += xp
        # Calcular nuevo nivel (cada 100 XP = 1 nivel)
        nuevo_nivel = (self.total_puntos_xp // 100) + 1
        if nuevo_nivel > self.nivel:
            self.nivel = nuevo_nivel
            # Actualizar insignia según nivel
            insignias = {
                1: 'Novato',
                5: 'Aprendiz',
                10: 'Jugador',
                20: 'Experto',
                30: 'Maestro',
                50: 'Leyenda',
                100: 'Arcade God'
            }
            for nivel_req, insignia in sorted(insignias.items()):
                if self.nivel >= nivel_req:
                    self.insignia = insignia
        self.save()
    
    def actualizar_racha(self):
        from datetime import date
        hoy = date.today()
        if self.ultima_jugada == hoy:
            return  # Ya jugó hoy
        elif self.ultima_jugada == date.fromordinal(hoy.toordinal() - 1):
            self.racha_dias += 1
        else:
            self.racha_dias = 1
        self.ultima_jugada = hoy
        self.save()
