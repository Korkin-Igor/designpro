from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        label="ФИО",
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}),
        help_text="Только кириллические буквы, дефисы и пробелы"
    )

    login = forms.CharField(
        label="Логин",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'ivan_ivanov'}),
        help_text="Только латиница и дефисы"
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'user@example.com'})
    )

    privacy_agreement = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        required=True,
        error_messages={
            '*': "Вы должны согласиться с обработкой персональных данных."
        }
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'login', 'email', 'password1', 'password2']

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            raise ValidationError("Поле ФИО обязательно для заполнения.")

        for char in full_name:
            if not (char.isalpha() or char in ' -' or char == 'ё' or char == 'Ё'):
                raise ValidationError("ФИО может содержать только кириллические буквы, пробелы и дефисы.")
        return full_name

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if not login:
            raise ValidationError("Логин обязателен.")

        for char in login:
            if not (char.isalnum() or char == '-'):
                raise ValidationError("Логин может содержать только латинские буквы, цифры и дефисы.")

        if CustomUser.objects.filter(username=login).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")

        return login

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email обязателен.")
        return email

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user