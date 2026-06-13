from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_sugerencias, name='lista_sugerencias'),
    path('crear/', views.crear_sugerencia, name='crear_sugerencia'),
    path('admin/', views.admin_sugerencias, name='admin_sugerencias'),
    path('admin/responder/<int:sugerencia_id>/', views.responder_sugerencia, name='responder_sugerencia'),
]
