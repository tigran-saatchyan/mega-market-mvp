from django.shortcuts import render


def index(request):
    return render(request, 'catalog/index.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Пользователь {name} ({email}) оставил отзыв: {message}")
    return render(request, 'catalog/contacts.html')
