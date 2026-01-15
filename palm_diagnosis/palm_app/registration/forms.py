from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "auth-input",
            "placeholder": "اسم المستخدم",
            "autocomplete": "off"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "auth-input",
            "placeholder": "كلمة المرور",
            "autocomplete": "current-password"
        })
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "auth-input",
            "placeholder": "اسم المستخدم",
            "autocomplete": "off"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "auth-input",
            "placeholder": "البريد الإلكتروني",
            "autocomplete": "off"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "auth-input",
            "placeholder": "كلمة المرور",
            "autocomplete": "new-password"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "auth-input",
            "placeholder": "تأكيد كلمة المرور",
            "autocomplete": "new-password"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
