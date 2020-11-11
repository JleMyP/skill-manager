import os

from django.core.wsgi import get_wsgi_application
from serverless_wsgi import handle_request


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
application = get_wsgi_application()


def handler(event: dict, context: dict):
    path = event['path']
    for k, v in event['pathParams'].items():
        path = path.replace('{' + k + '}', v)
    if not path.endswith('/'):
        path += '/'
    event['path'] = path
    print(path)
    return handle_request(application, event, context)
