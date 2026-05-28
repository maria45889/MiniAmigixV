from django.db import models
from django.utils import timezone

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('admin', 'Admin'),
    ]
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50)
    contenido = models.TextField()
    autor = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    lectura_min = models.PositiveIntegerField(default=1)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='personal')
    
    class Meta:
        ordering = ['-fecha']  # Most recent first
    
    def __str__(self):
        return self.titulo
