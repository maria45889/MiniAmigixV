from django.conf import settings
from django.http import HttpResponseForbidden
import re


class SecurityHeadersMiddleware:
    """
    Middleware para agregar headers de seguridad adicionales
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy básico
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com https://www.google.com https://www.youtube.com https://www.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            "img-src 'self' data: blob: https:; "
            "media-src 'self' blob: https://*.googlevideo.com https://*.youtube.com; "
            "connect-src 'self' http://127.0.0.1:8000 http://localhost:8000 https://api.openai.com https://www.googleapis.com https://*.openweathermap.org https://unpkg.com https://cdn.jsdelivr.net https://lrclib.net https://*.googlevideo.com https://www.youtube.com https://youtubei.googleapis.com; "
            "frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://www.google.com https://accounts.google.com; "
            "frame-ancestors 'self';"
        )
        
        # X-Content-Type-Options
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options (si no está configurado en settings)
        if not hasattr(settings, 'X_FRAME_OPTIONS'):
            response['X-Frame-Options'] = 'DENY'
        
        # Referrer-Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy
        response['Permissions-Policy'] = (
            'microphone=(self), camera=(self), '
            'payment=(), usb=(), magnetometer=(), gyroscope=()'
        )
        
        return response


class IPWhitelistMiddleware:
    """
    Middleware para restringir acceso a IPs específicas (opcional para admin)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = getattr(settings, 'ALLOWED_ADMIN_IPS', [])

    def __call__(self, request):
        # Solo aplicar a rutas de admin
        if request.path.startswith('/admin/'):
            ip = self.get_client_ip(request)
            if self.allowed_ips and ip not in self.allowed_ips:
                return HttpResponseForbidden("Acceso denegado")
        return self.get_response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class XSSProtectionMiddleware:
    """
    Middleware para protección adicional contra XSS
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Sanitizar headers potencialmente peligrosos
        dangerous_headers = ['HTTP_X_FORWARDED_FOR', 'HTTP_USER_AGENT']
        for header in dangerous_headers:
            if header in request.META:
                request.META[header] = self.sanitize_input(request.META[header])
        
        return response

    def sanitize_input(self, value):
        """Sanitiza input para prevenir XSS"""
        if isinstance(value, str):
            # Eliminar etiquetas HTML y scripts
            value = re.sub(r'<script.*?>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
            value = re.sub(r'<.*?>', '', value)
        return value
