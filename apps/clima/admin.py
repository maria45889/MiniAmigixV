from django.contrib import admin
from .models import WeatherCache

@admin.register(WeatherCache)
class WeatherCacheAdmin(admin.ModelAdmin):
    list_display = ['ciudad', 'pais', 'temperatura', 'descripcion', 'fecha_consulta', 'fecha_expiracion']
    list_filter = ['pais', 'fecha_consulta']
    search_fields = ['ciudad', 'descripcion']
    readonly_fields = ['fecha_consulta', 'fecha_expiracion']
