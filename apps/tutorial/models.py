from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """Categorías para organizar tutoriales"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icono de FontAwesome")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Tutorial(models.Model):
    """Tutoriales principales"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tutorials')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    image = models.ImageField(upload_to='tutorials/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="URL de video YouTube o Vimeo")
    estimated_time = models.IntegerField(help_text="Tiempo estimado en minutos")
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, help_text="Tutorial destacado")
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def total_steps(self):
        return self.steps.count()
    
    @property
    def average_rating(self):
        ratings = self.progress.filter(completed=True).values_list('rating', flat=True)
        if ratings:
            return sum(ratings) / len(ratings)
        return 0


class Step(models.Model):
    """Pasos individuales de un tutorial"""
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='steps')
    order = models.IntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='tutorial_steps/', blank=True, null=True)
    code_example = models.TextField(blank=True, help_text="Código de ejemplo si aplica")
    code_language = models.CharField(max_length=50, blank=True, help_text="Ej: python, javascript, html")
    is_optional = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
        unique_together = ['tutorial', 'order']
    
    def __str__(self):
        return f"{self.order}. {self.title} - {self.tutorial.title}"


class TutorialProgress(models.Model):
    """Progreso de usuarios en tutoriales"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutorial_progress')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='progress')
    current_step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, help_text="Calificación 1-5")
    notes = models.TextField(blank=True, help_text="Notas personales del usuario")
    last_accessed = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'tutorial']
        verbose_name_plural = "Progreso de Tutoriales"
    
    def __str__(self):
        return f"{self.user.username} - {self.tutorial.title}"
    
    @property
    def progress_percentage(self):
        if self.completed:
            return 100
        total_steps = self.tutorial.total_steps
        if total_steps == 0:
            return 0
        if self.current_step:
            completed_steps = Step.objects.filter(
                tutorial=self.tutorial, 
                order__lte=self.current_step.order
            ).count()
            return int((completed_steps / total_steps) * 100)
        return 0


class FAQ(models.Model):
    """Preguntas frecuentes"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='faqs', null=True, blank=True)
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ['order', '-helpful_count']
    
    def __str__(self):
        return self.question
