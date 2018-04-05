DOCKERCOMPOSE=docker-compose -f dev.yml

build:
	$(DOCKERCOMPOSE) build

