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
    fecha_agregada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.artista or 'Desconocido'}"

    class Meta:
        ordering = ['-fecha_agregada']

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
    ], default='personal')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = 'Publicación de Blog'
        verbose_name_plural = 'Publicaciones de Blog'
