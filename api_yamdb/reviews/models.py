from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import symbols_validator, names_validator_reserved

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            symbols_validator,
            names_validator_reserved
        ],
    )
    email = models.EmailField(
        verbose_name='Адрес эл. почты',
        max_length=150,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        max_length=max(len(role) for role, _ in ROLES),
        default=USER
    )

    class Meta(AbstractUser.Meta):
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
