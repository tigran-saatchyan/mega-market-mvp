from datetime import datetime
from typing import Dict, Tuple

from django.db import models

NULLABLE: Dict[str, bool] = {'blank': True, 'null': True}


def save_picture(model, picture):
    app_name = __package__.split('.')[0]
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
        return f"{app_name}/product/{model.pk}/{model.pk}_{picture_name}"
    elif isinstance(model, Category):
        return f"{app_name}/category/{model.pk}/{model.pk}_{picture_name}"
    elif isinstance(model, Posts):
        return f"{app_name}/post/{model.pk}/{model.pk}_{picture_name}"


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
    views_count: int = models.IntegerField(
        default=0,
        verbose_name='views count'
    )
    current_version = models.ForeignKey(
        'ProductVersion',
        on_delete=models.SET_NULL,
        verbose_name='текущая версия',
        related_name='product_version',
        **NULLABLE
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Product'

    class Meta:
        verbose_name: str = 'Product'
        verbose_name_plural: str = 'Products'
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


class Posts(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(blank=True, verbose_name='content')
    image = models.ImageField(
        upload_to=save_picture,
        blank=True,
        verbose_name='image'
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creation date'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='is published'
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name='views count'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('creation_date',)
