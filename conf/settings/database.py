import os

from .common import BASE_DIR, env


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3'),
}
