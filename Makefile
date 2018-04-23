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

.PHONY: debug
debug: ## Runs a docker service with service ports turned on (for ipdb to work).
ifdef SERVICE
		${DOCKERCOMPOSE_DEV} kill $(SERVICE)
		${DOCKERCOMPOSE_DEV} run --service-ports $(SERVICE)
else
		@echo "Please define SERVICE environment/make variable. Example:"
		@echo
		@echo "SERVICE=web make debug"
		@echo
		@echo "-- or --"
		@echo
		@echo "make debug SERVICE=web"
		@echo
endif
