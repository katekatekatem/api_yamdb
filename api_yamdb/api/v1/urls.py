from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

registration_uls = [
    path('signup/', views.SignUpView.as_view()),
    path('token/', views.GetTokenView.as_view()),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(registration_uls)),
]