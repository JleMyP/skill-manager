#!/bin/bash

docker compose \
  -p skill-manager \
  --project-directory $(pwd) \
  --env-file src/conf/settings/.env \
  -f docker/local.yml \
  $@
