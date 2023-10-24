from django.db.models import F
from settings.celery import app
from .models import Game


@app.task
def do_test(*args, **kwargs):
    Game.objects.all().update(
        price=F('price') + 50
    )
    print("OK")
