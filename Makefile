SHELL = /bin/bash

.PHONY: help up in down build bash freeze pytest

.DEFAULT_GOAL := help up down build bash env-file setup


help: ## Show this help message
	@echo "Available targets:"
	@grep -E '(^[a-zA-Z_-]+:.*?##|^# [A-Za-z])' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	/^# / {printf "\n%s\n", substr($$0, 3); next} \
	{printf "  %-20s %s\n", $$1, $$2}'

up:  ## Start containers
	docker compose -f docker-compose.yaml up -d

in:  ## Open a bash shell in started cli service
	docker compose -f docker-compose.yaml exec -it cli bash


down:  ## Remove containers
	docker compose -f docker-compose.yaml down


build:  ## Build image
	docker compose -f docker-compose.yaml build


bash:  ## Open a bash shell in cli service
	docker compose -f docker-compose.yaml run --rm -it cli bash


freeze:  ## Run pip freeze (requirements.txt)
	pip freeze | grep -v "bt_cli" > requirements.txt

pytest:  ## Run pytest
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/code cli /bin/bash -c "python -m pytest"

env-file: ## Create an .env file based on .env.example
	cp .env.example .env


setup:
	@echo "🔧 Setting up environment..."
	@$(MAKE) env-file
	echo "✅ Copied .env.example → .env";

	@read -p "Enter your DATABENTO_API_KEY (or ENTER to leave blank): " key; \
	if [ ! -z "$$key" ]; then \
		sed -i.bak "s|^DATABENTO_API_KEY=.*|DATABENTO_API_KEY=$$key|" .env || echo "DATABENTO_API_KEY=$$key" >> .env; \
		rm -f .env.bak; \
		echo "✅ API key saved to .env"; \
	else \
		echo "⚠️  No API key entered, continuing setup."; \
	fi
	@echo "🚀 Creating image and starting containers"
	@$(MAKE) build
	@$(MAKE) up
	@echo "⚡ Containers started, starting bash shell"
	docker compose -f docker-compose.yaml exec -it cli bash -c "echo '✅ Setup finished! Command to access the CLI: bt'; bash"
