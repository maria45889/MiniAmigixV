from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tema', 'idioma']
    list_filter = ['tema', 'idioma']
    search_fields = ['usuario__username', 'bio']
