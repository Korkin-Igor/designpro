from django.core.exceptions import ValidationError
import re

def full_name_validator(value):
    if not re.fullmatch(r'^[а-яА-ЯёЁ\s\-]+$', value):
        raise ValidationError({
            'full_name': 'ФИО должно содержать только кириллические буквы, пробелы и дефисы.'
        })