from django.contrib import admin
from .models import Category, Tutorial, Step, TutorialProgress, FAQ


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['name', 'description']
    prepopulated_fields = {}


class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    fields = ['order', 'title', 'content', 'is_optional']
    ordering = ['order']


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'is_active', 'featured', 'views', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active', 'featured', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'featured']
    inlines = [StepInline]
    readonly_fields = ['views', 'created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'description', 'category', 'difficulty')
        }),
        ('Multimedia', {
            'fields': ('image', 'video_url')
        }),
        ('Configuración', {
            'fields': ('estimated_time', 'is_active', 'featured')
        }),
        ('Estadísticas', {
            'fields': ('views', 'created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['tutorial', 'order', 'title', 'is_optional']
    list_filter = ['tutorial', 'is_optional']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_optional']


@admin.register(TutorialProgress)
class TutorialProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'tutorial', 'current_step', 'completed', 'progress_percentage', 'rating', 'last_accessed']
    list_filter = ['completed', 'tutorial__category', 'rating']
    search_fields = ['user__username', 'tutorial__title']
    readonly_fields = ['progress_percentage', 'started_at', 'last_accessed']
    
    def progress_percentage(self, obj):
        return f"{obj.progress_percentage}%"
    progress_percentage.short_description = 'Progreso'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'helpful_count', 'not_helpful_count', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order']
