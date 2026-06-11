from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_sugerencias, name='lista_sugerencias'),
    path('crear/', views.crear_sugerencia, name='crear_sugerencia'),
]
