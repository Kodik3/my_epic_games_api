from datetime import datetime as dt
from .models import CastomUser
from abstracts.utils import send_email


@app.task
def subscription_verification():
    today = dt.now().date()
    to_emails: list = []
    users = CastomUser.objects.filter(subscription=False, subscription_end_date=today)
    for user in users:
        user.subscription = False
        to_emails.append(user.email)
        user.save(update_fields=['subscription'])
    
    if to_emails:
        return send_email(
            'У вас закончилась подписка',
            'обновить подписку {}'.format('тут будет ссылка на страницу покупки подписки'),
            to_emails
        )
    else: return None


