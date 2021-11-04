#!/bin/bash

set -ex

poetry export -f requirements.txt --without-hashes -o requirements.txt
zip func -r src \
  -x static/\* \
  -x _storage/\* \
  -x \*/__pycache__/\*
yc serverless function version create \
  --function-name skill-manager \
  --runtime python37-preview \
  --entrypoint conf.wsgi.handler \
  --memory 256m \
  --execution-timeout 3s \
  --source-path func.zip \
  --environment S3_SECRET_ACCESS_KEY="$S3_SECRET_ACCESS_KEY" \
  --environment S3_ACCESS_KEY_ID="$S3_ACCESS_KEY_ID" \
  --environment DATABASE_URL="$DATABASE_URL"

rm func.zip
rm requirements.txt
