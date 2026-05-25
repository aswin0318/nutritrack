# NutriTrack360

**Corporate Wellness & Fitness Compliance Platform**

NutriTrack360 is a production-grade enterprise SaaS application that enables organizations to manage employee wellness programs, team fitness challenges, reward systems, and corporate health events with full HR analytics, RBAC, and audit capabilities.

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite 6
- TailwindCSS 3
- Shadcn UI (Radix primitives)
- React Router 7
- React Query (TanStack)
- Zustand (state management)
- Framer Motion (animations)
- Recharts (analytics charts)
- Lucide React (icons)

### Backend
- Python 3.12 + FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL 16
- Redis 7
- Alembic (migrations)
- Pydantic v2
- JWT Authentication (python-jose)
- bcrypt (password hashing)
- structlog (structured logging)
- slowapi (rate limiting)

### Infrastructure
- Docker + Docker Compose
- Nginx (production reverse proxy)
- AWS-aware architecture (RDS, ALB, Route53, ACM)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Run Locally (or on EC2)

```bash
# Clone the repository
git clone <repository-url>
cd nutritrack360

# Start all services
docker compose up --build -d

# Seed the database (in another terminal)
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.scripts.seed
```

### Access Points
| Service | URL |
|---------|-----|
| Frontend | http://<YOUR_IP>:3000 |
| Backend API | http://<YOUR_IP>:8000 |
| API Docs (Swagger) | http://<YOUR_IP>:8000/docs |

### Demo Credentials
| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@acme.com | Password123! |
| HR Admin | hr@acme.com | Password123! |
| Manager | manager@acme.com | Password123! |
| Employee | employee@acme.com | Password123! |

## Features

- **Authentication**: Login, signup, forgot/reset password, JWT with refresh tokens
- **RBAC**: Super Admin, HR Admin, Department Manager, Employee roles
- **Employee Dashboard**: Wellness score, activity stats, challenge progress, team rankings
- **Team Challenges**: Create, join, leaderboards, analytics
- **Event Management**: Corporate events, registration, capacity tracking
- **Reward System**: Point accumulation, catalog, redemption, achievements
- **HR Analytics**: Participation trends, department engagement, completion rates
- **Admin Panel**: User management, departments, settings, audit logs
- **Dark/Light Mode**: Full theme support with system preference detection

## Documentation

See the [docs/](./docs/) folder for:
- [Setup Guide](./docs/setup-guide.md)
- [Docker Guide](./docs/docker-guide.md)
- [Local Development](./docs/local-development.md)
- [API Documentation](./docs/api-documentation.md)
- [Deployment Guide](./docs/deployment-guide.md)
- [Architecture](./docs/architecture.md)
- [Implementation Steps](./docs/implementation-steps.md)

## License

Proprietary - All rights reserved.