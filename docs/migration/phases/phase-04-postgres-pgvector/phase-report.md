# Phase 04 Report - Postgres + pgvector Baseline

## Scope

This first Phase 4 round builds the runnable migration baseline in code: Postgres-only DB configuration, Alembic setup, initial schema revision, JSONB framework storage, docker-compose db wiring, and environment examples.

This round does not implement Phase 5/8/9/10/11 business features. The new Agent, RAG, LLMWiki, and artefact tables are schema placeholders only.

## Files Changed

- `MIGRATION_PHASES.md`
- `.env.example`
- `docker-compose.yml`
- `backend_py/.env.example`
- `backend_py/requirements.txt`
- `backend_py/app/db.py`
- `backend_py/app/models.py`
- `backend_py/main.py`
- `backend_py/app/api/frameworks_shared.py`
- `backend_py/app/api/frameworks_crud.py`
- `backend_py/app/services/vectorstore/pgvector.py`
- `backend_py/tests/conftest.py`
- `backend_py/tests/test_framework_jsonb.py`
- `backend_py/tests/test_provider_abstractions.py`
- `backend_py/alembic.ini`
- `backend_py/alembic/env.py`
- `backend_py/alembic/script.py.mako`
- `backend_py/alembic/versions/0001_phase4_postgres_pgvector.py`
- `docs/migration/phases/phase-04-postgres-pgvector/checklist.md`
- `docs/migration/phases/phase-04-postgres-pgvector/phase-report.md`
- `docs/migration/phases/phase-04-postgres-pgvector/verification.md`

## Database Configuration

- `backend_py/app/db.py` now reads `DATABASE_URL` from the environment.
- Missing `DATABASE_URL` raises `RuntimeError`.
- The SQLite URL default was removed.
- SQLite thread-check connect args were removed.
- `backend_py/main.py` no longer performs SQLAlchemy metadata auto-create at startup.
- Alembic is now the schema source.

## Alembic Baseline

- The initial revision is `0001_phase4_postgres_pgvector`.
- It starts with `CREATE EXTENSION IF NOT EXISTS vector`.
- It creates the existing runtime tables:
  - `users`
  - `frameworks`
  - `materials`
  - `synced_vector_items`
- It converts framework JSON storage to JSONB:
  - `metadata_json`
  - `steps_json`
  - `artefacts_json`
  - `risks_json`
  - `escalation_json`
  - `raw_framework_json`
  - `raw_metadata_json`
- JSONB server defaults use Postgres expressions such as `'{}'::jsonb` and `'[]'::jsonb`.
- The SQLAlchemy models do not use mutable Python defaults like `{}` or `[]`.

## Placeholder Tables

Phase 5 placeholder:

- `artefacts`

Phase 8 Agent placeholders:

- `agent_runs`
- `agent_messages`
- `agent_tool_invocations`

Phase 9 RAG placeholders:

- `documents`
- `document_chunks`
- `citations`

Phase 10 LLMWiki placeholders:

- `wiki_pages`
- `wiki_claims`
- `wiki_links`
- `wiki_entities`
- `wiki_builds`
- `wiki_eval_questions`

`document_chunks.embedding` is fixed to `Vector(1024)`, and the migration creates `ix_document_chunks_embedding_hnsw` using HNSW cosine ops.

## JSONB Roundtrip

Framework create/update/detail/list paths now pass Python dict/list values to JSONB columns and read back dict/list values directly. A compatibility helper still accepts legacy JSON text so old rows can be decoded if encountered.

This avoids double-encoding framework JSON in Postgres while preserving current framework CRUD response shapes.

Added unit coverage confirms generated framework saves assign native dict/list values instead of JSON strings.

## Docker and Env

- `docker-compose.yml` adds `db` using `pgvector/pgvector:pg16`.
- `pgdata` volume was added.
- The app service receives `DATABASE_URL`.
- The db service has no host `5432` port mapping by default.
- `.env.example` and `backend_py/.env.example` now show `DATABASE_URL=postgresql+psycopg://...`.
- No real password or local private connection string was committed.

## Boundary Decisions

- No quota/admin fields were added because current runtime code has no explicit dependency on them.
- No `tenants`, `tenant_members`, `workspaces`, or `workspace_members` tables were added.
- `artefacts` has schema only. Phase 5 will decide owner checks through `framework.creator_id`.
- No RAG upload/chunk/embed/search pipeline was added.
- No Agent loop, SSE, Tool Registry, LLMWiki compiler/retriever, Chat UI, or Skill Registry was added.
- `PgVectorProvider` remains a provider abstraction stub. Its NotImplementedError text now points to Phase 9 retrieval wiring because Phase 4 only creates the Postgres/pgvector schema baseline.

## Conflicts and Minimal Handling

- `MIGRATION_PHASES.md` contained the exact legacy SQLite thread-check literal as an instruction to remove it. The line was reworded so repository-wide grep can prove the forbidden literal is gone without changing the plan's intent.
- Legacy frontend and historical docs still contain tenant-era wording. Per the Phase 4 supplemental instruction, tenant scanning for new schema focused on `backend_py/app/models.py` and `backend_py/alembic/`, where there are no tenant hits. Legacy frontend cleanup remains Phase 6/7 scope.

## Reviewer Finding Closure - 2026-05-31

The Phase 4 verification record previously claimed Direct SQL and ORM JSONB smoke tests had passed, but both documented commands referenced fields that are not present in the current schema/model: `users.hashed_password`, `users.is_active`, `users.updated_at`, and `frameworks.description`. That made the recorded smoke results untrustworthy.

This follow-up corrected the smoke commands to use the actual Phase 4 schema:

- `users.password_hash`, `users.created_at`, and `users.last_login`.
- `frameworks.family` and existing JSONB columns.
- no `frameworks.description`.

The corrected Direct SQL smoke and corrected ORM smoke were rerun against the live compose Postgres db and passed. `verification.md` now records the actual rerun commands and results, including Docker availability, live `vector` extension checks, `document_chunks.embedding = vector(1024)`, the HNSW cosine index, backend pytest, Alembic history/offline SQL, and the required forbidden grep checks.

No schema changes were made for this closure because the existing schema matches the Phase 4 plan. No Phase 5, RAG, Agent, LLMWiki, Chat UI, or Skill Registry functionality was implemented.

## Current Completion Status

The Phase 4 first-round Postgres + pgvector baseline is complete:

- Docker Desktop was available for follow-up verification.
- The `db` service started with `pgvector/pgvector:pg16` and became healthy.
- A real empty Postgres + pgvector DB accepted `alembic upgrade head`.
- Live schema checks confirmed `document_chunks.embedding` is `vector(1024)` and the HNSW cosine index exists.
- Corrected Framework CRUD smoke passed against Postgres with native JSONB dict/list roundtrip.
- Backend `pytest -q` passed.
- Required grep checks passed.

No Phase 5/8/9/10/11 business functionality was implemented during the follow-up verification.
