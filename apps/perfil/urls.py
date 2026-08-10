from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_perfil, name='perfil'),
    path('editar/', views.editar_perfil, name='editar_perfil'),
    path('api/cambiar-tema/', views.cambiar_tema, name='cambiar_tema'),
]
