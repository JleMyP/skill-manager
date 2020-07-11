import os

import environ


env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'very secret key'),
)
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__ + '/..')))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ROOT_URLCONF = 'conf.urls'
WSGI_APPLICATION = 'conf.wsgi.application'
ASGI_APPLICATION = 'conf.asgi.application'
