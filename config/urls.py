from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
from pathlib import Path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication and Notifications
    path('accounts/', include('allauth.urls')),
    # path('webpush/', include('webpush.urls')), # Temporalmente deshabilitado - incompatible con Django 6.0

    path('send-test-notification/', views.send_test_notification, name='send_test_notification'),
    
    # PWA Manifest
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest'),
    
    # API routes
    path('api/', include('apps.api.urls')),
    
    # MongoDB Analytics - Temporalmente deshabilitado
    # path('mongodb/', include('mongodb.urls')),
    
    # Blog
    path('blog/', include('apps.blog.urls')),
    
    # Clima
    path('clima/', include('apps.clima.urls')),
    
    # Traductor
    path('traductor/', include('apps.traductor.urls')),
    
    # Eventos
    path('eventos/', include('apps.eventos.urls')),
    
    # Tutorial
    path('tutorial/', include('apps.tutorial.urls')),
    
    # Estudio
    path('estudio/', include('apps.estudio.urls')),
    
    # Main Application
    path('', include('apps.app.urls')),
]

# Serve PWA files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)