from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer

__all__ = ['CustomTokenObtainSerializer']


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    """Кастомизация полей для генератора апи."""

    password = PasswordField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(required=False, write_only=True)
