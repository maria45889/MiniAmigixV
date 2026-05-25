
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('animos/', views.animos_del_dia, name='animo_del_dia'),

    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('api/admin-stats/', views.api_admin_stats, name='api_admin_stats'),
]