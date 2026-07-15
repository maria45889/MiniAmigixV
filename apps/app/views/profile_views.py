"""
Profile views.
"""

from django.shortcuts import redirect


def perfil(request):
    """Redirect to profile."""
    return redirect('perfil')


def configuracion(request):
    """Redirect to configuration."""
    return redirect('configuracion_view')
