.PHONY: help up down build logs backend-shell frontend-shell db-shell migrate seed clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services
	docker compose up -d

up-build: ## Build and start all services
	docker compose up --build -d

down: ## Stop all services
	docker compose down

down-clean: ## Stop all services and remove volumes
	docker compose down -v

build: ## Build all services
	docker compose build

logs: ## View logs for all services
	docker compose logs -f

logs-backend: ## View backend logs
	docker compose logs -f backend

logs-frontend: ## View frontend logs
	docker compose logs -f frontend

backend-shell: ## Open a shell in the backend container
	docker compose exec backend bash

frontend-shell: ## Open a shell in the frontend container
	docker compose exec frontend sh

db-shell: ## Open psql in the database container
	docker compose exec postgres psql -U nutritrack -d nutritrack360

redis-cli: ## Open redis-cli
	docker compose exec redis redis-cli

migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MSG="migration message")
	docker compose exec backend alembic revision --autogenerate -m "$(MSG)"

seed: ## Seed database with sample data
	docker compose exec backend python -m app.scripts.seed

test-backend: ## Run backend tests
	docker compose exec backend pytest -v

lint-backend: ## Lint backend code
	docker compose exec backend ruff check app/

clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all --remove-orphans
