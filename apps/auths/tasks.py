from django_cron import CronJobBase, Schedule
from celery import Celery
import schedule
from datetime import datetime as dt
import time
from .models import CastomUser
from abstracts.utils import send_email


#! 1 CronJobBase, Schedule
class DailyTasks(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'auths.tasks.DailyTasks'
    
    def subscription_verification(self):
        '''
        проверяются пользователи только с подпиской.
        если дата окончания == сегодняшней, тогда
        убираем подписку у пользователя.
        '''
        today = dt.now().date()
        to_emails: list = []
        users = CastomUser.objects.filter(subscription=False, subscription_end_date=today)
        for user in users:
            user.subscription = False
            to_emails.append(user.email)
            user.save(update_fields=['subscription'])
        if to_emails:
            return send_email(
                f'У вас закончилась подписка',
                    ('обновить подписку {}'.format('тут будет ссылка на страницу покупки подписки')),
                to_emails
            )
        else:
            return None

#! 2 schedule
# def subscription_verification():
#     today = dt.now().date()
#     to_emails = []
#     users = CastomUser.objects.filter(subscription=False, subscription_end_date=today)
#     for user in users:
#         user.subscription = False
#         to_emails.append(user.email)
#         user.save(update_fields=['subscription'])

#     if to_emails:
#         return send_email(
#             'У вас закончилась подписка',
#             'обновить подписку {}'.format('тут будет ссылка на страницу покупки подписки'),
#             to_emails
#         )
#     else: return None

# schedule.every().day.at("03:00").do(subscription_verification)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

#! 3 Celery
# app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

# @app.task
# def subscription_verification():
#     today = dt.now().date()
#     to_emails = []
#     users = CastomUser.objects.filter(subscription=False, subscription_end_date=today)
#     for user in users:
#         user.subscription = False
#         to_emails.append(user.email)
#         user.save(update_fields=['subscription'])
    
#     if to_emails:
#         return send_email(
#             'У вас закончилась подписка',
#             'обновить подписку {}'.format('тут будет ссылка на страницу покупки подписки'),
#             to_emails
#         )
#     else: return None


