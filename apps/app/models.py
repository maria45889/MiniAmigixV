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

class Category(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    icono = models.CharField(max_length=50, default='📁')
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class PublicacionBlog(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.CharField(max_length=50, choices=[
        ('noticias', '📰 Noticias'),
        ('consejos', '💡 Consejos'),
        ('tutorial', '🎯 Tutorial'),
        ('personal', '📝 Personal'),
        ('anuncios', '🚀 Anuncios'),
        ('mantenimiento', '⚙️ Mantenimiento'),
        ('actualizaciones', '🔄 Actualizaciones'),
        ('avisos_urgentes', '⚠️ Avisos Urgentes'),
    ], default='personal')
    categoria_dinamica = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='publicaciones')
    es_oficial = models.BooleanField(default=False)
    fijado = models.BooleanField(default=False)
    visible_para_todos = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        ordering = ['-fijado', '-fecha_publicacion']
        verbose_name = 'Publicación de Blog'
        verbose_name_plural = 'Publicaciones de Blog'

class Comment(models.Model):
    publicacion = models.ForeignKey(PublicacionBlog, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.publicacion.titulo}"

    class Meta:
        ordering = ['fecha_creacion']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

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
