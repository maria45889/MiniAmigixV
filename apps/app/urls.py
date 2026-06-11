from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('chat/', views.chat, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('musica/', views.musica, name='musica'),
    path('api/add-song/', views.add_song_api, name='add_song_api'),
    path('api/delete-song/<int:song_id>/', views.delete_song_api, name='delete_song_api'),
    path('juegos/', views.juegos, name='juegos'),
    path('estudio/', views.estudio, name='estudio'),
    path('clima/', views.clima, name='clima'),
    path('traductor/', views.traductor, name='traductor'),
    path('entretenimiento/', views.entretenimiento, name='entretenimiento'),
    path('blog/', views.blog, name='blog'),
    path('blog/crear/', views.crear_publicacion, name='crear_publicacion'),
    path('api/delete-publicacion/<int:publicacion_id>/', views.delete_publicacion_api, name='delete_publicacion_api'),
    path('logout/', views.logout_view, name='logout'),
]
