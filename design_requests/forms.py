import os
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from django import forms
from .models import CustomUser, DesignRequest, Category


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

class DesignRequestForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        label="Название"
    )

    description = forms.CharField(
        max_length=255,
        required=True,
        label="Описание"
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Категория",
        empty_label="Выберите категорию"
    )

    photo = forms.ImageField(
        required=True,
        label="Фото помещения"
    )

    class Meta:
        model = DesignRequest
        fields = ['name', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        allowed_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
        ext = os.path.splitext(photo.name)[1].lower()
        if ext not in allowed_extensions:
            raise ValidationError(message="Формат фото должен быть JPG, JPEG, PNG или BMP.")

        max_size = 2 * 1024 * 1024
        if photo.size > max_size:
            raise ValidationError(message="Размер фото не должен превышать 2 МБ.")

        return photo

class DesignRequestUpdateForm(forms.ModelForm):
    comment = forms.CharField(
        required=True,
        max_length=255,
        label="Комментарий"
    )

    design_photo = forms.ImageField(
        required=True,
        label="Изображение готового дизайна"
    )

    STATUS_CHOICES_WITHOUT_NEW = [
        (value, label) for value, label in DesignRequest.STATUS_CHOICES
        if value != 'н'
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES_WITHOUT_NEW,
        label="Новый статус"
    )

    class Meta:
        model = DesignRequest
        fields = ['status', 'comment', 'design_photo']