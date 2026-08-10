from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'perfil', views.UserProfileViewSet, basename='userprofile')
router.register(r'misiones', views.MisionViewSet, basename='mision')
router.register(r'misiones-completadas', views.MisionCompletadaViewSet, basename='misioncompletada')
router.register(r'lecciones-rapidas', views.LeccionRapidaViewSet, basename='leccionrapida')
router.register(r'insignias', views.InsigniaViewSet, basename='insignia')
router.register(r'mis-insignias', views.InsigniaUsuarioViewSet, basename='insigniausuario')
router.register(r'accesorios', views.AccesorioViewSet, basename='accesorio')
router.register(r'mis-accesorios', views.AccesorioUsuarioViewSet, basename='accesoriusuario')

urlpatterns = [
    path('', views.estudio, name='estudio'),
    path('api/guardar-nota/', views.guardar_nota, name='guardar_nota'),
    path('api/eliminar-nota/<uuid:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('api/obtener-notas/', views.obtener_notas, name='obtener_notas'),
    path('api/resumir-texto/', views.resumir_texto, name='resumir_texto'),
    path('api/obtener-resumenes/', views.obtener_resumenes, name='obtener_resumenes'),
    path('api/eliminar-resumen/<uuid:resumen_id>/', views.eliminar_resumen, name='eliminar_resumen'),
    path('api/obtener-estadisticas/', views.obtener_estadisticas, name='obtener_estadisticas'),
    path('api/guardar-sesion-estudio/', views.guardar_sesion_estudio, name='guardar_sesion_estudio'),
    path('api/guardar-pomodoro/', views.guardar_pomodoro, name='guardar_pomodoro'),
    # Nuevos endpoints para el rediseño
    path('api/obtener-metas/', views.obtener_metas, name='obtener_metas'),
    path('api/guardar-meta/', views.guardar_meta, name='guardar_meta'),
    path('api/toggle-meta/<uuid:meta_id>/', views.toggle_meta, name='toggle_meta'),
    path('api/eliminar-meta/<uuid:meta_id>/', views.eliminar_meta, name='eliminar_meta'),
    path('api/obtener-dias-estudiados/', views.obtener_dias_estudiados, name='obtener_dias_estudiados'),
    path('api/', include(router.urls)),
]
