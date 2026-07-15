"""
Calendar views.
"""

from django.shortcuts import redirect


def eventos(request):
    """Redirect to events list."""
    return redirect('lista_eventos')
