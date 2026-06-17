from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication and Notifications
    path('accounts/', include('allauth.urls')),
    path('webpush/', include('webpush.urls')),

    path('send-test-notification/', views.send_test_notification, name='send_test_notification'),
    
    # PWA Manifest
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest'),
    
    # Main Application
    path('', include('app.urls')),
]

# Serve PWA files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)