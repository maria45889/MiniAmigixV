from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    tema = models.CharField(max_length=10, choices=[
        ('dark', 'Oscuro'),
        ('light', 'Claro'),
        ('auto', 'Automático'),
    ], default='dark')
    idioma = models.CharField(max_length=10, default='es')
    fecha_nacimiento = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    notificaciones_email = models.BooleanField(default=True)
    notificaciones_push = models.BooleanField(default=False)
    perfil_publico = models.BooleanField(default=True)
    # Accesibilidad
    tamano_fuente = models.CharField(max_length=10, choices=[
        ('small', 'Pequeño'),
        ('normal', 'Normal'),
        ('large', 'Grande'),
    ], default='normal')
    animaciones = models.BooleanField(default=True)
    sonidos = models.BooleanField(default=True)
    # Sesión
    actividad_en_linea = models.BooleanField(default=True)
    # Reloj inteligente
    formato_reloj = models.CharField(max_length=10, choices=[
        ('12h', '12 horas'),
        ('24h', '24 horas'),
    ], default='24h')
    mostrar_segundos = models.BooleanField(default=True)
    mostrar_fecha = models.BooleanField(default=True)
    zona_horaria = models.CharField(max_length=50, default='UTC')
    # Nuevos campos para perfil mejorado
    ubicacion = models.CharField(max_length=100, blank=True, null=True, help_text='Ciudad, País')
    color_acento = models.CharField(max_length=20, choices=[
        ('purple', 'Púrpura'),
        ('blue', 'Azul'),
        ('green', 'Verde'),
        ('orange', 'Naranja'),
        ('red', 'Rojo'),
    ], default='purple')
    # Sistema de niveles y experiencia
    nivel = models.IntegerField(default=1)
    experiencia = models.IntegerField(default=0)
    experiencia_siguiente_nivel = models.IntegerField(default=100)
    
    # Nuevos campos de privacidad
    mostrar_ultima_conexion = models.BooleanField(default=True)
    compartir_estadisticas = models.BooleanField(default=True)
    recomendaciones_ia = models.BooleanField(default=True)
    
    # Nuevos campos de IA
    guardar_historial_ia = models.BooleanField(default=True)
    recordar_preferencias_ia = models.BooleanField(default=True)
    sugerencias_ia = models.BooleanField(default=True)
    aprender_habitos_ia = models.BooleanField(default=True)
    # Nombre personalizado para Amigis
    nombre_amigis = models.CharField(max_length=50, default='Amigis', blank=True, help_text='Nombre personalizado para tu mascota patito')
    
    # Personalización del patito
    patito_ropa = models.CharField(max_length=20, choices=[
        ('hoodie', 'Sudadera'),
        ('shirt', 'Camiseta'),
        ('none', 'Sin ropa'),
    ], default='hoodie', help_text='Tipo de ropa del patito')
    patito_color_ropa = models.CharField(max_length=20, choices=[
        ('purple', 'Morada'),
        ('blue', 'Azul'),
        ('green', 'Verde'),
        ('red', 'Roja'),
        ('black', 'Negra'),
        ('white', 'Blanca'),
    ], default='purple', help_text='Color de la ropa')
    patito_accesorio = models.CharField(max_length=20, choices=[
        ('none', 'Ninguno'),
        ('glasses', 'Gafas'),
        ('hat', 'Gorra'),
        ('bow', 'Lazo'),
    ], default='none', help_text='Accesorio del patito')
    patito_color_cuerpo = models.CharField(max_length=20, choices=[
        ('yellow', 'Amarillo'),
        ('orange', 'Naranja'),
        ('white', 'Blanco'),
        ('pink', 'Rosa'),
    ], default='yellow', help_text='Color del cuerpo del patito')
    patito_estilo = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('neon', 'Neón'),
        ('gradient', 'Gradiente'),
    ], default='normal', help_text='Estilo visual del patito')

    def __str__(self):
        return self.usuario.username

    def agregar_experiencia(self, cantidad):
        """Agrega experiencia y sube de nivel si es necesario"""
        self.experiencia += cantidad
        while self.experiencia >= self.experiencia_siguiente_nivel:
            self.experiencia -= self.experiencia_siguiente_nivel
            self.nivel += 1
            self.experiencia_siguiente_nivel = int(self.experiencia_siguiente_nivel * 1.5)
        self.save()

class UserActivity(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_actividad = models.CharField(max_length=50, choices=[
        ('chat', 'Chat IA'),
        ('musica', 'Música'),
        ('evento', 'Evento'),
        ('juego', 'Juego'),
        ('estudio', 'Estudio'),
        ('traduccion', 'Traducción'),
        ('blog', 'Blog'),
    ])
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_actividad_display()} - {self.fecha}"

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Actividad de Usuario'
        verbose_name_plural = 'Actividades de Usuarios'

class ProfileAchievement(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='🏆')
    puntos_requeridos = models.IntegerField(default=100)
    tipo = models.CharField(max_length=50, choices=[
        ('chat', 'Chat'),
        ('musica', 'Música'),
        ('evento', 'Evento'),
        ('juego', 'Juego'),
        ('estudio', 'Estudio'),
        ('general', 'General'),
    ], default='general')

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Logro de Perfil'
        verbose_name_plural = 'Logros de Perfil'

class UserProfileAchievement(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    logro = models.ForeignKey(ProfileAchievement, on_delete=models.CASCADE)
    fecha_desbloqueado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.logro.nombre}"

    class Meta:
        ordering = ['-fecha_desbloqueado']
        verbose_name = 'Logro Desbloqueado'
        verbose_name_plural = 'Logros Desbloqueados'
        unique_together = ['usuario', 'logro']
