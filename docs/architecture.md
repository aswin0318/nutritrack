# System Architecture

## Overview

NutriTrack360 is designed as a modular monolith, separating the frontend and backend into distinct services that communicate over REST APIs.

## Components

### 1. Frontend (React SPA)
- **Framework**: React 18, Vite
- **State**: Zustand (global), React Query (server state caching)
- **Styling**: TailwindCSS, Shadcn UI patterns
- **Deployment**: Nginx serving static files

### 2. Backend (FastAPI)
- **Framework**: FastAPI (Python 3.12)
- **Architecture**: 
  - `Routes` (HTTP handling) -> `Services` (Business logic) -> `Repositories` (Data access)
- **Database**: PostgreSQL with asyncpg (SQLAlchemy 2.0)
- **Caching/Rate Limiting**: Redis

### 3. Data Model (Key Entities)
- **User/Organization**: Multi-tenant structure (one organization per deployment currently)
- **Challenges/Events**: Engagement mechanisms
- **Rewards**: Gamification and points redemption
- **Activities**: Tracking user compliance

## Security

- **RBAC**: Super Admin, HR Admin, Department Manager, Employee
- **Authentication**: Stateless JWTs
- **Passwords**: bcrypt hashing
