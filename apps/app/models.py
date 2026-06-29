from django.db import models
from django.contrib.auth.models import User

class ConversacionChat(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, default='Nueva conversación')
    emocion_dominante = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        ordering = ['-fecha_actualizacion']

class MensajeChat(models.Model):
    conversacion = models.ForeignKey(ConversacionChat, on_delete=models.CASCADE, related_name='mensajes')
    es_usuario = models.BooleanField(default=True)
    texto = models.TextField()
    imagen = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    emocion_detectada = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Usuario' if self.es_usuario else 'IA'}: {self.texto[:50]}"

    class Meta:
        ordering = ['fecha_creacion']

class EstadoAnimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    emocion = models.CharField(max_length=50, choices=[
        ('feliz', 'Feliz 😊'),
        ('triste', 'Triste 😢'),
        ('ansioso', 'Ansioso 😰'),
        ('enfadado', 'Enfadado 😠'),
        ('calmado', 'Calmado 😌'),
        ('motivado', 'Motivado 💪'),
        ('cansado', 'Cansado 😴'),
        ('confundido', 'Confundido 😕'),
    ])
    intensidad = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], default=5)
    notas = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.emocion} ({self.intensidad}/10)"

    class Meta:
        ordering = ['-fecha_registro']

class RecomendacionEntretenimiento(models.Model):
    categoria = models.CharField(max_length=50, choices=[
        ('peliculas', 'Películas'),
        ('series', 'Series'),
        ('libros', 'Libros'),
        ('teatro', 'Teatro'),
    ])
    datos = models.JSONField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recomendaciones {self.categoria} - {self.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Recomendación de Entretenimiento"
        verbose_name_plural = "Recomendaciones de Entretenimiento"

class Cancion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    artista = models.CharField(max_length=200, blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    youtube_id = models.CharField(max_length=50, blank=True, null=True)
    audio_file = models.FileField(upload_to='music/', blank=True, null=True)
    letra = models.TextField(blank=True, null=True)
    letra_sincronizada = models.TextField(blank=True, null=True)
    fecha_agregada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.artista or 'Desconocido'}"

    class Meta:
        ordering = ['-fecha_agregada']

class Playlist(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    canciones = models.ManyToManyField(Cancion, related_name='playlists')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    es_publica = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"

    class Meta:
        ordering = ['-fecha_actualizacion']

class Favorite(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name='favoritos')
    fecha_agregada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.cancion.nombre}"

    class Meta:
        ordering = ['-fecha_agregada']
        unique_together = ['usuario', 'cancion']


class Game(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ('quiz', 'Quiz'),
        ('memoria', 'Memoria'),
        ('matematicas', 'Matemáticas'),
        ('palabras', 'Palabras'),
        ('logica', 'Lógica'),
    ], default='quiz')
    dificultad = models.CharField(max_length=20, choices=[
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
    ], default='medio')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'

class Score(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    juego = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='puntuaciones')
    puntuacion = models.IntegerField(default=0)
    fecha_juego = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.juego.nombre}: {self.puntuacion}"

    class Meta:
        ordering = ['-puntuacion']
        verbose_name = 'Puntuación'
        verbose_name_plural = 'Puntuaciones'

class Achievement(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='🏆')
    puntos_requeridos = models.IntegerField(default=100)
    juego = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='logros', null=True, blank=True)

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'

class UserAchievement(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    logro = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    fecha_desbloqueado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.logro.nombre}"

    class Meta:
        ordering = ['-fecha_desbloqueado']
        verbose_name = 'Logro de Usuario'
        verbose_name_plural = 'Logros de Usuarios'
