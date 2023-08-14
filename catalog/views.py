"""Views module"""
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from catalog.models import Product, Contact, Category, Posts
from catalog.utils import send_mail


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 4
    ordering = ['-creation_date']
    queryset = Product.objects.filter(
        is_active=True
    )


class ProductDetailedView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class MainListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/product_main.html'
    ordering = ['-creation_date']

    def get_queryset(self):
        queryset = Product.objects.filter(
            is_active=True
        )[:5]
        return queryset


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

        message_to_send = f"Пользователь: <strong>{first_name.title()} " \
                          f"{last_name.title()}</strong><br>" \
                          f"Епошта: <strong>{email}</strong> <br>" \
                          f"Номер телефона: <strong>{tel_number}</strong>" \
                          f"<br>Сообщение: <p style=\"margin-left: 50px;\">" \
                          f"{message}</p>"

        subject = f'Make Appointment with {first_name} {last_name}'
        send_mail(subject=subject, message=message_to_send, to_email=email)

    return render(request, 'catalog/contacts.html', context)


class CategoryProductsListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 4
    ordering = ['-creation_date']

    def get_queryset(self):
        category = self.kwargs['pk']
        queryset = Product.objects.filter(
            category=category,
            is_active=True
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['pk']
        category = Category.objects.get(id=category)
        context["category_description"] = category.description
        context["category_name"] = category.name
        return context


class ProductCreateView(CreateView):
    model = Product
    fields = (
        'name', 'description', 'image',
        'category', 'purchase_price', 'is_active'
    )
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = (
        'name', 'description', 'image',
        'category', 'purchase_price', 'is_active'
    )
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('catalog:product_list')


# Добавление продукта через форму из шаблона product_form_bak.html
# def get_current_autoincrement_value(table_name, column_name='id'):
#     sequence_name = f"{table_name}_{column_name}_seq"
#
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT nextval('{sequence_name}');")
#         cursor.execute(f"SELECT currval('{sequence_name}');")
#         result = cursor.fetchone()
#
#     return result[0] if result else None


# def new_product(request: WSGIRequest) -> HttpResponse:
#     category_list = Category.objects.all()
#     category_mapping = {}
#     current_id = get_current_autoincrement_value('catalog_product')
#
#     if request.POST:
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         image = request.FILES['image']
#         category_id = request.POST.get('category')
#         purchase_price = request.POST.get('price')
#         is_active = request.POST.get('is_active')
#
#         for category in category_list:
#             category_mapping[category.id] = category
#
#         Product.objects.create(
#             id=current_id,
#             name=name,
#             description=description,
#             image=image,
#             category=Category.objects.get(id=category_id),
#             purchase_price=purchase_price,
#             is_active=is_active
#         )
#
#     context = {
#         "categories": category_list
#     }
#
#     return render(request, 'catalog/product_form.html', context)

class PostListView(ListView):
    model = Posts
    context_object_name = 'posts'
    template_name = 'catalog/posts_list.html'
    paginate_by = 4
    ordering = ('-creation_date',)

    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset.filter(
            is_published=True
        )
        return result


class PostDetailView(DetailView):
    model = Posts
    context_object_name = 'post'
    template_name = 'catalog/posts_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1

        if self.object.views_count == 100:
            subject = f'Поздравляем!'
            message = f'<p>Пост {self.object.title} достиг ' \
                      f'отметки в 100 просмотров</p>'
            email = 'mr.saatchyan@yandex.com'

            send_mail(
                subject=subject,
                message=message,
                to_email=email
            )
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = Posts
    template_name = 'catalog/posts_form.html'
    fields = ('title', 'content', 'image', 'is_published')
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        post = form.save(commit=False)
        slug = slugify(post.title)
        post_objects = Posts.objects
        if post_objects.filter(slug=slug).exists():
            count = 1
            while post_objects.filter(slug=f'{slug}-{count}').exists():
                count += 1
            slug = f'{slug}-{count}'

        post.slug = slug
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'catalog:post_detail',
            kwargs={'slug': self.object.slug}
        )


class PostUpdateView(UpdateView):
    model = Posts
    template_name = 'catalog/posts_form.html'
    fields = ('title', 'content', 'image', 'is_published')
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        slug = slugify(post.title)
        post_objects = Posts.objects
        if post_objects.filter(slug=slug).exists():
            count = 1
            while post_objects.filter(slug=f'{slug}-{count}').exists():
                count += 1
            slug = f'{slug}-{count}'
        post.slug = slug
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'catalog:post_detail',
            kwargs={'slug': self.object.slug}
        )


class PostDeleteView(DeleteView):
    model = Posts
    context_object_name = 'post'
    success_url = reverse_lazy('catalog:post_list')
    slug_url_kwarg = 'slug'
