"""Views module"""
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product, Customer, Contact


def index(request: WSGIRequest) -> HttpResponse:
    """Renders the index page.

    Args:
        request (WSGIRequest): The WSGIRequest object representing the
        HTTP request.

    Returns:
        HttpResponse: The HTTP response object containing the rendered
        index page.
    """
    last_five_products_list = Product.objects.filter(
        is_active=True
    ).order_by('-creation_date')[:5]
    context = {
        "products": last_five_products_list
    }

    return render(request, 'catalog/index.html', context)


def contacts(request: WSGIRequest) -> HttpResponse:
    """Handles the contacts page.

    If the request method is POST, it processes the form data and
    prints the message.

    Args:
        request (WSGIRequest): The WSGIRequest object representing the
        HTTP request.

    Returns:
        HttpResponse: The HTTP response object containing the rendered
        contacts page.
    """
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
