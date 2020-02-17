from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.user'
    label = 'user'
    verbose_name = 'Профиль'


default_app_config = 'apps.user.UserConfig'
