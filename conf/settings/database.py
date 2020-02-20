from .common import env

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3'),
}
