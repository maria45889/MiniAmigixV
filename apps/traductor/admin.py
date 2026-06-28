from django.contrib import admin
from .models import TranslationCache

@admin.register(TranslationCache)
class TranslationCacheAdmin(admin.ModelAdmin):
    list_display = ['texto_original', 'idioma_origen', 'idioma_destino', 'fecha_consulta', 'fecha_expiracion']
    list_filter = ['idioma_origen', 'idioma_destino', 'fecha_consulta']
    search_fields = ['texto_original', 'texto_traducido']
    readonly_fields = ['fecha_consulta', 'fecha_expiracion']
