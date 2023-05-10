from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        return user


class TokenObtainSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(
            max_length=150,
            validators=(UnicodeUsernameValidator,))
        self.fields['confirmation_code'] = serializers.CharField(max_length=50)

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        try:
            self.user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            return {'error': 'Пользователь не найден.'}
        if not self.user.is_active:
            raise serializers.ValidationError(
                'Пользователь заблокирован'
            )
        if default_token_generator.check_token(self.user, confirmation_code):
            refresh = self.get_token(self.user)
            token = refresh.access_token
            update_last_login(None, self.user)

            return {"token": str(token)}
        raise serializers.ValidationError(
            'Неверный код пподтвержддения'
        )
