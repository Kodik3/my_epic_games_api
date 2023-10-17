from django_cron import CronJobBase, Schedule
from .models import CastomUser
from datetime import datetime as dt
from abstracts.utils import send_email


class DailyTasks(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'auths.tasks.DailyTasks'
    
    def subscription_verification(self):
        '''
        проверяются пользователи только с подпиской.
        если дата окончания == сегодняшней, тогда
        убираем подписку у пользователя.
        '''
        users = CastomUser.objects.all()
        to_emails = []
        for user in users:
            if user.subscription == True:
                if user.subscription_end_date == dt.now():
                    user.subscription = False
                    to_emails.append(user.email)
                    user.save(update_fields=['subscription'])
        return send_email(
            f'У вас закончилась подписка',
                ('обновить подписку {}'.format('тут будет ссылка на страницу покупки подписки')),
            to_emails
        )
