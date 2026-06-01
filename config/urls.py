from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.chat.views import chat_view
from apps.users.auth_views import register_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/register/", register_view, name="register"),
    path("api/", include("apps.chat.urls")),
    path("api/mongo/", include("mongodb_app.urls")),
    path("blog/", include("apps.blog_app.urls")),
    path("", include("apps.musica.urls")),
    path("chat/ia/", chat_view, name="chat"),
    path("oauth/", include("social_django.urls", namespace="social")),
    path(
        "sw.js",
        TemplateView.as_view(
            template_name="sw.js",
            content_type="application/javascript",
        ),
        name="service_worker",
    ),
    path("", RedirectView.as_view(url="/home/", permanent=True)),
    path("", include("apps.users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
