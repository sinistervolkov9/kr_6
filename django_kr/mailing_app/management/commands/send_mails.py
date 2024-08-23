import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from django.utils import timezone
from mailing_app.models import Mailing, Attempt
from django.core.mail import send_mail
from django.conf import settings
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import pytz

MOSCOW_TZ = pytz.timezone('Europe/Moscow')
DEFAULT_FROM_EMAIL = 'sinister.volkov9@yandex.ru'


def send_mailing():
    now = timezone.now()
    mailings = Mailing.objects.filter(date_time__lte=now, status='created', periodicity='one time')
    for mailing_app in mailings:
        print('ok')
        for client in mailing_app.client.all():
            try:
                send_mail(
                    mailing_app.message.title,
                    mailing_app.message.text,
                    DEFAULT_FROM_EMAIL,
                    [client.email],
                    fail_silently=False,
                )
                Attempt.objects.create(
                    mailing=mailing_app,
                    status='ok',
                    # response='Mail sent successfully'
                )
            except Exception as e:
                print(e)
                Attempt.objects.create(
                    mailing=mailing_app,
                    status='failed',
                    # response=str(e)
                )
        mailing_app.status = 'completed'
        mailing_app.save()


logger = logging.getLogger(__name__)


def send_mailing_periodicity(periodicity, days):
    now = timezone.now().astimezone(MOSCOW_TZ).replace(microsecond=0)
    mailings = Mailing.objects.filter(periodicity=periodicity).exclude(status='completed')

    print(periodicity)

    for mailing_app in mailings:
        change_status(mailing_app)

        print(mailing_app)

        try:
            last_attempt_time = mailing_app.attempt.order_by('-attempt_time').values_list('attempt_time').first()[
                0].astimezone(MOSCOW_TZ)
        except Exception as e:
            last_attempt_time = mailing_app.start_date.astimezone(MOSCOW_TZ) - datetime.timedelta(days=days)

        print(last_attempt_time)

        lower_bound = last_attempt_time + datetime.timedelta(days=days, minutes=10)
        upper_bound = last_attempt_time + datetime.timedelta(days=days, minutes=-10)

        print(lower_bound)
        print(upper_bound)
        print(now)
        print()
        print(lower_bound >= now >= upper_bound)
        print(lower_bound >= now)
        print(now >= upper_bound)

        if lower_bound >= now >= upper_bound:

            print('отправка')

            for client in mailing_app.client.all():
                try:
                    send_mail(
                        mailing_app.message.title,
                        mailing_app.message.text,
                        DEFAULT_FROM_EMAIL,
                        [client.email],
                        fail_silently=False,
                    )
                    Attempt.objects.create(
                        mailing=mailing_app,
                        status='ok',
                        # response='Mail sent successfully'
                    )
                except Exception as e:
                    print(e)
                    Attempt.objects.create(
                        mailing=mailing_app,
                        status='failed',
                        # response=str(e)
                    )


class Command(BaseCommand):
    help = 'Runs APScheaduler'

    def handle(self, *args, **objects):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            send_mailing,
            trigger=CronTrigger(second='*/30'),
            id=f'send_message',
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            send_mailing_periodicity,
            trigger=CronTrigger(hour='*', minute='0'),
            id=f'send_message_day',
            max_instances=1,
            replace_existing=True,
            args=['day', 1]
        )

        scheduler.add_job(
            send_mailing_periodicity,
            trigger=CronTrigger(hour='*', minute='0'),
            id=f'send_message_week',
            max_instances=1,
            replace_existing=True,
            args=['week', 7]
        )

        scheduler.add_job(
            send_mailing_periodicity,
            trigger=CronTrigger(hour='*', minute='0'),
            id=f'send_message_month',
            max_instances=1,
            replace_existing=True,
            args=['month', 30]
        )

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()


def change_status(mailing):
    if timezone.now() > mailing.start_date:
        mailing.status = 'started'

    if timezone.now() > mailing.end_date:
        mailing.status = 'completed'

    mailing.save()

# scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
# scheduler.add_jobstore(DjangoJobStore(), 'default')

# send_mailing_periodicity('week', 7)


# def send_message():
#     send_mail('Заголовок', 'Сообщение', 'sinister.volkov9@yandex.ru', ['sinister.volkov9@yandex.ru'])


# @util.close_if_running
# def start_scheduler():
#     # scheduler.add_job(send_message, 'interval', seconds=30)
#     if not scheduler.get_jobs():
#         scheduler.add_job(send_mailing, 'interval', seconds=30)
#         scheduler.start()


# def start_or_not_mailing():
#     mailing_correct = Mailing.objects.title(status='started')
#     for mailing in mailing_correct:
#         logs = Attempt.objects.filter(mailing=mailing)
#         if not logs.exists():
#             add_job(mailing)


# def send_mailings(mailing):
#     # Attempt.objects.create(answer_severs='Отправлено', mailing_app=mailing_app)
#     Attempt.objects.create(mailing=mailing)
#     title = mailing.message.title
#     body = mailing.message.message
#     from_mail = 'sinister.volkov9@yandex.ru'
#     to_emails = [client.email for client in mailing.clients.all()]
#     send_mail(title, body, from_mail, to_emails)


# def add_job(mailing):
#     if mailing.periodicity == 'day':
#         cron_period = CronTrigger(second='*/30')
#     elif mailing.periodicity == 'week':
#         cron_period = CronTrigger(week='*/1')
#     else:
#         cron_period = CronTrigger(second='*/30')
#     scheduler.add_job(
#         send_mailings,
#         trigger=cron_period,
#         id=f'{mailing.pk}',
#         max_instances=1,
#         args=[mailing],
#         replace_existing=True,
#     )
