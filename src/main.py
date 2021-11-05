#!/usr/bin/env python

import os

import uvicorn
from uvicorn.config import LOGGING_CONFIG


def health_check(record: any) -> bool:
    return not record.scope['path'].startswith('/ht')


_LOGGING_CONFIG = LOGGING_CONFIG.copy()
_LOGGING_CONFIG['filters'] = {
    'skip_health_check': {
        '()': 'django.utils.log.CallbackFilter',
        'callback': health_check,
    },
}
_LOGGING_CONFIG['loggers']['uvicorn.access'] = {
    **LOGGING_CONFIG['loggers']['uvicorn.access'],
    'filters': ['skip_health_check'],
}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    listen = os.environ.get('LISTEN', '0.0.0.0')  # noqa: S104
    uvicorn.run(
        'conf.asgi:application',
        host=listen,
        port=port,
        loop='uvloop',
        lifespan='off',
        log_config=_LOGGING_CONFIG,
    )
