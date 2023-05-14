from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router_v1 = DefaultRouter()
router_v1.register(r'users', views.UserViewSet, basename='users')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('categories', views.CategoryViewSet, basename='categories')

registration_uls = [
    path('signup/', views.SignUpView.as_view()),
    path('token/', views.GetTokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(registration_uls)),
]
