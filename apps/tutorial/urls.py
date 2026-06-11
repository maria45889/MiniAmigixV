from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial_home, name='tutorial_home'),
]
