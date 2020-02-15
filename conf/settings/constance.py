from .apps import INSTALLED_APPS

INSTALLED_APPS += [
    'constance',
    'constance.backends.database',
]

CONSTANCE_CONFIG = {
    'GIT_IMPORT_TAG': (0, 'Метка для ресурсов, импортированных из гита'),
    'CHROME_IMPORT_TAG': (0, 'Метка для ресурсов, импортированных из chrome'),
}
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
