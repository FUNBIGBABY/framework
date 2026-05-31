# Phase 04 Verification - Postgres + pgvector Baseline

This file was corrected on 2026-05-31 to close reviewer findings against the Phase 4 verification record.

The previous Direct SQL and ORM JSONB smoke commands referenced fields that do not exist in the current schema/model:

- `users.hashed_password`
- `users.is_active`
- `users.updated_at`
- `frameworks.description`

Those previous smoke results are not trusted. The commands below were run against the current Phase 4 schema and ORM model.

## Syntax Check

Command:

```powershell
backend_py\.venv\Scripts\python.exe -m py_compile backend_py\app\db.py backend_py\app\models.py backend_py\app\api\frameworks_shared.py backend_py\app\api\frameworks_crud.py backend_py\app\services\vectorstore\pgvector.py backend_py\main.py backend_py\alembic\env.py backend_py\alembic\versions\0001_phase4_postgres_pgvector.py backend_py\tests\conftest.py backend_py\tests\test_provider_abstractions.py
```

Result: passed with exit code `0` and no output.

## Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
57 passed, 5 warnings in 4.39s
```

Warnings are existing Pydantic v2 deprecation warnings in `backend_py/app/api/users.py` plus existing `datetime.utcnow()` deprecation warnings in framework JSONB save paths.

## Alembic History

Command:

```powershell
$env:DATABASE_URL='postgresql+psycopg://test:test@localhost:5432/test'
backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini history --verbose
```

Result:

```text
Rev: 0001_phase4_postgres_pgvector (head)
Parent: <base>
Path: C:\Users\micha\Desktop\project\framework\backend_py\alembic\versions\0001_phase4_postgres_pgvector.py

    phase 4 postgres pgvector baseline

    Revision ID: 0001_phase4_postgres_pgvector
    Revises:
    Create Date: 2026-05-31
```

## Alembic Offline SQL

Command:

```powershell
$env:DATABASE_URL='postgresql+psycopg://test:test@localhost:5432/test'
backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini upgrade head --sql
```

Result: passed with exit code `0`.

Important generated SQL lines:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
embedding VECTOR(1024);
CREATE INDEX ix_document_chunks_embedding_hnsw ON document_chunks USING hnsw (embedding vector_cosine_ops);
```

## Docker DB Availability

Commands:

```powershell
docker --version
docker compose up -d db
docker compose ps db
docker compose exec -T db pg_isready -U valorie -d valorie
docker compose exec -T db psql -U valorie -d valorie -c "SELECT version_num FROM alembic_version;"
```

Result: Docker was available. `docker --version` printed an access warning for `C:\Users\micha\.docker\config.json` and then:

```text
Docker version 29.5.2, build 79eb04c
```

`docker compose up -d db` reused the existing container and reported:

```text
Container valorie-db Running
```

`docker compose ps db` showed `valorie-db` using image `pgvector/pgvector:pg16`, status `Up ... (healthy)`, and only container port `5432/tcp`.

`pg_isready` returned:

```text
/var/run/postgresql:5432 - accepting connections
```

The live DB migration version was:

```text
0001_phase4_postgres_pgvector
```

Docker Compose emitted expected warnings about unset app/frontend environment variables and the obsolete top-level `version` key; these warnings did not affect the db checks.

## Live Schema Check

Extension check:

```powershell
docker compose exec -T db psql -U valorie -d valorie -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

Result:

```text
vector
```

Embedding type check:

```powershell
docker compose exec -T db psql -U valorie -d valorie -c "SELECT format_type(a.atttypid, a.atttypmod) AS embedding_type FROM pg_attribute a JOIN pg_class c ON c.oid = a.attrelid JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relname = 'document_chunks' AND a.attname = 'embedding' AND NOT a.attisdropped;"
```

Result:

```text
vector(1024)
```

HNSW cosine index check:

```powershell
docker compose exec -T db psql -U valorie -d valorie -c "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'document_chunks' AND indexname = 'ix_document_chunks_embedding_hnsw';"
```

Result:

```text
ix_document_chunks_embedding_hnsw | CREATE INDEX ix_document_chunks_embedding_hnsw ON public.document_chunks USING hnsw (embedding vector_cosine_ops)
```

## Corrected Direct SQL JSONB Smoke

This smoke uses the actual Phase 4 columns:

- `users.password_hash`
- `users.created_at`
- `users.last_login`
- `frameworks.family`
- no `frameworks.description`

Command:

```powershell
docker compose exec -T db psql -v ON_ERROR_STOP=1 -U valorie -d valorie -c "DELETE FROM frameworks WHERE id = 'fw_phase4_smoke'; DELETE FROM users WHERE id = 'user_phase4_smoke'; INSERT INTO users (id, email, username, password_hash, created_at, last_login) VALUES ('user_phase4_smoke', 'phase4-smoke@example.com', 'phase4-smoke', 'not-used', now(), NULL); INSERT INTO frameworks (id, title, version, family, confidence, pov, creator_id, metadata_json, steps_json, artefacts_json, risks_json, escalation_json, raw_framework_json, raw_metadata_json, created_at, updated_at) VALUES ('fw_phase4_smoke', 'Phase 4 Smoke', '1.0.0', 'Other', 0.9, 'Postgres JSONB smoke', 'user_phase4_smoke', jsonb_build_object('title', 'Phase 4 Smoke'), jsonb_build_array(jsonb_build_object('id', 'step-1')), jsonb_build_object(), jsonb_build_array(), jsonb_build_array(), jsonb_build_object('source', 'smoke'), jsonb_build_object('source', 'smoke'), now(), now()); SELECT id, title, family, jsonb_typeof(metadata_json) AS metadata_type, metadata_json->>'title' AS metadata_title, jsonb_array_length(steps_json) AS step_count FROM frameworks WHERE id = 'fw_phase4_smoke'; UPDATE frameworks SET title = 'Phase 4 Smoke Updated', metadata_json = jsonb_set(metadata_json, '{title}', to_jsonb('Phase 4 Smoke Updated'::text)), updated_at = now() WHERE id = 'fw_phase4_smoke'; SELECT id, title, metadata_json->>'title' AS metadata_title FROM frameworks WHERE id = 'fw_phase4_smoke'; DELETE FROM frameworks WHERE id = 'fw_phase4_smoke'; DELETE FROM users WHERE id = 'user_phase4_smoke'; SELECT count(*) AS remaining_frameworks FROM frameworks WHERE id = 'fw_phase4_smoke';"
```

Result: passed with exit code `0`.

Key output:

```text
INSERT 0 1
INSERT 0 1
fw_phase4_smoke | Phase 4 Smoke | Other | object | Phase 4 Smoke | 1
UPDATE 1
fw_phase4_smoke | Phase 4 Smoke Updated | Phase 4 Smoke Updated
DELETE 1
DELETE 1
remaining_frameworks: 0
```

## Corrected ORM JSONB Smoke

This smoke uses the actual ORM constructor keywords:

- `User.password_hash`
- `User.last_login`
- `Framework.family`
- no `User.hashed_password`
- no `User.is_active`
- no `User.updated_at`
- no `Framework.description`

Command:

```powershell
docker run --rm --network framework_default -v C:\Users\micha\Desktop\project\framework:/work -w /work/backend_py -e DATABASE_URL=postgresql+psycopg://valorie:change-me@valorie-db:5432/valorie python:3.12-slim python -c "import subprocess, sys; subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sqlalchemy>=2.0.36', 'psycopg[binary]>=3.2.3', 'pgvector>=0.3.6']); from datetime import datetime; from app.db import SessionLocal; from app.models import User, Framework; db=SessionLocal(); user_id='user_phase4_orm_smoke'; fw_id='fw_phase4_orm_smoke'; db.query(Framework).filter(Framework.id==fw_id).delete(); db.query(User).filter(User.id==user_id).delete(); db.commit(); now=datetime.utcnow(); user=User(id=user_id, email='phase4-orm-smoke@example.com', username='phase4-orm-smoke', password_hash='not-used', created_at=now, last_login=None); framework=Framework(id=fw_id, title='Phase 4 ORM Smoke', version='1.0.0', family='Other', confidence=0.9, pov='Postgres ORM JSONB smoke', creator_id=user_id, metadata_json={'title': 'Phase 4 ORM Smoke'}, steps_json=[{'id': 'step-1'}], artefacts_json={}, risks_json=[], escalation_json=[], raw_framework_json={'source': 'orm-smoke'}, raw_metadata_json={'source': 'orm-smoke'}, created_at=now, updated_at=now); db.add(user); db.add(framework); db.commit(); loaded=db.query(Framework).filter(Framework.id==fw_id).one(); assert isinstance(loaded.metadata_json, dict); assert isinstance(loaded.steps_json, list); assert loaded.family == 'Other'; loaded.title='Phase 4 ORM Smoke Updated'; loaded.metadata_json={'title': 'Phase 4 ORM Smoke Updated'}; db.commit(); updated=db.query(Framework).filter(Framework.id==fw_id).one(); assert updated.metadata_json['title']=='Phase 4 ORM Smoke Updated'; db.delete(updated); db.delete(user); db.commit(); assert db.query(Framework).filter(Framework.id==fw_id).count()==0; db.close(); print('orm framework crud smoke ok')"
```

Result: passed with exit code `0`.

The temporary container installed `sqlalchemy-2.0.50`, `psycopg-3.3.4`, `psycopg-binary-3.3.4`, and `pgvector-0.4.2`, then printed:

```text
orm framework crud smoke ok
```

The command also emitted a Python `datetime.utcnow()` deprecation warning.

## Forbidden Grep Checks

Runtime forbidden-path command:

```powershell
rg -n "sqlite:///|check_same_thread|Base\.metadata\.create_all" backend_py/app backend_py/main.py
```

Result: no matches. `rg` exited `1`.

Tenant schema command:

```powershell
rg -n "tenant|tenant_id|tenantId" backend_py/app/models.py backend_py/alembic
```

Result: no matches. `rg` exited `1`.

PgVector stale-deferral command:

```powershell
rg -n "deferred to Phase 4|SQLAlchemy/pgvector wiring is deferred to Phase 4|Phase 2 stub" backend_py/app/services/vectorstore/pgvector.py
```

Result: no matches. `rg` exited `1`.

## Phase 4 Completion Gate

The reviewer finding closure checks are satisfied:

- Backend tests passed after updating the PgVectorProvider stub expectation to Phase 9.
- Alembic history and offline SQL generation passed.
- Docker db was available and healthy.
- The live DB is at `0001_phase4_postgres_pgvector`.
- Corrected Direct SQL JSONB smoke passed against the actual schema.
- Corrected ORM JSONB smoke passed against the actual SQLAlchemy models.
- Live schema checks confirmed `vector`, `document_chunks.embedding = vector(1024)`, and `ix_document_chunks_embedding_hnsw`.
- Required forbidden grep checks passed.

This verification does not claim completion of deferred Phase 5/8/9/10/11 business features. RAG upload/chunk/embed/search and PgVectorProvider retrieval behavior remain Phase 9 scope.
