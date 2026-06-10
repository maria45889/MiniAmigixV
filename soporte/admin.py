from django.contrib import admin
from .models import TicketSoporte

@admin.register(TicketSoporte)
class TicketSoporteAdmin(admin.ModelAdmin):
    list_display = ['asunto', 'usuario', 'prioridad', 'estado', 'fecha_creacion']
    list_filter = ['prioridad', 'estado', 'fecha_creacion']
    search_fields = ['asunto', 'descripcion', 'usuario__username']
