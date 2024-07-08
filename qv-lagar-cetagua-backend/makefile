.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: up
up: ## run the project
	@make stop
	@docker compose up -d
	@make log

.PHONY: ps
ps: ## ps command
	@docker compose ps

.PHONY: stop
stop: ## stop Docker containers without removing them
	@docker compose stop

.PHONY: rebuild
rebuild: ## rebuild base Docker images
	@docker compose down --remove-orphans
	@docker compose build --no-cache
	@make up


.PHONY: reset
reset: ## update Docker images and reset local databases
	@docker compose down --volumes --remove-orphans
	@docker system prune -a
	@make up

.PHONY: pull
pull: ## update Docker images without losing local databases
	@docker compose down --remove-orphans
	@docker compose pull

.PHONY: bash
bash: ## open bash into project directory
	@docker exec -it cetagua-backend bash

.PHONY: log
log: ## get only log of the django project
	@docker logs --tail 200 -f cetagua-backend

.PHONY: logs
logs: ## get logs of all project
	@docker compose logs --tail 200 -f


.PHONY: fromscratch 
fromscratch: reset pull up