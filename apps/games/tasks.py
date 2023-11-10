# Python.
from datetime import datetime as dt
import random
# Django.
from django.db.models import F, query
from django.core.mail import send_mail
# Celery.
from settings.celery import app
# models.
from .models import Game, Subscribe
from auths.models import CastomUser


@app.task
def do_test(*args, **kwargs):
    Game.objects.all().update(
        price=F('price') + 50
    )
    print("OK")
    
@app.task
def game_sub_verifi(game_id:int, *args, **kwargs):
    today = dt.now().date()
    game = Game.objects.get(pk=game_id)
    users = CastomUser.objects.all()
    
    for user in users:
        sub = Subscribe.objects.filter(
            game=game, 
            user=user,
            is_active=True,
            datetime_finished=today
        )
        sub.is_active=False
        sub.save(fields=['is_active'])

@app.task
def cancel_subcribe(subcribe_id: int, *args, **kwargs) -> None:
    Subscribe.objects.filter(id=subcribe_id).update(is_active=False)

@app.task
def finish_sub(sub, *args, **kwargs) -> None:
    """ countdown 30 days. """
    if sub.auto_buy is False:
        sub.is_active = False
        sub.save(update_fields=['is_active'])
    else:
        ... #! продливаем подписку (await sub.auto_buy: False)

@app.task(name='sub-remove')
def remove_subscribe(sub, *args, **kwargs) -> None:
    if sub:
        sub.is_active = True
        sub.save(fields=['is_active'])


@app.task(name='games-price-updater')
def games_price_updater() -> None:
    def random_value(rate: int) -> int:
        date_today = dt.now().date()
        if date_today.month == 1 and date_today.day == 1\
        or date_today.month == 11 and date_today.day == 11:
            game.price += random.randrange(0, -200)
        if rate >= 3:
            return random.randrange(0, -30)
        else:
            return random.randrange(1, 50)

    games: query.QuerySet[Game] = Game.objects.all()
    game: Game
    for game in games:
        game.price += random_value(game.rate)
        game.save(update_fields=('price',))

    print(f'All games prices were updated!!!')

