from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Account

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label="Prénom")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label="Nom")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input'}), label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), label="Confirmer le mot de passe")

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas")

        return cleaned_data

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data['password1'])
        if commit:
            account.save()
        return account

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), label="Mot de passe")

    class Meta:
        model = Account
        fields = ['username', 'password']

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("Ce compte est désactivé.")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
