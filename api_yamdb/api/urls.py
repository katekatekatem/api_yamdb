from django.urls import path, include
from rest_framework.routers import SimpleRouter


from users.views import TokenObtainView, UserRegistrationView
from .views import UserViewSet, ProfileUserView
router_v1 = SimpleRouter()

router_v1.register('users', UserViewSet)

auth_patterns = [
    path(
        'token/',
        TokenObtainView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'signup/',
        UserRegistrationView.as_view(),
        name='signup'
    ),
]

urlpatterns = [
    path('v1/users/me/', ProfileUserView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns))