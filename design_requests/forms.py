from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        required=True,
        label="ФИО",
    )
    username = forms.CharField(
        max_length=255,
        required=True,
        label="Логин",
    )
    email = forms.EmailField(required=True)
    privacyConsent = forms.BooleanField(
        required=True,
        label="Согласие на обработку персональных данных",
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'password1', 'password2', 'privacyConsent')

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.fullmatch(r'[А-яёЁ\s\-]+', full_name):
            raise ValidationError("ФИО может состоять только из кириллических букв, пробелов и дефисов")
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.fullmatch(r'[A-z\-]+', username):
            raise ValidationError("Логин может состоять только из латинских букв и дефисов")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Такой логин уже зарегистрирован")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if (len(password1) < 8):
            raise ValidationError('Пароль должен состоять минимум из 8 символов')

        return password1