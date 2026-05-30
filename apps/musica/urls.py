from django.urls import path
from . import views

urlpatterns = [
    path('music/lyrics/', views.obtener_letra, name='obtener_lyric'),
]
