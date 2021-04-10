from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from apscheduler.triggers.cron import CronTrigger

from .messages import SendNewStrategiesMessage
from .models import Strategy, Profile

scheduler = BackgroundScheduler()

def send_new_strategies_weekly_schedule():
    print('1')
    date_start = datetime.now() - timedelta(days=7)
    strategies = Strategy.objects.filter(date_create__gte=date_start)

    for profile in Profile.objects.all():
        if profile.subscriptions.filter(id=1):
            print('2')
            SendNewStrategiesMessage(strategies, profile)

trigger = CronTrigger(day_of_week='mon', hour=10)
#scheduler.add_job(send_new_strategies_weekly_schedule,  'interval', days = 7)
scheduler.add_job(send_new_strategies_weekly_schedule,  trigger)
scheduler.start()
