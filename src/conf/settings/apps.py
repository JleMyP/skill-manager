MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
]

MPTT_ADMIN_LEVEL_INDENT = 20


CONSTANCE_CONFIG = {
    'GIT_IMPORT_TAG': (0, 'Метка для ресурсов, импортированных из гита'),
    'GIT_IMPORT_RESOURCE_TYPE': (0, 'Тип ресурса для импортированных из гита'),
    'GITHUB_DEFAULT_USER': ('JleMyP', 'Пользователь гитхаба по умолчанию'),
    'GITHUB_TOKEN': (None, 'Токен гитхаба'),
    'CHROME_IMPORT_TAG': (0, 'Метка для ресурсов, импортированных из Chrome'),
    'CHROME_IMPORT_RESOURCE_TYPE': (0, 'Тип ресурса для импортированных из Chrome'),
}
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


# debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
