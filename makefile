#!make

SHELL := /bin/bash
.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


########################################################################################
# Docker-compose targets
########################################################################################
DOCKER_DEV := COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose --project-directory docker -f docker/dev-docker-compose.yml
DOCKER_ENV_ARGS := $(shell < docker/.env xargs)

format:
	black . && isort .

build:
	$(DOCKER_DEV) build api tests

tests_docker: build
	$(DOCKER_DEV) run tests

tests_locally:
	cd tests && \
	$(DOCKER_ENV_ARGS) \
	pytest -s integration

run_locally:
	$(DOCKER_ENV_ARGS) \
	POSTGRES_HOST=localhost \
	uvicorn api.flights_api.api_endpoints:app --reload --port 8000

up: build
	$(DOCKER_DEV) up --remove-orphans api
