from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenView, SignUpView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

registration_uls = [
    path('signup/', SignUpView.as_view()),
    path('token/', GetTokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(registration_uls)),
]
