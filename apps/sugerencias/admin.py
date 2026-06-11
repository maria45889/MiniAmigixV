from django.contrib import admin
from .models import Sugerencia

@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'categoria', 'estado', 'fecha_creacion']
    list_filter = ['categoria', 'estado', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'usuario__username']
