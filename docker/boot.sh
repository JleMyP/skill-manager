#!/bin/bash

set -e

if [ "$1" = 'update' ]; then
  python manage.py migrate
  python manage.py collectstatic
elif [ "$1" = 'server' ]; then
  exec python main.py
elif [ "$1" = 'scheduler' ]; then
  exec python manage.py scheduler
elif [ "$1" = 'worker' ]; then
  exec python manage.py worker
else
  exec $@
fi
