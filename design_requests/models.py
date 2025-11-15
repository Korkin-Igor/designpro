from django.db.models.functions import Lower
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from . import validators

class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Category name')
    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint (
                Lower("name"),
                name="category_name_lower_uniq",
                violation_error_message="Category with this name already exists (case-insensitive)."
            )
        ]

class DesignRequest(models.Model):
    name = models.CharField(max_length=100, help_text='Design request name')
    description = models.TextField(help_text='Design request description')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,        # ← обязательно!
        blank=True,       # если форма может быть пустой
        help_text='Design request category'
    )
    photo = models.ImageField(upload_to="uploads/", null=False, blank=False, help_text='Design request photo')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Design request creation date')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("design_requests:detail", args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="design_request_name_lower_uniq",
                violation_error_message="Category with this name already exists (case-insensitive)."
            )
        ]

class CustomUser(AbstractUser):
    full_name = models.CharField(
        max_length=255,
        help_text='Profile first name, last name and patronymic (only Cyrillic letters, hyphens, and spaces)'
    )

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("profile:detail", args=[str(self.id)])