
from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.blog_fragment, name='blog_fragment'),
    path('personal/', views.personal_blog, name='personal_blog'),
    path('admin/', views.admin_blog, name='admin_blog'),
    path('create/', views.create_post, name='create_post'),
]

