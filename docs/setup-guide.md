# Setup Guide

## Requirements
- Docker and Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.12+ (for local backend dev)

## Quick Start (Docker)

The fastest way to get started is using Docker Compose:

1. Clone the repository
2. Run `docker compose up --build`
3. In a separate terminal, seed the database:
   `docker compose exec backend python -m app.scripts.seed`

## Manual Setup

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`
6. Start PostgreSQL and Redis locally
7. `alembic upgrade head`
8. `python -m app.scripts.seed`
9. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. Copy `.env.example` to `.env`
4. `npm run dev`
