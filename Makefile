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

