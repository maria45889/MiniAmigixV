from django.conf import settings
from django.shortcuts import redirect


def is_admin_owner(request):
    """Devuelve True si el request.user es TU admin (propietaria del panel)."""
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False

    # Solo para tu cuenta. Ajustable por settings.ADMIN_USERNAME.
    admin_username = getattr(settings, "ADMIN_USERNAME", None)
    if admin_username is None:
        return False

    return user.username.startswith(admin_username)


def admin_owner_required(view_func):
    """Decorador simple para redirigir al soporte si no es TU usuario."""
    def _wrapped_view(request, *args, **kwargs):
        if not is_admin_owner(request):
            return redirect('soporte')
        return view_func(request, *args, **kwargs)

    _wrapped_view.__name__ = getattr(view_func, "__name__", "admin_owner_required")
    _wrapped_view.__doc__ = getattr(view_func, "__doc__")
    return _wrapped_view

