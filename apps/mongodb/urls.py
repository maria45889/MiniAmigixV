from django.urls import path
from . import views

urlpatterns = [
    path('dashboard-analitica/', views.dashboard_analitica, name='dashboard_analitica'),
]
