import os

import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'very secret key'),
)
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__ + "/..")))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ROOT_URLCONF = 'conf.urls'
WSGI_APPLICATION = 'conf.wsgi.application'
