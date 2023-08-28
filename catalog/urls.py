from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, \
    CategoryListView, ProductDetailedView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView, \
    CategoryProductsListView, MainListView, PostListView, \
    PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', MainListView.as_view(), name='index'),
    path(
        'products/list/',
        ProductListView.as_view(),
        name='product_list'
    ),
    path(
        'products/view/<int:pk>',
        ProductDetailedView.as_view(),
        name='product_detail'
    ),
    path(
        'products/create/',
        ProductCreateView.as_view(),
        name='create_product'
    ),
    path(
        'products/update/<int:pk>',
        ProductUpdateView.as_view(),
        name='update_product'
    ),
    path(
        'products/delete/<int:pk>',
        ProductDeleteView.as_view(),
        name='delete_product'
    ),
    path(
        'categories/list/',
        CategoryListView.as_view(),
        name='categories'
    ),
    path(
        'categories/<int:pk>/products/',
        CategoryProductsListView.as_view(),
        name='category_products'
    ),

    path('contacts/', contacts, name='contacts'),

    path(
        'blog/posts/list/',
        PostListView.as_view(),
        name='post_list'
    ),
    path(
        'blog/posts/view/<slug:slug>',
        PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'blog/posts/create/',
        PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'blog/posts/update/<slug:slug>',
        PostUpdateView.as_view(),
        name='update_post'
    ),
    path(
        'blog/posts/delete/<slug:slug>',
        PostDeleteView.as_view(),
        name='delete_post'
    )
]
