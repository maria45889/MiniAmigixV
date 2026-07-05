from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_notificaciones, name='lista_notificaciones'),
    path('marcar-leidas/', views.marcar_leidas, name='marcar_leidas'),
    path('eliminar/', views.eliminar_notificacion, name='eliminar_notificacion'),
    path('fijar/', views.fijar_notificacion, name='fijar_notificacion'),
    path('buscar/', views.buscar_notificaciones, name='buscar_notificaciones'),
]
