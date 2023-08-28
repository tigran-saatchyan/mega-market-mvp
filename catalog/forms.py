from django import forms
from django.forms import BaseInlineFormSet

from catalog.models import Product, ProductVersion, Posts

PROHIBITED_WORDS = ['радар', 'казино', 'криптовалюта', 'крипта', 'биржа',
                    'дешево', 'бесплатно', 'обман', 'полиция']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


def validate_prohibited_words(clean_data):
    for word in PROHIBITED_WORDS:
        if word.lower() in clean_data.lower():
            raise forms.ValidationError(
                'Вы использовали одно из запрещённых слов: \n'
                f'{", ".join(PROHIBITED_WORDS)}'
            )


class ProductForm(StyleFormMixin, forms.ModelForm):

    def clean_name(self):
        clean_data = self.cleaned_data['name']
        validate_prohibited_words(clean_data)
        return clean_data

    def clean_description(self):
        clean_data = self.cleaned_data['description']
        validate_prohibited_words(clean_data)
        return clean_data

    class Meta:
        model = Product
        fields = (
            'name', 'description', 'image',
            'category', 'price', 'is_active', 'user'
        )


class ProductVersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = ProductVersion
        fields = ('version', 'version_name', 'is_current')


class ProductVersionFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        current_version_counter = sum(
            1
            for form in self.forms
            if form.cleaned_data.get('is_current')
        )

        if current_version_counter > 1:
            raise forms.ValidationError(
                'Только одна версия может быть активной'
            )
        for form in self.forms:
            if form.cleaned_data.get('DELETE') and form.cleaned_data.get(
                    'is_current'
            ):
                raise forms.ValidationError('Нельзя удалить активную версию')
        if current_version_counter == 0:
            raise forms.ValidationError(
                'Необходимо выбрать одну версию как активную'
            )


class PostForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('title', 'content', 'image', 'is_published')
