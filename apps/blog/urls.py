from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('comentario/', views.crear_comentario, name='crear_comentario'),
    path('categoria/', views.crear_categoria, name='crear_categoria'),
    path('categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('eliminar-publicacion/<int:post_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('api/delete-publicacion/<int:post_id>/', views.delete_publicacion_api, name='delete_publicacion_api'),
]
