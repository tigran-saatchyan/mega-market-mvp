from datetime import datetime
from typing import Dict, Tuple

from django.db import models

from service.utils import save_picture
from users.models import User

NULLABLE: Dict[str, bool] = {'blank': True, 'null': True}


class Category(models.Model):
    name: str = models.CharField(
        verbose_name='категория',
        max_length=100,
        unique=True
    )
    description: str = models.CharField(
        verbose_name='описание'
    )

    image: str = models.ImageField(
        verbose_name='изображение',
        upload_to=save_picture,
        **NULLABLE
    )

    class Meta:
        verbose_name: str = 'категория'
        verbose_name_plural: str = 'категории'
        ordering: Tuple[str] = ('pk',)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Category(name: {self.name})'


class Product(models.Model):
    name: str = models.CharField(
        verbose_name='продукт',
        max_length=100
    )
    description: str = models.TextField(
        verbose_name='описание'
    )
    image: str = models.ImageField(
        verbose_name='изображение',
        upload_to=save_picture,
        **NULLABLE
    )
    category: int = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.CASCADE,
        **NULLABLE
    )
    price: int = models.PositiveIntegerField(
        verbose_name='цена',
        **NULLABLE
    )
    creation_date: datetime = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    last_modified: datetime = models.DateTimeField(
        verbose_name='последнее изменение',
        auto_now=True
    )

    is_active: bool = models.BooleanField(
        verbose_name='активен',
        default=True
    )
    views_count: int = models.IntegerField(
        default=0,
        verbose_name='просмотры'
    )
    current_version = models.ForeignKey(
        'ProductVersion',
        on_delete=models.SET_NULL,
        verbose_name='текущая версия',
        related_name='product_version',
        **NULLABLE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        **NULLABLE
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Product'

    class Meta:
        verbose_name: str = 'продукт'
        verbose_name_plural: str = 'продукты'
        ordering: Tuple[str] = ('last_modified', '-views_count')


class ProductVersion(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='продукт',
    )
    version = models.SmallIntegerField(verbose_name='версия')
    version_name = models.CharField(
        max_length=50,
        verbose_name='название версии',
        **NULLABLE
    )
    is_current = models.BooleanField(default=False)

    def __str__(self):
        result = f'{self.version} ({self.version_name})' \
            if self.version_name else self.version
        return result

    class Meta:
        verbose_name = 'Версия Продукта'
        verbose_name_plural = 'Версии Продуктов'
        ordering = ('version',)


class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(max_length=255, verbose_name='Эл. Почта')
    tel_number = models.CharField(
        max_length=20,
        verbose_name='Телефонный номер'
    )
    address = models.TextField(verbose_name='Адрес', **NULLABLE)
    date_added: datetime = models.DateTimeField(
        verbose_name='Дата отправки',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"first_name={self.first_name}\n" \
               f"last_name={self.last_name}\n" \
               f"email={self.email}\n" \
               f"tel_number={self.tel_number}\n" \
               f"date_added={self.date_added}"

    class Meta:
        verbose_name: str = 'контакт'
        verbose_name_plural: str = 'контакты'
        ordering: Tuple[str] = ('date_added',)


class Posts(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(blank=True, verbose_name='контент')
    image = models.ImageField(
        upload_to=save_picture,
        blank=True,
        verbose_name='изображение'
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='опубликован'
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name='просмотры'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('creation_date',)
