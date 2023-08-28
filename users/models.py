from datetime import datetime
from typing import Dict

from django.contrib.auth.models import AbstractUser
from django.db import models

from service.utils import save_picture

NULLABLE: Dict[str, bool] = {'blank': True, 'null': True}


class Country(models.Model):
    name = models.CharField(max_length=255, **NULLABLE, verbose_name='страна')
    code = models.CharField(max_length=255, **NULLABLE, verbose_name='код')

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    telephone = models.CharField(
        max_length=50, verbose_name='телефон', **NULLABLE
    )
    country = models.ForeignKey(
        Country,
        verbose_name='страна',
        on_delete=models.CASCADE,
        max_length=255,
        **NULLABLE,
    )
    avatar = models.ImageField(upload_to=save_picture, **NULLABLE)
    date_added: datetime = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    last_modified: datetime = models.DateTimeField(
        verbose_name='последнее изменениесдуфк',
        auto_now=True
    )

    is_verified: bool = models.BooleanField(
        verbose_name='статус верификации',
        default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('date_added',)
