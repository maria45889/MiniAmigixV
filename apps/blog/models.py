from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    icono = models.CharField(max_length=50, default='📁')
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    class Meta:
        app_label = 'blog'
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Post(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='blog_images/', null=True, blank=True)
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
    categoria_dinamica = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    es_oficial = models.BooleanField(default=False)
    fijado = models.BooleanField(default=False)
    visible_para_todos = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    class Meta:
        app_label = 'blog'
        ordering = ['-fijado', '-fecha_publicacion']
        verbose_name = 'Publicación de Blog'
        verbose_name_plural = 'Publicaciones de Blog'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.post.titulo}"

    class Meta:
        app_label = 'blog'
        ordering = ['fecha_creacion']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
