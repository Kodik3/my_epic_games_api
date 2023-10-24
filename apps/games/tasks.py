from django.db.models import F
from settings.celery import app
from .models import Game, Subscripe
from auths.models import CastomUser
from datetime import datetime as dt


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
        sub = Subscripe.objects.filter(
            game=game, 
            user=user,
            is_active=True,
            datetime_finished=today
        )
        sub.is_active=False
        sub.save(fields=['is_active'])
        
@app.task
def finish_sub(user, game_id:int, *args, **kwargs):
    ...
    
