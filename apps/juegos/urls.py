from django.urls import path

from . import views

urlpatterns = [
    path('', views.arena_zen_fragment, name='juegos-index'),
]


