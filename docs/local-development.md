# Local Development Guide

## Commands

We provide a `Makefile` for convenience (if you have `make` installed):

- `make build` - Build all Docker containers
- `make up` - Start all services
- `make down` - Stop all services
- `make logs` - View logs
- `make migrate` - Run database migrations
- `make seed` - Seed the database with demo data
- `make test` - Run backend tests

## Frontend Development

The frontend is built with Vite and React.
- Runs on port 3000
- Hot-reloads on file changes
- API requests to `/api/*` are proxied to the backend

## Backend Development

The backend is built with FastAPI and SQLAlchemy.
- Runs on port 8000
- Auto-reloads on file changes
- Accessible at `http://localhost:8000/docs` for API interaction
