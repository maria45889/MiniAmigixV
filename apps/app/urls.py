from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('chat/', views.chat, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('musica/', views.musica, name='musica'),
    path('juegos/', views.juegos, name='juegos'),
    path('estudio/', views.estudio, name='estudio'),
    path('clima/', views.clima, name='clima'),
    path('traductor/', views.traductor, name='traductor'),
    path('entretenimiento/', views.entretenimiento, name='entretenimiento'),
    path('blog/', views.blog, name='blog'),
    path('logout/', views.logout_view, name='logout'),
]
