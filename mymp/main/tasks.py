from datetime import datetime, timedelta
from celery import shared_task
from celery.utils.log import get_task_logger
from main.messages import SendNewStrategiesMessage, SendWelcomeMessage, SendSMS
import main.models as main_model
import random

logger = get_task_logger(__name__)


@shared_task
def send_new_strategies_weekly_schedule():
    date_start = datetime.now() - timedelta(days=7)
    strategies = main_model.Strategy.objects.filter(
        date_create__gte=date_start)

    for profile in main_model.Profile.objects.all():
        if profile.subscriptions.filter(id=1):
            SendNewStrategiesMessage(strategies, profile)


@shared_task
def send_welcome_message_schedule(user_id):
    logger.info('send_welcome_message_schedule')
    user = main_model.User.objects.get(pk=user_id)
    SendWelcomeMessage(user)


@shared_task
def send_sms_code(phone_number, user_id):
    code = random.randint(1000, 9999)
    status = SendSMS(phone_number, code)
    sms = main_model.SMSlog.objects.create(
        code=code, status=status)
    user = main_model.User.objects.get(pk=user_id)
    user.smslog_set.add(sms)
