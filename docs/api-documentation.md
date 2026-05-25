# API Documentation

NutriTrack360 uses FastAPI, which automatically generates OpenAPI (Swagger) documentation.

## Accessing the Documentation

When the backend is running, access the documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Authentication

The API uses JWT Bearer authentication. 
1. Call `POST /api/v1/auth/login` to get an `access_token`.
2. Include the token in the `Authorization` header as `Bearer <token>` for subsequent requests.

## Core Endpoints

- `POST /api/v1/auth/login` - Authenticate user
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/challenges` - List organization challenges
- `POST /api/v1/activities` - Log a wellness activity
- `GET /api/v1/analytics/dashboard` - Get HR analytics (Admin only)
