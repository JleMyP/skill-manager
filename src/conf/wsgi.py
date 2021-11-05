import os

from django.core.wsgi import get_wsgi_application
from serverless_wsgi import handle_request

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
application = get_wsgi_application()


def handler(event: dict, context: dict) -> dict:
    path = event['path']
    for key, value in event['pathParams'].items():
        path = path.replace('{' + key + '}', value)
    if not path.endswith('/'):
        path += '/'
    event['path'] = path
    return handle_request(application, event, context)
