from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer

__all__ = ['RegistrationSerializer', 'ProfileSerializer',
           'CustomTokenObtainSerializer']

user_model = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Кастомный юзер и хз че еще."""

    _validator = UniqueValidator(queryset=user_model.objects)
    email = serializers.EmailField(validators=[_validator], required=False, write_only=True)
    username = serializers.CharField(validators=[_validator], write_only=True)

    class Meta:
        model = user_model
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return make_password(value)


class ProfileSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ('username', 'email', 'first_name', 'last_name', 'middle_name',
                  'is_staff', 'date_joined')
        read_only_fields = ('username', 'email', 'is_staff', 'date_joined')


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    """Кастомизация полей для генератора апи."""

    password = PasswordField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(required=False, write_only=True)
