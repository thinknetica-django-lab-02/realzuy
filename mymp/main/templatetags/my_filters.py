from django import template
import datetime
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def my_text_reverse(value):
    return value[::-1]


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()

