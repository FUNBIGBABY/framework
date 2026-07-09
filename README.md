# Personal AI Framework Studio

A personal-use application for creating, editing, publishing, merging, and exporting expert evaluation frameworks with AI assistance.

This repository is in the middle of a staged migration from a legacy customer project to a personal AI Agent + LLMWiki + RAG architecture. The canonical migration plan and execution records are:

- `MIGRATION_PHASES.md`
- `docs/migration/README.md`
- `docs/migration/phases/`

Historical migration records are retained for audit evidence. Current setup and operation should follow this README and the migration docs above.

## Current Boundaries

- Personal-use app by default.
- Public registration is disabled by default.
- Users are created by an administrator or allowed through `ALLOWED_EMAILS`.
- Backend JWT cookie sessions are the current auth boundary.
- DeepSeek is the default LLM provider route.
- Postgres with pgvector is the current database target.
- Legacy local/Ollama/GCP LLM code is disabled unless `ENABLE_LEGACY_LLM=true` is set intentionally.
- Browser smoke for the Phase 6/7 migration remains deferred until Docker/Postgres and seeded local credentials are available.

Removed customer-specific setup paths are not current setup paths.

## Requirements

- Node.js 22.12.0 or newer
- Python 3.11 or newer
- Docker, if running the compose stack
- A DeepSeek API key for real LLM calls
- Postgres/pgvector for the current backend database path

## Environment

Start from the templates:

```bash
cp .env.example .env
cp backend_py/.env.example backend_py/.env
cp frontend/.env.example frontend/.env
```

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

## Local Development

Install frontend dependencies and start Vite:

```bash
cd frontend
npm install
npm run dev
```

Install backend dependencies and start FastAPI:

```bash
cd backend_py
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The frontend defaults to `http://localhost:5173`. The backend defaults to `http://localhost:8000`.

Seed the personal super-admin after configuring backend env and database access:

```bash
cd backend_py
python scripts/seed_admin.py
```

## Docker

The compose stack provides Postgres/pgvector and the app container:

```bash
docker compose up --build
```

The app is exposed on `http://localhost:8000`. The compose defaults use neutral `framework` database/user names. Existing local volumes created with older defaults may need explicit compatibility env values or an intentional volume reset after backing up any needed data.

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

Phase 8+ features such as the Agent loop, Tool Registry, Chat UI, RAG retrieval, LLMWiki, and MCP-compatible adapter are planned migration work and should not be claimed as complete from the current README.
