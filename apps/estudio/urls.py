from django.urls import path
from . import views

urlpatterns = [
    path('', views.estudio, name='estudio'),
    path('api/guardar-nota/', views.guardar_nota, name='guardar_nota'),
    path('api/eliminar-nota/<uuid:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('api/resumir-texto/', views.resumir_texto, name='resumir_texto'),
    path('api/obtener-notas/', views.obtener_notas, name='obtener_notas'),
    path('api/obtener-resumenes/', views.obtener_resumenes, name='obtener_resumenes'),
    path('api/eliminar-resumen/<uuid:resumen_id>/', views.eliminar_resumen, name='eliminar_resumen'),
]
