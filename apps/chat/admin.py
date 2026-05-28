from django.contrib import admin

from .models import Marca, Vehiculo


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ["marca", "modelo", "anio", "placa", "color", "creado_en"]
    list_filter = ["marca", "anio"]
    search_fields = ["modelo", "placa", "color", "marca__nombre"]
