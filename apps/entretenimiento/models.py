from django.db import models
from django.contrib.auth.models import User


class CategoriaEntretenimiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    icono = models.CharField(max_length=50, default='🎬')
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Categoría de Entretenimiento'
        verbose_name_plural = 'Categorías de Entretenimiento'
    
    def __str__(self):
        return f"{self.icono} {self.nombre}"


class ContenidoEntretenimiento(models.Model):
    TIPO_CHOICES = [
        ('pelicula', 'Película'),
        ('serie', 'Serie'),
        ('anime', 'Anime'),
        ('libro', 'Libro'),
        ('manga', 'Manga'),
        ('musica', 'Música'),
        ('podcast', 'Podcast'),
        ('documental', 'Documental'),
        ('teatro', 'Teatro'),
        ('radio', 'Radio'),
        ('meme', 'Meme'),
        ('fondo', 'Fondo de Pantalla'),
        ('curiosidad', 'Curiosidad'),
        ('juego', 'Juego Recomendado'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    genero = models.CharField(max_length=100, blank=True)
    imagen = models.URLField(blank=True, help_text='URL de la imagen del póster/portada')
    trailer = models.URLField(blank=True, help_text='URL del tráiler en YouTube')
    anio = models.IntegerField(null=True, blank=True, help_text='Año de lanzamiento')
    duracion = models.CharField(max_length=50, blank=True, help_text='Duración o extensión')
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text='Calificación de 0 a 10')
    director = models.CharField(max_length=255, blank=True, help_text='Director, autor o creador')
    plataforma = models.CharField(max_length=100, blank=True, help_text='Plataforma donde ver/escuchar')
    categoria = models.ForeignKey(CategoriaEntretenimiento, on_delete=models.SET_NULL, null=True, blank=True)
    es_destacado = models.BooleanField(default=False, help_text='Marcar como recomendación del día')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-es_destacado', '-calificacion', '-fecha_creacion']
        verbose_name = 'Contenido de Entretenimiento'
        verbose_name_plural = 'Contenidos de Entretenimiento'
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"


class FavoritoEntretenimiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.ForeignKey(ContenidoEntretenimiento, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'contenido']
        ordering = ['-fecha_agregado']
        verbose_name = 'Favorito de Entretenimiento'
        verbose_name_plural = 'Favoritos de Entretenimiento'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.contenido.titulo}"


class RecomendacionIA(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.ForeignKey(ContenidoEntretenimiento, on_delete=models.CASCADE)
    razon = models.TextField(help_text='Razón de la recomendación por IA')
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    vista = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_recomendacion']
        verbose_name = 'Recomendación IA'
        verbose_name_plural = 'Recomendaciones IA'
    
    def __str__(self):
        return f"IA recomendó {self.contenido.titulo} a {self.usuario.username}"
