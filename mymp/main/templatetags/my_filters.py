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