"""Views module"""
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, ProductVersionForm, PostForm, \
    ProductVersionFormset
from catalog.models import Product, Contact, Category, Posts, ProductVersion


class PostSlugifyMixin:
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
        send_mail(
            subject=subject,
            from_email=None,
            recipient_list=[email],
            message=message_to_send
        )

    return render(request, 'catalog/contacts.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'


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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product,
            ProductVersion,
            form=ProductVersionForm,
            extra=1
        )

        if self.request.method == 'POST':

            context['version_formset'] = VersionFormset(
                self.request.POST
            )
        else:
            context['version_formset'] = VersionFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = self.request.user

        version_formset = context['version_formset']
        self.object = form.save()
        if version_formset.is_valid():
            version_formset.instance = self.object
            version_formset.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product,
            ProductVersion,
            form=ProductVersionForm,
            formset=ProductVersionFormset,
            extra=1
        )

        if self.request.method == 'POST':
            version_formset = VersionFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            version_formset = VersionFormset(instance=self.object)

        context_data['version_formset'] = version_formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        version_formset = context_data['version_formset']

        self.object = form.save()
        if version_formset.is_valid():
            version_formset.instance = self.object
            version_formset.save()
        else:
            return self.form_invalid(form)

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('catalog:product_list')


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
                from_email=None,
                recipient_list=[email],
                message=message
            )
        self.object.save()
        return self.object


class PostCreateView(PostSlugifyMixin, CreateView):
    model = Posts
    template_name = 'catalog/posts_form.html'
    slug_url_kwarg = 'slug'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            'catalog:post_detail',
            kwargs={'slug': self.object.slug}
        )


class PostUpdateView(PostSlugifyMixin, UpdateView):
    model = Posts
    template_name = 'catalog/posts_form.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            'catalog:post_detail',
            kwargs={'slug': self.object.slug}
        )


class PostDeleteView(DeleteView):
    model = Posts
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('catalog:post_list')
