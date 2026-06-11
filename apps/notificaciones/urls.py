from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_notificaciones, name='lista_notificaciones'),
    path('marcar-leidas/', views.marcar_leidas, name='marcar_leidas'),
]
