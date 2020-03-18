from .apps import INSTALLED_APPS


INSTALLED_APPS += [
    'constance',
    'constance.backends.database',
]

CONSTANCE_CONFIG = {
    'GIT_IMPORT_TAG': (0, 'Метка для ресурсов, импортированных из гита'),
    'GIT_IMPORT_RESOURCE_TYPE': (0, 'Тип ресурса для импортированных из гита'),
    'GIT_DEFAULT_USER': ('JleMyP', 'Пользователь гита по умолчанию'),
    'CHROME_IMPORT_TAG': (0, 'Метка для ресурсов, импортированных из Chrome'),
    'CHROME_IMPORT_RESOURCE_TYPE': (0, 'Тип ресурса для импортированных из Chrome'),
}
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
