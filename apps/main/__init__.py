from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'apps.main'
    label = 'main'
    verbose_name = 'Основное'


default_app_config = 'apps.main.MainConfig'
