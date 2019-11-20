INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'loginas',
    'django_extensions',
    'django_filters',
    'reversion',

    'user.apps.MainConfig',
    'projects.apps.ProjectsConfig',
    'main.apps.MainConfig',
]
