# NutriTrack360 Implementation Steps

## End-to-End Project Implementation Plan

This document provides the complete, step-by-step implementation plan for building NutriTrack360 from scratch.

---

## Phase 1: Project Foundation

### 1.1 Repository Setup
- Initialize Git repository
- Create `.gitignore` for Python, Node, Docker, IDE files
- Set up branch protection rules (main, develop)
- Create `Makefile` with common dev commands

### 1.2 Backend Scaffolding
- Create Python project structure (`backend/app/`)
- Set up `requirements.txt` with all pinned dependencies
- Create `app/config.py` with Pydantic Settings (env-based)
- Create `.env.example` with all configuration variables
- Configure structured logging with `structlog`

### 1.3 Frontend Scaffolding
- Scaffold with Vite + React + TypeScript template
- Install TailwindCSS 3 + PostCSS + Autoprefixer
- Install Shadcn UI primitives (Radix components)
- Install React Router, React Query, Zustand, Framer Motion, Recharts
- Set up path aliases (`@/` -> `src/`)
- Configure `tsconfig.json` for strict TypeScript

---

## Phase 2: Database Architecture

### 2.1 SQLAlchemy Models
Create all models with proper relationships, indexes, and constraints:

| Model | Purpose |
|-------|---------|
| Organization | Top-level tenant |
| User | Core identity with RBAC |
| Role | Role definitions |
| Permission | Permission definitions |
| RolePermission | Role-permission mapping |
| Department | Org departments with managers |
| Challenge | Team/individual challenges |
| ChallengeParticipation | User challenge enrollment |
| Event | Corporate wellness events |
| EventRegistration | Event sign-ups |
| Reward | Reward catalog items |
| UserReward | Earned/redeemed rewards |
| Achievement | Badge definitions |
| UserAchievement | Unlocked badges |
| ActivityLog | Daily activity tracking |
| WellnessProgram | Org wellness programs |
| WellnessGoal | Individual goals |
| Notification | User notifications |
| AuditLog | System audit trail |

### 2.2 Database Features
- UUID primary keys on all tables
- `created_at` / `updated_at` timestamps (auto-managed)
- Soft delete support (`deleted_at`, `is_deleted`)
- Foreign key constraints with appropriate ON DELETE behavior
- Indexes on frequently queried columns
- JSONB columns for flexible settings/metadata

### 2.3 Alembic Migrations
- Configure async Alembic with `env.py`
- Generate initial migration from models
- Support for `alembic upgrade head` and `alembic downgrade`

---

## Phase 3: Authentication & Security

### 3.1 JWT Authentication
- `create_access_token()` with user ID, role, org ID claims
- `create_refresh_token()` for session continuity
- `create_password_reset_token()` for forgot-password flow
- Token expiry: access (30 min), refresh (7 days), reset (1 hour)
- bcrypt password hashing via `passlib`

### 3.2 RBAC (Role-Based Access Control)
Four system roles with hierarchical permissions:
1. **Super Admin** — Full system access
2. **HR Admin** — HR management, analytics, user management
3. **Department Manager** — Department scope, challenge/event creation
4. **Employee** — Personal dashboard, challenge participation, events

### 3.3 Security Middleware
- CORS configuration with whitelisted origins
- Security headers (HSTS, XSS Protection, Content-Type-Options)
- Rate limiting via `slowapi` backed by Redis
- Request/response logging with request IDs
- Input validation and sanitization

---

## Phase 4: Backend API Layer

### 4.1 Repository Pattern
- Generic `BaseRepository` with CRUD, pagination, filtering, sorting
- Specialized repositories for each entity
- Async database operations throughout
- Soft delete support where appropriate

### 4.2 Service Layer
- `AuthService` — Login, register, refresh, password reset
- `UserService` — Profile management, org-scoped queries
- `ChallengeService` — Create, join, leaderboard, participation
- `EventService` — Create, register, capacity management
- `RewardService` — Catalog, redemption, points tracking
- `ActivityService` — Log activities, calculate points, summaries
- `AnalyticsService` — Dashboard stats, trends, department engagement
- `OrganizationService`, `DepartmentService`, `NotificationService`

### 4.3 API Routes (`/api/v1/`)
All endpoints follow RESTful conventions with:
- Proper HTTP methods and status codes
- Pagination (page, page_size)
- Filtering and search
- Sorting (sort_by, sort_order)
- Validation via Pydantic schemas
- Error handling with structured responses
- Swagger/OpenAPI documentation

---

## Phase 5: Frontend Architecture

### 5.1 Design System
- TailwindCSS with CSS variable tokens (Shadcn approach)
- Light and dark theme support via `class` strategy
- Custom color palette (primary blue, semantic colors)
- Inter font family from Google Fonts
- Custom scrollbar styling
- Glass-morphism utility classes

### 5.2 State Management
- `useAuthStore` (Zustand) — Auth state, login/logout, token management
- `useThemeStore` — Light/dark mode with localStorage persistence
- `useUIStore` — Sidebar open/collapsed state
- React Query for server state (API data caching)

### 5.3 Routing
- React Router v7 with nested routes
- Protected route wrapper (redirects unauthenticated users)
- App layout with sidebar + topbar wrapper
- Public routes: login, signup, forgot-password
- Protected routes: dashboard, challenges, events, rewards, analytics, admin, profile

### 5.4 API Integration
- Axios instance with base URL and auth interceptor
- Automatic token attachment to all requests
- Token refresh on 401 responses
- Redirect to login on auth failure

---

## Phase 6: Frontend Pages

### 6.1 Authentication Pages
- **Login** — Split layout with branded gradient panel, email/password form, demo credentials
- **Signup** — Full registration form with organization name
- **Forgot Password** — Email submission with confirmation state

### 6.2 Employee Dashboard
- Welcome greeting with user name
- Stats grid (wellness score, points, challenges, events)
- Activity overview area chart (Recharts)
- Challenge progress bars with animation
- Recent activity feed
- Upcoming events list
- Team wellness rankings

### 6.3 Challenges
- Filterable card grid (all/active/draft/completed)
- Search by title
- Challenge cards with status badges, participant counts, rewards
- Create challenge button (Manager+)

### 6.4 Events
- Event cards with type badges, location, capacity bar
- Registration buttons
- Virtual event link support

### 6.5 Rewards
- Points summary (available, earned, redeemed)
- Achievement badges (unlocked/locked)
- Reward catalog grid with category icons
- Redeem buttons with point validation

### 6.6 HR Analytics (Admin)
- Top-level stats with change indicators
- Participation trends area chart
- Department engagement bar chart
- Challenge completion donut chart
- Event attendance grouped bar chart

### 6.7 Admin Panel
- **User Management** — Searchable table with role badges and status indicators
- **Departments** — Card grid with manager, employee count, wellness score
- **Settings** — General, wellness, notification, and security configuration forms
- **Audit Logs** — Searchable table with action badges and timestamps

### 6.8 Profile
- Avatar with initials
- Editable personal information form
- Read-only work information

---

## Phase 7: Docker & Infrastructure

### 7.1 Docker Setup
- `backend/Dockerfile` — Python 3.12 slim, non-root user, uvicorn
- `frontend/Dockerfile` — Node 20 Alpine, dev server
- `docker-compose.yml` — 4 services (frontend, backend, postgres, redis)
- Health checks on postgres and redis
- Volume mounts for hot-reload development

### 7.2 Nginx Configuration (Production)
- SPA routing (try_files → index.html)
- Static asset caching (1 year, immutable)
- API reverse proxy to backend
- Security headers
- Gzip compression

### 7.3 AWS Deployment Architecture
- Region: us-east-1, 2 AZs
- VPC with 6 subnets (2 public, 2 private app, 2 private DB)
- Internet-facing ALB for frontend + API routing
- Internal ALB for backend services
- EC2 Auto Scaling Groups in private subnets
- RDS PostgreSQL Multi-AZ in private DB subnets
- ElastiCache Redis for session/caching
- Route53 for DNS (nutritrack360.in)
- ACM for TLS certificates
- Bastion host in separate VPC with VPC peering

---

## Phase 8: Quality & Polish

### 8.1 Dark/Light Mode
- CSS variable-based theming
- Seamless toggle in topbar
- localStorage persistence
- All components theme-aware

### 8.2 Animations
- Framer Motion page transitions
- Staggered card animations
- Progress bar animations
- Hover effects on interactive elements
- Loading spinner animations

### 8.3 Responsive Design
- Mobile-first approach
- Collapsible sidebar on desktop
- Hidden sidebar on mobile with hamburger menu
- Responsive grid layouts (1 → 2 → 4 columns)
- Mobile-optimized forms and tables

### 8.4 Error & Loading States
- Loading skeletons on data-fetching pages
- Empty state placeholders
- Error message displays
- Form validation feedback
- Toast notifications

---

## Verification Checklist

- [ ] `docker compose up --build` starts all 4 services cleanly
- [ ] Backend health check at `/health` returns 200
- [ ] Frontend loads at `http://localhost:3000`
- [ ] API docs accessible at `http://localhost:8000/docs`
- [ ] Database seeded via `make seed`
- [ ] Login with demo credentials works
- [ ] Dark/light mode toggles correctly
- [ ] Sidebar navigation works for all pages
- [ ] Charts render on analytics page
- [ ] Tables render on admin pages
- [ ] Forms validate input properly
- [ ] RBAC restricts admin routes for employees
- [ ] Responsive layout works on mobile viewport
