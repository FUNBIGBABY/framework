# Backend Setup

This guide describes the current backend contract. The backend requires PostgreSQL with pgvector and an Alembic-managed schema. SQLite is not a supported substitute for the current JSONB/vector schema.

## 1. Prerequisites

- Python 3.11 or newer.
- PostgreSQL with the pgvector extension available, or Docker for the supplied `pgvector/pgvector:pg16` service.
- A strong `JWT_SECRET_KEY`.
- A DeepSeek API key only when real LLM calls are intentionally run.

Install the complete backend dependency set; do not install only FastAPI/Uvicorn:

```powershell
cd backend_py
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Environment

The backend and Alembic load the repository `.env` and `backend_py/.env` files without overriding an already-set process variable. Keep the host and Compose paths separate. For Compose substitution, create only the repository-root file and replace its placeholders:

```powershell
Copy-Item ..\.env.example ..\.env
```

The root template uses the Compose-only hostname `db:5432`; a host process cannot resolve it. For host Alembic/Uvicorn, export a host-reachable `DATABASE_URL` explicitly as shown in Option B. `scripts/seed_admin.py` reads process environment directly and does not load either `.env` file. Do not create `backend_py/.env` before a Docker build: the current `.dockerignore` does not exclude it and the current Dockerfile copies `backend_py/` into the final image.

Required or important values:

- `DATABASE_URL=postgresql+psycopg://...`: must point to a reachable PostgreSQL/pgvector database.
- `JWT_SECRET_KEY`: required at import time.
- `FRONTEND_URL=http://localhost:5173`: used by credentialed CORS and the cookie Origin/Referer policy.
- `APP_NAME`, `APP_BASE_DOMAIN`: application naming and production-origin configuration.
- `SUPER_ADMIN_EMAIL`: backend-authoritative administrator identity.
- `SUPER_ADMIN_PASSWORD`: required by the seed script.
- `ALLOWED_EMAILS`: exact-email allowlist used if registration is ever explicitly enabled.
- `ENABLE_PUBLIC_REGISTER=false`: keep public registration disabled.
- `ENV=production` / `APP_ENV=production`, or truthy `AUTH_COOKIE_SECURE`: enables the `Secure` cookie flag.
- `AUTH_COOKIE_SAMESITE=lax`: only `lax` or `strict` is accepted; other values are clamped to `lax`.
- `LLM_PROVIDER=deepseek`, `DEEPSEEK_BASE_URL=https://api.deepseek.com`, `DEEPSEEK_API_KEY`: current LLM provider configuration. Do not append `/v1` to the base URL.
- `ENABLE_LEGACY_LLM=false`: keep the legacy local/Ollama/GCP path disabled.

Do not commit `.env` files or real secrets.

## 3. Choose one database/runtime path

### Option A: Compose app + Compose database

This is the intended path that uses the supplied internal `db:5432` hostname. It was not run by this corrective remediation and currently has an exact static build blocker: `Dockerfile` uses `node:18-alpine`, while the locked Vite 7.1.9 requires Node `^20.19.0 || >=22.12.0` and React Router 7.9.3 requires Node `>=20.0.0`. Container Runtime Owner owns the correction; the trigger is a separately reviewed runtime candidate that makes the declared builder compatible. Do not treat the following sequence as run evidence before that blocker is resolved.

From the repository root:

```powershell
docker compose build app
docker compose up -d --wait --wait-timeout 120 db
docker compose run --rm --entrypoint alembic app -c alembic.ini upgrade head
```

`docker compose up --wait` blocks until the database healthcheck passes and returns non-zero on timeout. Do not replace it with plain `up -d`; the current short-form `depends_on` does not establish readiness.

The entrypoint does not run Alembic automatically. Confirm the database is at the repository head before starting the app:

```powershell
docker compose run --rm --entrypoint alembic app -c alembic.ini current
docker compose run --rm --entrypoint alembic app -c alembic.ini heads
```

Seed the administrator. `SUPER_ADMIN_PASSWORD` is deliberately not part of the normal app container environment, so pass it from the current shell without writing it to source:

```powershell
$env:SUPER_ADMIN_PASSWORD = '<set-a-strong-password>'
$env:SEED_ADMIN_RESET_PASSWORD = 'false'
docker compose run --rm -e SUPER_ADMIN_PASSWORD -e SEED_ADMIN_RESET_PASSWORD --entrypoint python app scripts/seed_admin.py
```

Then start the application:

```powershell
docker compose up -d --wait --wait-timeout 180 app
Invoke-WebRequest -UseBasicParsing http://localhost:8000/health
```

The app `/health` request comes only after Compose reports the app container healthy. These commands are an intended sequence, not evidence that Docker, live PostgreSQL, or the endpoint was verified in this remediation.

Compose does not automatically migrate or seed the database. Existing volumes created with old database/user defaults may require explicit compatibility values or an intentional, backed-up local reset. The supplied app environment does not map `ENV` / `APP_ENV`, `AUTH_COOKIE_SECURE`, `AUTH_COOKIE_SAMESITE`, `ALLOWED_EMAILS`, or `ENABLE_PUBLIC_REGISTER`; putting those names in the root `.env` does not inject unmapped variables. The supplied Compose file is therefore not a production deployment recipe.

### Option B: Host Uvicorn + separately reachable PostgreSQL

Use this path only when `DATABASE_URL` reaches a PostgreSQL/pgvector server from the host. Running only `docker compose up -d db` is insufficient because the supplied `db` service has no host `5432` mapping.

Apply Alembic before seed/start:

```powershell
cd backend_py
$env:DATABASE_URL = 'postgresql+psycopg://framework:<password>@localhost:5432/framework'
.\.venv\Scripts\alembic.exe -c alembic.ini upgrade head
$env:DATABASE_URL = 'postgresql+psycopg://framework:<password>@localhost:5432/framework'
.\.venv\Scripts\alembic.exe -c alembic.ini current
$env:DATABASE_URL = 'postgresql+psycopg://framework:<password>@localhost:5432/framework'
.\.venv\Scripts\alembic.exe -c alembic.ini heads
```

The live `current` revision must match `heads`. The initial migration creates the `vector` extension, so the database role must be allowed to create/enable that extension.

`scripts/seed_admin.py` reads process environment directly; it does not load `.env` itself. Export the required values in the same shell before running it:

```powershell
$env:DATABASE_URL = 'postgresql+psycopg://framework:<password>@localhost:5432/framework'
$env:JWT_SECRET_KEY = '<strong-signing-secret>'
$env:SUPER_ADMIN_EMAIL = 'you@example.com'
$env:SUPER_ADMIN_PASSWORD = '<set-a-strong-password>'
$env:SEED_ADMIN_RESET_PASSWORD = 'false'
.\.venv\Scripts\python.exe scripts\seed_admin.py
```

Start Uvicorn only after migration and seed complete:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```powershell
Invoke-WebRequest -UseBasicParsing http://localhost:8000/health
```

## 4. Authentication and CSRF contract

- `POST /api/users/login` sets a 1h access cookie and a 30d refresh cookie.
- Both cookies are `httpOnly`; `Secure` is set when `ENV` / `APP_ENV` declares production or `AUTH_COOKIE_SECURE` is truthy, and `SameSite=Lax` is the default.
- `GET /api/users/me` restores the session. `POST /api/users/refresh` reissues access and refresh cookies without revoking the prior refresh token; `POST /api/users/logout` clears cookies and increments the refresh-session version when the refresh cookie is valid.
- The frontend stores no auth token and must send requests with `credentials: "include"`.
- Protected routes read the access cookie only. `Authorization: Bearer` is rejected as a protected-route credential.
- Cookie-authenticated `POST`, `PUT`, `PATCH`, and `DELETE` requests require an allowed `Origin` or `Referer`. A wrong/missing origin on an authenticated unsafe request returns `403`.
- Public registration remains disabled; use the seed script and admin-only user API.

## 5. Verification order

Run targeted checks first, then the full suite:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m compileall -q app
.\.venv\Scripts\python.exe -m pytest -q tests\test_cookie_sessions.py tests\test_auth_hardening.py tests\test_admin_users.py
.\.venv\Scripts\python.exe -m pytest -q
```

When a migration changes, also run Alembic history/offline generation and an authorized live Postgres upgrade before claiming live migration evidence:

```powershell
$env:DATABASE_URL = 'postgresql+psycopg://framework:<password>@localhost:5432/framework'
.\.venv\Scripts\alembic.exe -c alembic.ini history --verbose
$env:DATABASE_URL = 'postgresql+psycopg://framework:<password>@localhost:5432/framework'
.\.venv\Scripts\alembic.exe -c alembic.ini upgrade head --sql
```

The URL above is a placeholder and must be replaced with an authorized host-reachable PostgreSQL/pgvector endpoint. It is repeated immediately before every host Alembic invocation so a copied command cannot inherit the Compose-only `db:5432` value. Do not infer a live-database pass from offline SQL generation.

Browser smoke requires a running migrated Postgres database, backend, frontend, and seeded credentials. If any prerequisite is unavailable, record the check as `not run` with the exact blocker, owner, and trigger. Do not turn static/unit evidence into a browser-smoke claim.

Real DeepSeek smoke likewise requires explicit authorization, a real `DEEPSEEK_API_KEY`, the official `https://api.deepseek.com` endpoint, and a direct-transport preflight in which `urllib.request.getproxies()` returns no non-empty `http`, `https`, or `all` entry. This covers the environment and Windows registry/macOS SystemConfiguration sources consulted by the default httpx/OpenAI transport when they are returned by that function; the smoke rejects before provider construction and never prints proxy values. Localhost and mock responses do not qualify. Do not claim a real-provider pass from mocked provider tests.

## 6. Common failures

- `JWT_SECRET_KEY environment variable is required`: export/set the signing secret before importing the app.
- `DATABASE_URL environment variable is required`: make the URL available to the current process.
- Connection refused from host Uvicorn: the Compose database is not host-published; use a separately reachable Postgres or the full Compose app path.
- Alembic cannot create `vector`: use a database role allowed to enable pgvector.
- Authenticated unsafe request returns `403 CSRF origin check failed`: align `FRONTEND_URL`/`APP_BASE_DOMAIN` and send the real Origin/Referer.
- Bearer request returns `401`: expected; use the httpOnly cookie session.
