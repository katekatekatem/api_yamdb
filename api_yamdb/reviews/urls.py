from django.urls import path

from . import views


app_name = 'reviews'

urlpatterns = [
    path(
        'titles/<int:title_id>/reviews/',
        views.create_reviews,
        name='create_reviews'
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/',
        views.create_comments,
        name='create_comments'
    ),
]