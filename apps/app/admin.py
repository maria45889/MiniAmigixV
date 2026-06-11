from django.contrib import admin
from .models import PublicacionBlog

@admin.register(PublicacionBlog)
class PublicacionBlogAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'categoria', 'fecha_publicacion', 'publicado']
    list_filter = ['categoria', 'fecha_publicacion', 'publicado']
    search_fields = ['titulo', 'contenido']
    readonly_fields = ['fecha_publicacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_publicacion'
