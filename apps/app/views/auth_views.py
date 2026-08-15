"""
Authentication views.
"""

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from apps.app.services import AuthService
from apps.app.selectors import AuthSelector
from apps.app.forms import LoginForm, RegisterForm
from apps.app.constants.messages import ERROR_MESSAGES, SUCCESS_MESSAGES


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            success, error = AuthService.login_user(request, username, password)
            if success:
                return redirect('home')
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': error
                })
    else:
        form = LoginForm()
    
    google_auth_enabled = bool(getattr(settings, 'GOOGLE_CLIENT_ID', '') and getattr(settings, 'GOOGLE_CLIENT_SECRET', ''))
    
    return render(request, 'login.html', {
        'form': form,
        'google_auth_enabled': google_auth_enabled
    })


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration."""
    google_auth_enabled = bool(getattr(settings, 'GOOGLE_CLIENT_ID', '') and getattr(settings, 'GOOGLE_CLIENT_SECRET', ''))
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password_confirm = form.cleaned_data['password2']
            
            user, error = AuthService.register_user(username, email, password, password_confirm)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                # Preserve form data on error (only clear password fields)
                return render(request, 'register.html', {
                    'form': form,
                    'error': error,
                    'username': request.POST.get('username', ''),
                    'email': request.POST.get('email', ''),
                    'google_auth_enabled': google_auth_enabled
                })
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {
        'form': form,
        'google_auth_enabled': google_auth_enabled
    })


@require_http_methods(["POST", "GET"])
def logout_view(request):
    """Handle user logout."""
    AuthService.logout_user(request)
    return redirect('login')
