from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import datetime as dt


START_YEAR = 0

User = get_user_model()


def validate_yaer(year):
    """Валидация даты релиза."""

    current_year = dt.datetime.today().year
    if not (START_YEAR <= year <= current_year):
        raise ValidationError('Неподходящее значение')


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=150)
    year = models.IntegerField(validators=[validate_yaer])
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


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]
