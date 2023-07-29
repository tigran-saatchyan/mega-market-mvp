from django.urls import path

from catalog.views import index, contacts, categories, products, \
    product_description, products_by_categories, new_product

urlpatterns = [
    path('', index),
    path('products/', products),
    path('products/<int:product_id>', product_description),
    path('new_product/', new_product),
    path('categories/', categories),
    path('categories/<int:category_id>', products_by_categories),
    path('contacts/', contacts)
]
