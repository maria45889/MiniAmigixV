from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views

# ============================================================================
# URL PATTERNS
# ============================================================================

urlpatterns = [
    # -------------------------------------------------------------------------
    # Core Django
    # -------------------------------------------------------------------------
    path('admin/', admin.site.urls),

    # -------------------------------------------------------------------------
    # Authentication & Notifications
    # -------------------------------------------------------------------------
    path('accounts/', include('allauth.urls')),
    path('send-test-notification/', views.send_test_notification, name='send_test_notification'),
    # path('webpush/', include('webpush.urls')),  # Temporalmente deshabilitado - incompatible con Django 6.0

    # -------------------------------------------------------------------------
    # PWA
    # -------------------------------------------------------------------------
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest'),

    # -------------------------------------------------------------------------
    # API Routes
    # -------------------------------------------------------------------------
    path('api/', include('apps.api.urls')),
    path('api/music/', include('apps.musica.urls')),
    path('api/games/', include('apps.juegos.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # -------------------------------------------------------------------------
    # Feature Apps (Alphabetical Order)
    # -------------------------------------------------------------------------
    path('blog/', include('apps.blog.urls')),
    path('clima/', include('apps.clima.urls')),
    path('entretenimiento/', include('apps.entretenimiento.urls')),
    path('estudio/', include('apps.estudio.urls')),
    path('eventos/', include('apps.eventos.urls')),
    path('traductor/', include('apps.traductor.urls')),
    path('tutorial/', include('apps.tutorial.urls')),

    # -------------------------------------------------------------------------
    # Main Application
    # -------------------------------------------------------------------------
    path('', include('apps.app.urls')),
]

# Temporalmente deshabilitado
# path('mongodb/', include('mongodb.urls')),

# ============================================================================
# DEVELOPMENT ONLY
# ============================================================================

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)