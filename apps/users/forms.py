from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        label='Correo electrónico o apodo',
        max_length=254,
        widget=forms.TextInput(attrs={'autocomplete': 'email', 'placeholder': 'Correo electrónico o apodo', 'class': 'pw-input'})
    )
    
    subject_template_name = 'registration/password_reset_subject.txt'
    email_template_name = 'registration/password_reset_email.html'
    html_email_template_name = 'registration/password_reset_email.html'

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError('Este campo es requerido.')
        return email

    def get_users(self, email):
        if not email:
            return []

        UserModel = get_user_model()
        query = Q(email__iexact=email) | Q(username__iexact=email)
        return UserModel._default_manager.filter(query, is_active=True)
