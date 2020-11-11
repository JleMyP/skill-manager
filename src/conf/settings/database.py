from .common import env


DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3'),
}
