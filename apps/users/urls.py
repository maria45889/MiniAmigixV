from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from .views import login_view, register_view, home_view, profile_view, update_profile, logout_view, google_auth_view, support_view, admin_support_view, crear_sugerencia, panel_dashboard, bandeja_sugerencias, bandeja_soporte, responder_sugerencia, responder_soporte, notificaciones_view, clima_api_view, traductor_translate

from django.views.generic import TemplateView

from django.shortcuts import redirect

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('registro/', register_view, name='registro'),
    path('register/', register_view, name='register'),
    path('auth/google/', google_auth_view, name='google_auth'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        form_class=CustomPasswordResetForm,
        email_template_name='users/password_reset_email.html',
        html_email_template_name='users/password_reset_email_html.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('home/', home_view, name='home'),
    path('musica/', TemplateView.as_view(template_name='musica/index.html'), name='musica'),
    path('api/clima/', clima_api_view, name='api_clima'),
    path('clima/', TemplateView.as_view(template_name='clima/index.html'), name='clima'),
    path('eventos/', TemplateView.as_view(template_name='eventos/index.html'), name='eventos'),
    path('estudios/', TemplateView.as_view(template_name='estudios/index.html'), name='estudios'),
    path('entretenimiento/', TemplateView.as_view(template_name='entretenimiento/index.html'), name='entretenimiento'),
    # Antiestrés / Juegos
    path('antistres/', TemplateView.as_view(template_name='antistres/index.html'), name='antistres'),
    path('juegos/', TemplateView.as_view(template_name='juegos/index.html'), name='juegos'),
    path('juegos/arena-zen/', TemplateView.as_view(template_name='juegos/arena-zen.html'), name='juegos_arena_zen'),
    path('juegos/adivinar/', TemplateView.as_view(template_name='juegos/adivinar.html'), name='juegos_adivinar'),
   
    path('notificaciones/', notificaciones_view, name='notificaciones'),
    path('sugerencias/', TemplateView.as_view(template_name='sugerencias/index.html'), name='sugerencias'),
    path('sugerencias/crear/', crear_sugerencia, name='crear_sugerencia'),
   
    path('soporte/', support_view, name='soporte'),
    path('admin-soporte/', admin_support_view, name='admin_soporte'),
    path('panel/', panel_dashboard, name='panel_dashboard'),
    path('panel/sugerencias/', bandeja_sugerencias, name='bandeja_sugerencias'),
    path('panel/soporte/', bandeja_soporte, name='bandeja_soporte'),
    path('panel/sugerencias/<int:sugerencia_id>/responder/', responder_sugerencia, name='responder_sugerencia'),
    path('panel/soporte/<int:ticket_id>/responder/', responder_soporte, name='responder_soporte'),
    path('traductor/', TemplateView.as_view(template_name='traductor/index.html'), name='traductor'),
    path('traductor/translate/', traductor_translate, name='traductor_translate'),
    path('tutorial/', TemplateView.as_view(template_name='tutorial/index.html'), name='tutorial'),
    path('configuraciones/', TemplateView.as_view(template_name='configuraciones/index.html'), name='configuraciones'),
    path('perfil/', profile_view, name='perfil'),
    path('actualizar-perfil/', update_profile, name='actualizar_perfil'),
    path('logout/', logout_view, name='logout'),
]









