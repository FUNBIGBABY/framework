# Personal AI Framework Studio

A personal-use application for creating, editing, publishing, merging, and exporting expert evaluation frameworks with AI assistance.

This repository is in the middle of a staged migration from a legacy customer project to a personal AI Agent + LLMWiki + RAG architecture. The canonical migration plan and execution records are:

- `MIGRATION_PHASES.md`
- `docs/migration/README.md`
- `docs/migration/REVIEW_LEDGER.md`
- `docs/migration/phases/`

`MIGRATION_PHASES.md` remains the canonical plan. The review ledger indexes verdict/acceptance status only, and phase reports remain historical evidence. Current setup and operation should follow this README and the migration docs above.

## Current Boundaries

- Personal-use app by default.
- Public registration is disabled by default.
- Users are created by an administrator or allowed through `ALLOWED_EMAILS`.
- Backend JWT cookie sessions are the current auth boundary.
- DeepSeek is the default LLM provider route.
- Postgres with pgvector is the current backend database path; SQLite is not a supported substitute for the current schema.
- Legacy local/Ollama/GCP LLM code is disabled unless `ENABLE_LEGACY_LLM=true` is set intentionally.
- Phase 6/7 browser smoke is recorded as `not run`. The historical environment blocker was an unavailable Docker Desktop Linux engine plus no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded credentials; the current Compose app path also has the Node-builder incompatibility documented below. Missing browser smoke is not automatically a blocker when a named reviewer records an explicit documented deferral, owner, and trigger.

Removed customer-specific setup paths are not current setup paths.

## Authentication Contract

- `POST /api/users/login` establishes a 1h access cookie and a 30d refresh cookie.
- Both cookies are `httpOnly`; `Secure` is set when `ENV` / `APP_ENV` declares production or `AUTH_COOKIE_SECURE` is truthy, and `SameSite=Lax` is the default.
- Session restore uses `/api/users/me`; `/api/users/refresh` reissues the session cookies, and `/api/users/logout` clears them and revokes the current refresh-session version when possible.
- The frontend stores no auth token in `localStorage` or `sessionStorage` and sends private requests with `credentials: "include"`.
- Protected routes accept the access cookie only and reject `Authorization: Bearer` as a protected-route credential.
- Cookie-authenticated unsafe methods require an allowed Origin or Referer.

## Requirements

- Node.js 22.12.0 or newer
- Python 3.11 or newer
- Docker, if running the compose stack
- A DeepSeek API key for real LLM calls
- Postgres/pgvector for the current backend database path

## Environment

Use the templates as a variable inventory, but keep the host and Compose paths separate. For Compose substitution, create the repository-root file:

```powershell
Copy-Item .env.example .env
```

For a host-run backend, export a host-reachable `DATABASE_URL` in the process as shown below; the root template's `db:5432` hostname is Compose-only and wins over `backend_py/.env` when both files exist. The seed script does not load either file. Do not create `backend_py/.env` before a Docker build: the current `.dockerignore` does not exclude it and the current Dockerfile copies `backend_py/` into the image. Frontend `.env` files must contain public `VITE_*` values only.

Important variables:

- `JWT_SECRET_KEY`: required backend signing secret.
- `DATABASE_URL`: SQLAlchemy database URL.
- `SUPER_ADMIN_EMAIL`: configured super-admin identity.
- `SUPER_ADMIN_PASSWORD`: password used by the admin seed script.
- `ALLOWED_EMAILS`: comma-separated registration allowlist.
- `ENABLE_PUBLIC_REGISTER=false`: default public-registration guard.
- `LLM_PROVIDER=deepseek`: default provider.
- `DEEPSEEK_API_KEY`: required for real DeepSeek calls.
- `DEEPSEEK_BASE_URL=https://api.deepseek.com`: do not append `/v1`.
- `APP_NAME` and `VITE_APP_NAME`: app display name.
- `APP_BASE_DOMAIN`, `FRONTEND_URL`, and `VITE_API_BASE_URL`: deployment routing and CORS configuration.
- `ENV=production` / `APP_ENV=production` or truthy `AUTH_COOKIE_SECURE`: enables `Secure`; `AUTH_COOKIE_SAMESITE` is clamped to `lax` or `strict`.

## Local Development

Install frontend dependencies and start Vite:

```bash
cd frontend
npm install
npm run dev
```

Install backend dependencies, export process environment, then migrate, seed, and start FastAPI:

```powershell
cd backend_py
python -m pip install -r requirements.txt
$env:DATABASE_URL = 'postgresql+psycopg://framework:<password>@localhost:5432/framework'
$env:JWT_SECRET_KEY = '<strong-signing-secret>'
$env:SUPER_ADMIN_EMAIL = 'you@example.com'
$env:SUPER_ADMIN_PASSWORD = '<set-a-strong-password>'
alembic -c alembic.ini upgrade head
python scripts/seed_admin.py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The required order is Postgres/pgvector available → environment loaded → Alembic upgraded → admin seeded → Uvicorn started. `seed_admin.py` reads process environment directly, so make `DATABASE_URL`, `JWT_SECRET_KEY`, `SUPER_ADMIN_EMAIL`, and `SUPER_ADMIN_PASSWORD` available to that process. See `backend_py/SETUP.md` for host and Compose variants.

The frontend defaults to `http://localhost:5173`. The backend defaults to `http://localhost:8000`.

## Docker

The Compose file declares Postgres/pgvector and the app container, but the app image is not currently a verified runnable path: `Dockerfile` uses Node 18 while the locked Vite 7.1.9 requires Node `^20.19.0 || >=22.12.0` and React Router 7.9.3 requires Node `>=20.0.0`. `docker compose build app` is therefore a static blocker until the Container Runtime Owner supplies and reviews a compatible runtime change. After that trigger, the intended order is:

```powershell
docker compose build app
docker compose up -d --wait --wait-timeout 120 db
docker compose run --rm --entrypoint alembic app -c alembic.ini upgrade head
$env:SUPER_ADMIN_PASSWORD = '<set-a-strong-password>'
docker compose run --rm -e SUPER_ADMIN_PASSWORD --entrypoint python app scripts/seed_admin.py
docker compose up -d --wait --wait-timeout 180 app
Invoke-WebRequest -UseBasicParsing http://localhost:8000/health
```

`docker compose up --wait` must report the database healthy before Alembic and the app healthy before `/health`; a timeout is a failure, not readiness. This sequence was not run by the remediation and is not Docker, live-PostgreSQL, or endpoint evidence. The intended app endpoint is `http://localhost:8000`. Compose does not automatically run Alembic or seed the administrator. Its `db` service is not published on the host, so a host-run Uvicorn process needs a separately reachable Postgres/pgvector instance or an explicitly authorized port override. The compose defaults use neutral `framework` database/user names. Existing local volumes created with older defaults may need explicit compatibility values or an intentional, backed-up reset. The supplied Compose environment also does not map `ENV` / `APP_ENV`, `AUTH_COOKIE_*`, `ALLOWED_EMAILS`, or `ENABLE_PUBLIC_REGISTER`; a root `.env` entry alone does not inject an unmapped variable. Treat this as a local contract, not a production deployment recipe.

## Tests And Checks

Use targeted checks for the files you change. Common commands:

```bash
cd frontend
npm run lint
npm test
npm run build
```

```bash
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

```bash
git diff --check
```

Do not treat obsolete top-level backend helper scripts as test coverage. Maintained backend tests live under `backend_py/tests/`.

## Project Layout

```text
frontend/                         React + Vite frontend
  src/components/                 UI components
  src/contexts/                   Auth and app context
  src/lib/                        API and app config helpers

backend_py/                       FastAPI backend
  app/api/                        API route modules
  app/services/                   Provider and business services
  app/models.py                   SQLAlchemy models
  scripts/seed_admin.py           Admin account seed utility
  tests/                          Maintained backend pytest tests

docs/migration/                   Migration entry point and phase records
docs/PERSONAL_USE_BOUNDARY.md     Personal-use boundary
docker-compose.yml                Local compose stack
```

## Current Features

- Backend-cookie authenticated personal framework list.
- Framework creation from text or file.
- Framework editing, local draft handling, and artefact child-resource UI.
- Library publish/unpublish flow for authenticated users.
- Admin user management for the configured super-admin.
- Markdown and DOCX export.
- Provider abstraction with DeepSeek as the current default LLM route.

Phase 8+ features such as the Agent loop, Tool Registry, Chat UI, RAG retrieval, LLMWiki, and MCP-compatible adapter are planned and not implemented. Phase 8 planning is also gated by the canonical dependency/review rules; this roadmap is not authorization to start it.
