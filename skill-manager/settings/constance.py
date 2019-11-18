from .apps import INSTALLED_APPS

INSTALLED_APPS += [
    'constance',
    'constance.backends.database',
]

CONSTANCE_CONFIG = {}
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
