#!/usr/bin/env python

import os

import uvicorn

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    listen = os.environ.get('LISTEN', '0.0.0.0')  # noqa: S104
    uvicorn.run(
        'conf.asgi:application',
        host=listen,
        port=port,
        loop='uvloop',
        lifespan='off',
    )
