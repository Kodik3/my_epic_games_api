from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class CastomUserManager(BaseUserManager):
    def create_user(self, email: str, password:str=None, **kwargs):
        if not email:
            raise ValidationError('Требуется электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        # создание токена пользователя.
        refresh = RefreshToken.for_user(user)
        print(f"Access Token: {str(refresh.access_token)}")
        return user

    def create_superuser(self, email: str, password:str=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class CastomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='почта/логин', max_length=200, unique=True)
    password = models.CharField(verbose_name='пароль', max_length=60, unique=True)
    name = models.CharField(verbose_name='имя', max_length=100)
    balance: float = models.DecimalField(verbose_name='баланс', max_digits=11, decimal_places=2, default=0.00)
    is_staff: bool = models.BooleanField(default=False)
    # подписка \
    subscription: bool = models.BooleanField(default=False, verbose_name='подписка')
    subscription_end_date = models.DateField(verbose_name='дата окончания', blank=True, null=True)
    
    objects = CastomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return self.email
