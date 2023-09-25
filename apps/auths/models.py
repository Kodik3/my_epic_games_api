from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError


class CastomUserManager(BaseUserManager):
    def create_user(self, email: str, password:str=None, **kwargs):
        if not email:
            raise ValidationError('Требуется электронная почта')
        email = self.normalize_email(email)
        user: 'MyUser' = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password:str=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class CastomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='почта/логин', max_length=200, unique=True)
    password = models.CharField(verbose_name='пароль', max_length=60, unique=True)
    name = models.CharField(verbose_name='имя', max_length=100)
    balance = models.DecimalField(verbose_name='баланс', max_digits=11, decimal_places=2, default=0.00)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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
