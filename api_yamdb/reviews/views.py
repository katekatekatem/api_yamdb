from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .forms import CommentForm, ReviewForm
from .models import Review, Title


@login_required
def create_reviews(request, title_id):
    title = get_object_or_404(Title, pk=title_id)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.title = title
        comment.save()
    return redirect('reviews:create_reviews', title_id=title_id)


@login_required
def create_comments(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.review = review
        comment.save()
    return redirect('reviews:create_comments', review_id=review_id)
