from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

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
