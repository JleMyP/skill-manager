from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

__all__ = ['CustomAuthBackend']

user_model = get_user_model()


class CustomAuthBackend(ModelBackend):
    """Авторизация по адресу почты."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            user_model().set_password(password)  # расчет хеша шоб время ответа выровнять
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
