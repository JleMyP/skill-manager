from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from ..models import CustomUser

__all__ = ['RegistrationSerializer', 'ProfileSerializer']


class RegistrationSerializer(serializers.ModelSerializer):
    """Кастомный юзер и хз че еще."""

    _validator = UniqueValidator(queryset=CustomUser.objects.all())
    email = serializers.EmailField(validators=[_validator], required=False, write_only=True)
    username = serializers.CharField(validators=[_validator], write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)


class ProfileSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'middle_name',
                  'is_staff', 'date_joined')
        read_only_fields = ('username', 'email', 'is_staff', 'date_joined')
