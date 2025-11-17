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
        help_text="Только латинские буквы и дефисы"
    )
    email = forms.EmailField(required=True)
    privacyConsent = forms.BooleanField(
        required=True,
        label="Согласие на обработку персональных данных",
        help_text="Я соглашаюсь"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'password1', 'password2', 'privacyConsent')

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.fullmatch(r'[а-яА-ЯёЁ\s\-]+', full_name):
            raise ValidationError("ФИО может состоять только из кириллических букв, пробелов и дефисов")
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.fullmatch(r'[a-zA-Z\-]+', username):
            raise ValidationError("Логин может состоять только из латинских букв и дефисов")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Такой логин уже зарегистрирован")
        return username