from django import template

register = template.Library()


@register.filter
def media_path(path):
    from django.conf import settings

    media_url = settings.MEDIA_URL

    return f'{media_url}{path}'
