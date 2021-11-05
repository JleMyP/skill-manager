import typing
from pathlib import Path

import environ
from django.http import HttpRequest, HttpResponse

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'very secret key'),
    S3_BUCKET=(str, 'skill-manager'),
    S3_ACCESS_KEY_ID=(str, None),
    S3_SECRET_ACCESS_KEY=(str, None),
)
env.read_env()

BASE_DIR = Path(__file__).parents[2]

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ROOT_URLCONF = 'conf.urls'
WSGI_APPLICATION = 'conf.wsgi.application'
ASGI_APPLICATION = 'conf.asgi.application'

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3'),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'conf.settings.common.DisableCSRF',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


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
    'autocompletefilter',
    'django_object_actions',
    'django_json_widget',
    'reversion',
    'polymorphic',
    'storages',
    'drf_spectacular',
    'rest_framework',
    'rest_framework_serializer_extensions',
    'markdownx',
    'mptt',
    'debug_toolbar',
    'corsheaders',

    'constance',
    'constance.backends.database',

    'health_check',
    'health_check.db',

    'apps.user',
    'apps.projects',
    'apps.main',
]


class DisableCSRF:
    def __init__(self, get_response: typing.Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request._dont_enforce_csrf_checks = True
        return self.get_response(request)
