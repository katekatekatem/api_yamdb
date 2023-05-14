from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import CustomUser

from .permissions import AdminPermission
from .serializers import (AdminUserSerializer, SignupSerializer,
                          TokenSerializer, UserSerializer)


class SignUpView(APIView):
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = CustomUser.objects.get_or_create(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username']
            )
        except IntegrityError:
            return Response(
                'Данное имя пользователя и адрес эл. почты уже существуют',
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        to_email = serializer.validated_data['email']
        send_mail(
            'Добро пожаловать!',
            f'Ваш код подтверждения: {confirmation_code}.',
            settings.YAMDB_EMAIL,
            [to_email],
            fail_silently=False,
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


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
    permission_classes = (AdminPermission,)
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
