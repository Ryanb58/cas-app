DOCKERCOMPOSE=docker-compose -f dev.yml

build:
	$(DOCKERCOMPOSE) build

run:
	$(DOCKERCOMPOSE) up

up: run

clean:
	$(DOCKERCOMPOSE) down

