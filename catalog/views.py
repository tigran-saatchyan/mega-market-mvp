"""Views module"""
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product, Customer, Contact, Category


def get_current_autoincrement_value(table_name, column_name='id'):
    sequence_name = f"{table_name}_{column_name}_seq"

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT nextval('{sequence_name}');")
        cursor.execute(f"SELECT currval('{sequence_name}');")
        result = cursor.fetchone()

    return result[0] if result else None


def index(request: WSGIRequest) -> HttpResponse:

    last_five_products_list = Product.objects.filter(
        is_active=True
    ).order_by('-creation_date')[:5]
    context = {
        "products": last_five_products_list
    }

    return render(request, 'catalog/index.html', context)


def categories(request: WSGIRequest) -> HttpResponse:

    category_list = Category.objects.all()
    context = {
        "categories": category_list
    }

    return render(request, 'catalog/categories.html', context)


def products(request: WSGIRequest) -> HttpResponse:

    all_products = Product.objects.filter(
        is_active=True
    ).order_by('-creation_date')

    paginator = Paginator(all_products, 4)

    page_number = request.GET.get('page', 1)

    page_obj = paginator.get_page(page_number)
    context = {
        "products": page_obj
    }
    return render(request, 'catalog/products.html', context)


def contacts(request: WSGIRequest) -> HttpResponse:

    try:
        contact = Contact.objects.filter(id=1)[0]
    except IndexError:
        contact = None

    context = {
        'contact': contact
    }

    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        tel_number = request.POST.get('phone')
        message = request.POST.get('message')

        print(
            f"Пользователь {first_name.title()} {last_name.title()} "
            f"({email}) оставил отзыв: {message}"
        )

        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            tel_number=tel_number,
            message=message
        )
    return render(request, 'catalog/contacts.html', context)


def product_description(request: WSGIRequest, product_id: int) -> HttpResponse:
    product = Product.objects.filter(
        id=product_id
    )
    context = {
        "products": product
    }

    return render(request, 'catalog/product_description.html', context)


def products_by_categories(
        request: WSGIRequest, category_id: int
) -> HttpResponse:
    category = Category.objects.get(id=category_id)
    product_list = Product.objects.filter(
        category=category_id, is_active=True
    )
    paginator = Paginator(product_list, 4)

    page_number = request.GET.get('page', 1)

    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "category_description": category.description,
        "category_name": category.name
    }

    return render(request, 'catalog/products.html', context)


def new_product(request: WSGIRequest) -> HttpResponse:
    category_list = Category.objects.all()
    category_mapping = {}
    current_id = get_current_autoincrement_value('catalog_product')

    if request.POST:
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES['image']
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        is_active = request.POST.get('is_active')

        for category in category_list:
            category_mapping[category.id] = category

        Product.objects.create(
            id=current_id,
            name=name,
            description=description,
            image=image,
            category=Category.objects.get(id=category_id),
            purchase_price=price,
            is_active=is_active
        )

    context = {
        "categories": category_list
    }

    return render(request, 'catalog/new_product.html', context)
