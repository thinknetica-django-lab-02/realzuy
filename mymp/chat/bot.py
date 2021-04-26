import os
import django
from main.models import Strategy

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


def reply_from_server(message: str) -> str:
    if message[:1] == '#':
        message = message[1:]
        return is_revenue_message(message)
    else:
        return 'Не знаю что ответить на это'


def is_revenue_message(name):
    try:
        if Strategy.objects.get(title=name).is_revenue:
            return 'Доходная стратегия'
        return 'Фигня'
    except Strategy.DoesNotExist:
        return 'Ничего не найдено'
