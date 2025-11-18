from django.db.models.functions import Lower
from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Название категории')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        permissions = (('can_manage_categories', 'Пользователь может управлять категориями'),)
        constraints = [
            UniqueConstraint (
                Lower("name"),
                name="category_name_lower_uniq",
                violation_error_message="Такая категория уже есть"
            )
        ]

class DesignRequest(models.Model):
    name = models.CharField(max_length=100, help_text='Название')
    description = models.TextField(help_text='Описание')

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='Категория заявки'
    )

    STATUS_CHOICES = (
        ('н', 'Новая'),
        ('п', 'Принято в работу'),
        ('в', 'Выполнено'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='н'
    )

    photo = models.ImageField(
        upload_to="user_photos/",
        null=False,
        blank=False,
        help_text='Фото помещения'
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='design_requests',
        help_text='Пользователь, создавший заявку'
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text='Временная метка')

    # для админа
    comment = models.TextField(
        null=True,
        help_text='Комментарий при принятии в работу'
    )
    design_photo = models.ImageField(
        upload_to="designs/",
        null=True,
        help_text='Готовый дизайн'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("design_requests:detail", args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Заявки"
        permissions = (('can_manage_requests', 'Пользователь может редактировать заявки'),)
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="design_request_name_lower_uniq",
                violation_error_message="Заявка с таким названием уже существует"
            )
        ]