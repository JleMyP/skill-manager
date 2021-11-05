from typing import (
    Any,
    Optional,
    Type,
)

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser

__all__ = ['CustomAuthBackend']


user_model: Type[AbstractUser] = get_user_model()  # type: ignore


class CustomAuthBackend(ModelBackend):
    """Авторизация по адресу почты."""

    def authenticate(self, _request: Any, username: Optional[str] = None,
                     password: Optional[str] = None, **kwargs) -> user_model:
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            user_model().set_password(password)  # расчет хеша шоб время ответа выровнять
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
