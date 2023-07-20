"""Views module"""
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def index(request: WSGIRequest) -> HttpResponse:
    """Renders the index page.

    Args:
        request (WSGIRequest): The WSGIRequest object representing the
        HTTP request.

    Returns:
        HttpResponse: The HTTP response object containing the rendered
        index page.
    """
    return render(request, 'catalog/index.html')


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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Пользователь {name} ({email}) оставил отзыв: {message}")
    return render(request, 'catalog/contacts.html')
