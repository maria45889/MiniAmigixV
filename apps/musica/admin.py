from django.contrib import admin
from .models import Cancion


@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'artista', 'tiene_letra', 'actualizado_en')
    search_fields = ('titulo', 'artista')
    list_filter = ('actualizado_en',)
    readonly_fields = ('creado_en', 'actualizado_en')
