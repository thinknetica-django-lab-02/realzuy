from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from .models import *

def SendWelcomeMessage(user):
    msg_title = 'Welcome to MyMP!'
    ctx = {
        'title': msg_title,
        'user_name': user.get_username
    }
    message = get_template('emails/welcome.html').render(ctx)

    msg = EmailMultiAlternatives(msg_title, 'Welcome message', settings.EMAIL_HOST_USER, [user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()


def SendNewStrategyMessage(strategy, profile):
    msg_title = 'Появилась новая стратегия'
    ctx = {
        'title': msg_title,
        'user_name': profile.user.get_username,
        'strategy_title': strategy.title,
        'strategy_description': strategy.description,
        'strategy_url': strategy.id
    }
    message = get_template('emails/strategy_new.html').render(ctx)

    msg = EmailMultiAlternatives(msg_title, 'New strategy message', settings.EMAIL_HOST_USER, [profile.user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()


def SendNewStrategiesMessage(strategies, profile):
    msg_title = 'Появились новые стратегии'
    ctx = {
        'title': msg_title,
        'user_name': profile.user.get_username,
        'strategies': strategies,
    }
    message = get_template('emails/strategies_new.html').render(ctx)

    msg = EmailMultiAlternatives(msg_title, 'New strategies message', settings.EMAIL_HOST_USER, [profile.user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()