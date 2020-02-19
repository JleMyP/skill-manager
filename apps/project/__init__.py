from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'apps.project'
    label = 'project'
    verbose_name = 'Проекты'


default_app_config = 'apps.project.ProjectsConfig'
