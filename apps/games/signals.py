# Django.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
# models.
from auths.models import CastomUser
from .models import Game



@receiver(post_save, sender=Game)
def span_attack_when_create_new_game(
    sender: Game.__class__,
    instance: Game,
    created: bool,
    **kwargs
) -> None:
    emails: list[str] = CastomUser.objects.filter(is_staff=False).values_list('email', flat=True)
    send_mail(
        subject='EPIC GAMES! NEW GAME!',
        message='Вышла новая игра, иди купи!',
        from_email='boss.barbashin10@gmail.com',
        recipient_list=emails
    )
    
@receiver(post_save, sender=Game)
def span_attack_when_game_discount_added(
    sender: Game.__class__,
    instance: Game,
    update: bool,
    **kwargs
) -> None:
    if instance.is_discount is True:
        emails: list[str] = CastomUser.objects.filter(is_staff=False).values_list('email', flat=True)
        send_mail(
            subject='EPIC GAMES! DISCOUNT GAME!',
            message=f'Вышла скидка на {instance.name}, иди купи!',
            from_email='boss.barbashin10@gmail.com',
            recipient_list=emails
        )
        
@receiver(post_save, sender=Game)
def apply_discount(
    sender: Game.__class__,
    instance: Game,
    **kwargs
) -> None:
    if instance.is_discount:
        instance.price = (instance.price/100) * instance.discount
        instance.save()