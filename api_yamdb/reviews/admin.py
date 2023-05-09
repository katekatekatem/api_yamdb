from django.contrib import admin
from .models import Title, Genre, Category


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('name', 'year',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'slug',
    ]
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
