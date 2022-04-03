import logging
import typing
from pathlib import Path
import uuid

import environ
from django.http import HttpRequest, HttpResponse
import structlog

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'very secret key'),
    S3_BUCKET=(str, 'skill-manager'),
    S3_ACCESS_KEY_ID=(str, None),
    S3_SECRET_ACCESS_KEY=(str, None),
    JSON_LOG=(bool, False),
    OTLP_ENDPOINT=(str, None),
)
env.read_env()

BASE_DIR = Path(__file__).parents[2]

ALLOWED_HOSTS = ['*']
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ROOT_URLCONF = 'conf.urls'
WSGI_APPLICATION = 'conf.wsgi.application'
ASGI_APPLICATION = 'conf.asgi.application'

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3'),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'conf.settings.common.TracerWrapper',
    'conf.settings.common.LogRequest',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'conf.settings.common.DisableCSRF',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'loginas',
    'django_extensions',
    'django_filters',
    'autocompletefilter',
    'django_object_actions',
    'django_json_widget',
    'reversion',
    'polymorphic',
    'storages',
    'drf_spectacular',
    'rest_framework',
    'rest_framework_serializer_extensions',
    'markdownx',
    'mptt',
    'debug_toolbar',
    'corsheaders',

    'constance',
    'constance.backends.database',

    'health_check',
    'health_check.db',

    'apps.user',
    'apps.projects',
    'apps.main',
]


class DisableCSRF:
    def __init__(self, get_response: typing.Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request._dont_enforce_csrf_checks = True
        return self.get_response(request)


class LogRequest:
    def __init__(self, get_response: typing.Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.headers.get('x-request-id')
        if not request_id:
            request_id = uuid.uuid4().hex
        span = request.META.get('opentelemetry-instrumentor-django.span_key')
        if span:
            request_id = hex(span.context.trace_id)[2:]
        structlog.threadlocal.bind_threadlocal(request_id=request_id)
        headers = dict(request.headers)
        headers.pop('Authorization', None)
        headers.pop('Cookie', None)
        log = structlog.get_logger().bind()
        log.info(
            'request started',
            headers=headers,
            query=request.GET,
            path=request.path,
            method=request.method,
        )
        response = self.get_response(request)
        response['x-request-id'] = request_id
        log.info('request finished', code=response.status_code)
        return response


class TracerWrapper:
    _tracer_configured = False
    _middleware = None

    def __init__(self, get_response: typing.Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self._prepare_tracer(get_response)
        print(self.__class__._middleware)

    @classmethod
    def _prepare_tracer(cls, get_response: typing.Callable[[HttpRequest], HttpResponse]):
        if cls._tracer_configured:
            return

        cls._tracer_configured = True

        otlp_endpoint = env('OTLP_ENDPOINT')
        if not otlp_endpoint:
            return

        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        span_exporter = OTLPSpanExporter(otlp_endpoint)
        tracer_provider = TracerProvider(
            resource=Resource.create({SERVICE_NAME: 'app.backend'}),
        )
        trace.set_tracer_provider(tracer_provider)
        span_processor = SimpleSpanProcessor(span_exporter)
        tracer_provider.add_span_processor(span_processor)

        from opentelemetry.instrumentation.django.middleware import _DjangoMiddleware
        from opentelemetry.instrumentation.django import get_tracer

        cls._middleware = _DjangoMiddleware(get_response)
        cls._middleware._tracer = get_tracer(__name__)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self.__class__._middleware:
            return self.__class__._middleware.__call__(request)
        return self.get_response(request)


def health_check(record: any) -> bool:
    return not record.scope['path'].startswith('/ht')


def add_uvicorn_scope(logger: any, method: str, event: dict) -> dict:
    rec = event.get('_record')
    if not rec:
        return event
    if rec.name != 'uvicorn.access' or not hasattr(rec, 'scope'):
        return event
    event['method'] = rec.scope['method']
    event['path'] = rec.scope['path']
    return event


processors = [
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.TimeStamper(fmt='iso', utc=True),
    structlog.threadlocal.merge_threadlocal_context,
    add_uvicorn_scope,
]

renderer = structlog.processors.JSONRenderer() if env('JSON_LOG') else structlog.dev.ConsoleRenderer()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'struct_formatter': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': renderer,
            'foreign_pre_chain': processors,
        },
    },
    'filters': {
        'skip_health_check': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': health_check,
        },
    },
    'handlers': {
        'struct': {
            'class': 'logging.StreamHandler',
            'formatter': 'struct_formatter',
        },
    },
    'loggers': {
        '': {
            'handlers': ['struct'],
            'level': 'INFO',
        },
        'django': {'level': 'INFO'},
        'uvicorn': {'level': 'INFO'},
        # server start / stop
        'uvicorn.error': {'level': 'WARNING', 'handlers': ['struct'], 'propagate': False},
        'uvicorn.access': {
            'filters': ['skip_health_check'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

structlog.configure(
    processors=processors + [
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)
