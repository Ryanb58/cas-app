DOCKER_COMPOSE=docker-compose -f dev.yml

build:
	$(DOCKER_COMPOSE) build

rebuild:
	$(DOCKER_COMPOSE) build --no-cache

run:
	$(DOCKER_COMPOSE) up

up: run

clean:
	$(DOCKER_COMPOSE) down

auth-migrations:
	(DOCKER_COMPOSE) run auth python3 manage.py makemigrations

auth-migrate:
	(DOCKER_COMPOSE) run auth python3 manage.py migrate
