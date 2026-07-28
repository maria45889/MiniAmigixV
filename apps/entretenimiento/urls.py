from django.urls import path
from . import views

app_name = 'entretenimiento'

urlpatterns = [
    path('', views.entretenimiento_view, name='entretenimiento'),
    path('toggle-favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('recomendacion-ia/', views.obtener_recomendacion_ia, name='recomendacion_ia'),
    path('buscar/', views.buscar_contenido, name='buscar_contenido'),
    path('favoritos/', views.listar_favoritos, name='listar_favoritos'),
]
