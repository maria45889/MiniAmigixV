from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)
    display_name = models.CharField(max_length=100, blank=True)  # Nombre del perfil
    ai_name = models.CharField(max_length=50, default='Asistente IA')  # Nombre de la IA
    profile_background = models.CharField(max_length=200, default='default')  # Fondo del perfil
    app_background = models.CharField(max_length=200, default='default')  # Fondo general de la aplicación
    screen_appearance = models.CharField(max_length=50, default='standard')  # Apariencia de la pantalla
    font_size = models.CharField(max_length=20, default='medium')  # Tamaño de fuente preferido
    theme_preference = models.CharField(max_length=20, default='dark')  # Tema preferido (dark/light)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        # Create profile if it doesn't exist when user is saved
        super().save(*args, **kwargs)


class Sugerencia(models.Model):
    TIPO_CHOICES = [
        ('idea', 'Idea'),
        ('mejora', 'Mejora'),
        ('reporte', 'Reporte de Error'),
        ('pregunta', 'Pregunta'),
        ('elogio', 'Elogio'),
        ('otro', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('respuesta', 'Respondida'),
        ('resuelta', 'Resuelta'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sugerencias')
    titulo = models.CharField(max_length=180)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='idea')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    respuesta = models.TextField(blank=True)
    respondido_en = models.DateTimeField(null=True, blank=True)
    respondido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sugerencias_respuestas')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Sugerencia #{self.id} - {self.titulo}'


class SupportTicket(models.Model):

    TIPO_CHOICES = [
        ('ayuda', 'Ayuda'),
        ('consulta', 'Consulta'),
        ('sugerencia', 'Sugerencia'),
        ('problema', 'Problema Técnico'),
        ('solicitud', 'Solicitud de Funcionalidad'),
        ('reporte', 'Reporte de Error'),
        ('informacion', 'Solicitud de Información'),
    ]
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_revision', 'En Revisión'),
        ('resuelto', 'Resuelto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    title = models.CharField(max_length=180)
    description = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='consulta')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='media')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    respuesta = models.TextField(blank=True)
    respondido_en = models.DateTimeField(null=True, blank=True)
    respondido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_responses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Support ticket #{self.id} - {self.title}'
