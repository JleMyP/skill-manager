SHELL = /bin/bash

DOCKER_TAG ?= skill-manager


.PHONY: build-dev build-prod build-prod-alpine
build-prod: DOCKERFILE_SUFFIX = .prod
build-prod-alpine: DOCKERFILE_SUFFIX = .prod.alpine
build-dev build-prod build-prod-alpine:
	DOCKER_BUILDKIT=1 docker -f docker/Dockerfile${DOCKERFILE_SUFFIX} build -t ${DOCKER_TAG} .

.PHONY: run
run: # dev server
	cd src && python manage.py runserver_plus 0.0.0.0:8000

.PHONY: shell
shell: # django shell
	cd src && python manage.py shell_plus --quiet-load

shell-sql:
	cd src && python manage.py shell_plus --quiet-load  --print-sql

lint:
	flakehell lint src --count --exit-zero
