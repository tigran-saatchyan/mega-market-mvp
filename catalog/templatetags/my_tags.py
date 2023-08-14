from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def media_path(path):
    from django.conf import settings

    media_url = settings.MEDIA_URL

    return f'{media_url}{path}'
