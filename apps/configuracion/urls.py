from django.urls import path
from . import views

urlpatterns = [
    path('', views.configuracion_view, name='configuracion_view'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
]
