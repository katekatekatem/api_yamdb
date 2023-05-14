from rest_framework import serializers
from reviews.models import CustomUser
from reviews.validators import reserved_names_validator, regex_validator


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[regex_validator, reserved_names_validator]
    )
    email = serializers.EmailField(
        max_length=150,
        required=True
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[regex_validator, reserved_names_validator]
    )
    confirmation_code = serializers.CharField(
        required=True
    )


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        regex_validator(value)
        reserved_names_validator(value)
        return value


class UserSerializer(AdminUserSerializer):

    class Meta(AdminUserSerializer.Meta):
        read_only_fields = ('role',)
