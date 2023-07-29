from datetime import datetime
from typing import Dict, Tuple

from django.db import models

NULLABLE: Dict[str, bool] = {'blank': True, 'null': True}


def save_picture(model, picture):
    my_date = str(datetime.now().isoformat())
    picture_name = "".join(
        [
            "".join(picture.split('.')[:-1]),
            my_date,
            ".",
            picture.split('.')[-1]
        ]
    )
    if isinstance(model, Product):
        return f"product/{model.pk}/{model.pk}_{picture_name}"
    elif isinstance(model, Category):
        return f"category/{model.pk}/{model.pk}_{picture_name}"


class Category(models.Model):
    name: str = models.CharField(
        verbose_name='category',
        max_length=100,
        unique=True
    )
    description: str = models.CharField(
        verbose_name='description'
    )

    image: str = models.ImageField(
        verbose_name='image',
        upload_to=save_picture,
        **NULLABLE
    )

    class Meta:
        verbose_name: str = 'Category'
        verbose_name_plural: str = 'Categories'
        ordering: Tuple[str] = ('pk',)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Category(name: {self.name})'


class Product(models.Model):
    name: str = models.CharField(
        verbose_name='product name',
        max_length=100
    )
    description: str = models.TextField(
        verbose_name='description'
    )
    image: str = models.ImageField(
        verbose_name='image',
        upload_to=save_picture,
        **NULLABLE
    )
    category: int = models.ForeignKey(
        Category,
        verbose_name='category name',
        on_delete=models.CASCADE,
        **NULLABLE
    )
    purchase_price: int = models.PositiveIntegerField(
        verbose_name='purchase price',
        **NULLABLE
    )
    creation_date: datetime = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True
    )
    last_modified: datetime = models.DateTimeField(
        verbose_name='last modified',
        auto_now_add=True
    )

    is_active: bool = models.BooleanField(
        verbose_name='is active',
        default=True
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Product'

    class Meta:
        verbose_name: str = 'Product'
        verbose_name_plural: str = 'Products'
        ordering: Tuple[str] = ('last_modified',)


class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(max_length=255, verbose_name='Эл. Почта')
    tel_number = models.CharField(
        max_length=20,
        verbose_name='Телефонный номер'
    )
    message = models.TextField(verbose_name='Сообщение')
    date_added: datetime = models.DateTimeField(
        verbose_name='Дата отправки',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"first_name={self.first_name}\n" \
               f"last_name={self.last_name}\n" \
               f"email={self.email}" \
               f"tel_number={self.tel_number}\n" \
               f"message={self.message}\n" \
               f"date_added={self.date_added}"

    class Meta:
        verbose_name: str = 'Customer'
        verbose_name_plural: str = 'Customers'
        ordering: Tuple[str] = ('date_added',)


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
        verbose_name: str = 'Contact'
        verbose_name_plural: str = 'Contacts'
        ordering: Tuple[str] = ('date_added',)
