from datetime import datetime, timedelta
from celery import Celery

from main.messages import SendNewStrategiesMessage, SendWelcomeMessage
import main.models as model

app = Celery('tasks')


@app.task
def send_new_strategies_weekly_schedule():
    date_start = datetime.now() - timedelta(days=7)
    strategies = model.Strategy.objects.filter(date_create__gte=date_start)

    for profile in model.Profile.objects.all():
        if profile.subscriptions.filter(id=1):
            SendNewStrategiesMessage(strategies, profile)


@app.task
def send_welcome_message_schedule(user_id):
    user = model.User.objects.get(pk=user_id)
    SendWelcomeMessage(user)
