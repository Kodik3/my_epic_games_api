from typing import Any
# models.
from games.models import UserGame


def save_game_to_user(game: Any, user: Any):
    user.balance -= game.price
    user.save()
    game.quantity -= 1
    game.save()
    UserGame.objects.create(user=user, game=game)
    
def all_user_games(user: Any):
    return UserGame.objects.all().filter(user=user)