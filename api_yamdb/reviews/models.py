from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import datetime as dt

from .validators import symbols_validator, names_validator_reserved


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
START_YEAR = 0

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class CustomUser(AbstractUser):
    """Модель пользователя."""

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


def validate_year(year):
    """Валидация даты релиза."""

    current_year = dt.datetime.today().year
    if not (START_YEAR <= year <= current_year):
        raise ValidationError('Неподходящее значение')


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=150)
    year = models.IntegerField(validators=[validate_year])
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    genres = models.ManyToManyField(
        'Genre',
        through='TitleGenre'
    )
    description = models.TextField(max_length=250, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(max_length=150,)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug[:10]


class TitleGenre(models.Model):
    """Связующая модель жанров и произведений."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, {self.genre}'
