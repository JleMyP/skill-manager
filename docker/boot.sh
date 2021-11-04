#!/bin/bash

set -ex

if [ "$1" = 'update' ]; then
  exec python manage.py migrate
elif [ "$1" = 'server' ]; then
  exec python main.py
elif [ "$1" = 'scheduler' ]; then
  exec python manage.py scheduler
elif [ "$1" = 'worker' ]; then
  exec python manage.py worker
else
  exec $@
fi
