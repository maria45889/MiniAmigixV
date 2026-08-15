"""
Authentication views.
"""

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
    
    # Get social providers
    site = AuthSelector.get_current_site()
    providers = AuthSelector.get_google_social_apps(site)
    
    return render(request, 'login.html', {
        'form': form,
        'providers': providers
    })


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration."""
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
                    'email': request.POST.get('email', '')
                })
    else:
        form = RegisterForm()
    
    # Get social providers
    site = AuthSelector.get_current_site()
    providers = AuthSelector.get_google_social_apps(site)
    
    return render(request, 'register.html', {
        'form': form,
        'providers': providers
    })


@require_http_methods(["POST", "GET"])
def logout_view(request):
    """Handle user logout."""
    AuthService.logout_user(request)
    return redirect('login')
