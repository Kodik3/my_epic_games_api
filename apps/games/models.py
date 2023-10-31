
"""| GAMES MODELS |"""

# Django.
from django.db import models
from django.core.validators import MinValueValidator
# models.
from auths.models import CastomUser
import datetime


class Game(models.Model):
    name = models.CharField(verbose_name='название', max_length=100, unique=True)
    price = models.DecimalField(verbose_name='цена', max_digits=11, decimal_places=2,
        validators=[MinValueValidator(0, message='Мы деньги за игры не даём!')]
    )
    poster = models.ImageField(verbose_name='постер', upload_to='posters', default='posters/default_game.png', blank=True)
    rate = models.FloatField(verbose_name='рэйтинг', max_length=5, default=0, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='количество', default=0, blank=True)
    # скидка
    is_discount = models.BooleanField(default=False)
    discount = models.FloatField(verbose_name='скидка', max_length=100, default=0, blank=True, null=True)
    # discount_duration = models.IntegerField(verbose_name='длительность скидки', default=0, blank=True) # в днях.

    @property
    def is_active(self):
        return self.quantity > 0
    
    class Meta:
        ordering=('id',)
        verbose_name='игра'
        verbose_name_plural = 'игры'

    def __str__(self):
        return f"{self.name} | {self.price:.2f}$"
    

class UserGame(models.Model):
    user = models.ForeignKey(to=CastomUser, verbose_name='владелец', on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, verbose_name='игра', on_delete=models.CASCADE)


class GameComment(models.Model):
    user = models.ForeignKey(to=CastomUser, verbose_name='пользователь', on_delete=models.CASCADE, related_name='comment')
    game = models.ForeignKey(to=Game, verbose_name='игра', on_delete=models.CASCADE, related_name='comment')
    text = models.CharField(verbose_name='текст', max_length=200)
    is_delete = models.BooleanField(default=False)
    
    class Meta:
        ordering=('-id',)
        verbose_name='комментрий'
        verbose_name_plural = 'комментрии'
        
    def __str__(self):
        return f"{self.user} | {self.game}"
    
class Subscripe(models.Model):
    game: Game = models.ForeignKey(
        to=Game,
        related_name='subs',
        on_delete=models.CASCADE
    )
    user: CastomUser = models.ForeignKey(
        to=CastomUser,
        related_name='subs',
        on_delete=models.CASCADE
    )
    is_active: bool = models.BooleanField(
        default=True
    )
    datetime_finished = models.DateField(
        verbose_name='Дата завершения',
        default=(datetime.datetime.today() + datetime.timedelta(days=30))
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'