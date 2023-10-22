from django_cron import CronJobBase, Schedule
from .models import CastomUser
from datetime import datetime as dt
from abstracts.utils import send_email


class DailyTasks(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'auths.tasks.DailyTasks'
    
    def subscription_verification(self):
        '''
        Проверяются пользователи только с подпиской.
        Если дата окончания == сегодняшней, тогда
        убираем подписку у пользователя.
        '''
        today = dt.now().date()
        to_emails: list = []
        users = CastomUser.objects.filter(subscription=True, subscription_end_date=today)

        for user in users:
            user.subscription = False
            to_emails.append(user.email)
            user.save(update_fields=['subscription'])
        if to_emails:
            return send_email(
                f'У вас закончилась подписка',
                ('обновить подписку {}'.format('ссылка на страницу покупки подписки')),
                to_emails
            )
        else:
            return None
