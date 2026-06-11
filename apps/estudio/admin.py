from django.contrib import admin
from .models import Nota, Resumen

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ['contenido', 'usuario', 'fecha_creacion', 'fecha_actualizacion']
    list_filter = ['fecha_creacion', 'usuario']
    search_fields = ['contenido']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

@admin.register(Resumen)
class ResumenAdmin(admin.ModelAdmin):
    list_display = ['texto_original', 'resumen', 'usuario', 'fecha_creacion']
    list_filter = ['fecha_creacion', 'usuario']
    search_fields = ['texto_original', 'resumen']
    readonly_fields = ['fecha_creacion']
