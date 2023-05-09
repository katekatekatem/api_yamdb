from django.contrib import admin

from .models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'text',
        'score',
    )
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'author',
        'text',
    )
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)