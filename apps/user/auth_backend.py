from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

__all__ = ['CustomAuthBackend']

UserModel = get_user_model()


class CustomAuthBackend(ModelBackend):
    """ авторизация по адресу почты """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
