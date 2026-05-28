from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q


class CustomPasswordResetForm(PasswordResetForm):
    identifier = forms.CharField(
        label='Correo electrónico o apodo',
        max_length=254,
        widget=forms.TextInput(attrs={'autocomplete': 'email', 'placeholder': 'Correo electrónico o apodo'})
    )

    def clean_identifier(self):
        return self.cleaned_data.get('identifier', '').strip()

    def get_users(self, identifier):
        if not identifier:
            return self.user_cache

        UserModel = get_user_model()
        query = Q(email__iexact=identifier) | Q(username__iexact=identifier)
        return UserModel._default_manager.filter(query, is_active=True)

    def save(self, *args, **kwargs):
        self.cleaned_data['email'] = self.cleaned_data.get('identifier')
        return super().save(*args, **kwargs)
