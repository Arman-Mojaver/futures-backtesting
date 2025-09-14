SHELL = /bin/bash

.PHONY: help up down build bash freeze

.DEFAULT_GOAL := help up down build bash


help: ## Show this help message
	@echo "Available targets:"
	@grep -E '(^[a-zA-Z_-]+:.*?##|^# [A-Za-z])' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	/^# / {printf "\n%s\n", substr($$0, 3); next} \
	{printf "  %-20s %s\n", $$1, $$2}'

up:  ## Start containers
	docker compose -f docker-compose.yaml up -d


down:  ## Remove containers
	docker compose -f docker-compose.yaml down


build:  ## Build image
	docker compose -f docker-compose.yaml build


bash:  ## Open a bash shell in web service
	docker compose -f docker-compose.yaml run --rm -it cli bash


freeze:  ## Run pip freeze (requirements.txt)
	pip freeze | grep -v "bt_cli" > requirements.txt
