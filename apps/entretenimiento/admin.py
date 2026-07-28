from django.contrib import admin
from .models import CategoriaEntretenimiento, ContenidoEntretenimiento, FavoritoEntretenimiento, RecomendacionIA


@admin.register(CategoriaEntretenimiento)
class CategoriaEntretenimientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'orden']
    list_editable = ['icono', 'orden']
    search_fields = ['nombre']


@admin.register(ContenidoEntretenimiento)
class ContenidoEntretenimientoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'genero', 'calificacion', 'es_destacado', 'anio']
    list_filter = ['tipo', 'categoria', 'es_destacado', 'genero']
    list_editable = ['calificacion', 'es_destacado']
    search_fields = ['titulo', 'director', 'genero']
    ordering = ['-es_destacado', '-calificacion']


@admin.register(FavoritoEntretenimiento)
class FavoritoEntretenimientoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'contenido', 'fecha_agregado']
    list_filter = ['fecha_agregado']
    search_fields = ['usuario__username', 'contenido__titulo']


@admin.register(RecomendacionIA)
class RecomendacionIAAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'contenido', 'fecha_recomendacion', 'vista']
    list_filter = ['vista', 'fecha_recomendacion']
    search_fields = ['usuario__username', 'contenido__titulo']
