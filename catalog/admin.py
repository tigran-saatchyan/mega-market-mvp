from typing import Tuple

from django.contrib import admin

from catalog.models import Category, Product, Contact, Posts


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = ('id', 'name', 'description')

    list_display_links: Tuple[str] = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = (
        'id',
        'name',
        'description',
        'category',
        'price',
        'user',
        'is_active',
        'creation_date',
        'last_modified',
    )

    list_display_links: Tuple[str] = ('name',)

    list_filter: Tuple[str] = (
        'is_active',
        'category',
        'creation_date',
    )

    search_fields: Tuple[str] = ('name', 'description')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = (
        'id',
        'first_name',
        'last_name',
        'email',
        'tel_number',
        'address'
    )

    list_display_links: Tuple[str] = ('first_name', 'last_name')

    list_filter: Tuple[str] = ('last_name', 'tel_number')

    search_fields: Tuple[str] = (
        'first_name',
        'last_name',
        'email',
        'tel_number'
    )


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = (
        'id',
        'title',
        'content',
        'creation_date',
        'image',
        'is_published'
    )

    list_display_links = ('title',)

    list_filter = ('is_published',)

    search_fields = ('title',)
