#!/bin/bash

docker-compose \
  -p skill-manager \
  --project-dir $(pwd) \
  --env-file src/conf/settings/.env \
  -f docker/docker-compose.local.yml \
  $@
