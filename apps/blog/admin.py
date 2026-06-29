from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_creacion']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'categoria', 'fecha_publicacion', 'publicado', 'fijado']
    list_filter = ['categoria', 'fecha_publicacion', 'publicado', 'fijado', 'es_oficial']
    search_fields = ['titulo', 'contenido']
    readonly_fields = ['fecha_publicacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_publicacion'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'usuario', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['contenido']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
