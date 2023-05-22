from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import MixinViewSet
from .permissions import (IsAdminPermission, IsAdminOrReadOnlyPermission,
                          IsStaffOrAuthorOrReadOnlyPermission)
from .serializers import (AdminUserSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          ReviewSerializer, SignupSerializer,
                          TitleCreateSerializer, TitleReadSerializer,
                          TokenSerializer, UserSerializer)
from reviews.models import (Comment, Category, CustomUser,
                            Genre, Review, Title)


class SignUpView(APIView):
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        existing_user = self.check_existing_user(username, email)
        if not existing_user:
            user = self.create_user(username, email)
            if not user:
                return Response(
                    'Не удалось создать пользователя',
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            user = existing_user
        confirmation_code = default_token_generator.make_token(user)
        to_email = email
        self.send_confirmation_email(to_email, confirmation_code)
        response_data = {
            'username': user.username,
            'email': user.email
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def check_existing_user(self, username, email):
        user = CustomUser.objects.filter(
            username=username,
            email=email
        ).first()
        return user

    def create_user(self, username, email):
        try:
            user = CustomUser.objects.create(
                email=email,
                username=username
            )
            return user
        except IntegrityError:
            return None

    def send_confirmation_email(self, email, confirmation_code):
        send_mail(
            'Добро пожаловать!',
            f'Ваш код подтверждения: {confirmation_code}.',
            settings.YAMDB_EMAIL,
            [email],
            fail_silently=False,
        )


class GetTokenView(APIView):
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(CustomUser, username=username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            access_token = RefreshToken.for_user(user).access_token
            data = {'token': str(access_token)}
            return Response(
                data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            'Некорректный код.',
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        ['GET', 'PATCH'],
        url_path='me',
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(
                UserSerializer(request.user).data, status=status.HTTP_200_OK
            )
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleReadSerializer


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnlyPermission,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnlyPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnlyPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
