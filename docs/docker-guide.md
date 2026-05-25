# Docker Guide

NutriTrack360 uses Docker and Docker Compose to provide a consistent development and production environment.

## Services Overview

The `docker-compose.yml` defines the following services:

1. **frontend**: The React application, served via Vite for development or Nginx in production.
2. **backend**: The FastAPI application running via Uvicorn.
3. **postgres**: The PostgreSQL database.
4. **redis**: The Redis instance used for caching and rate limiting.

## Common Commands

- Start all services: `docker compose up -d`
- Stop all services: `docker compose down`
- Rebuild images: `docker compose up --build`
- View logs for a specific service: `docker compose logs -f backend`
- Execute a command inside a container: `docker compose exec backend bash`

## Database Management via Docker

Run Alembic migrations:
```bash
docker compose exec backend alembic upgrade head
```

Seed the database:
```bash
docker compose exec backend python -m app.scripts.seed
```
