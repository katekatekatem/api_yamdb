from django import forms

from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'score')
        labels = {
            'text': 'Оставить отзыв:',
            'score': 'Оценка:',
        }
        help_texts = {
            'text': 'Текст нового отзыва',
            'score': 'Поставьте оценку от 1 до 10',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Добавить комментарий:',
        }
        help_texts = {
            'text': 'Текст нового комментария',
        }
