from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        required=True,
        label="ФИО",
        widget=forms.TextInput()
    )

    login = forms.CharField(
        max_length=255,
        required=True,
        label="Логин",
        widget=forms.TextInput()
    )

    privacyConsent = forms.BooleanField(
        required=True,
        label="Согласие на обработку персональных данных",
        widget=forms.CheckboxInput(),
        help_text="Я соглашаюсь"
    )

    class Meta:
        model = CustomUser
        fields = ('full_name', 'login', 'email', 'password1', 'password2', 'privacyConsent')

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not re.search('^[а-яА-Я\-\s]+$', full_name):
            raise ValidationError(message="ФИО может состоять только из кириллических буквы, дефисов и пробелов")
        return full_name

    def clean_password2(self):
        pass