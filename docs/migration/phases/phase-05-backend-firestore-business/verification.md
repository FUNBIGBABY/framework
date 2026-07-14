# Phase 05 Verification - Backend Firestore Business Logic

## Current Reviewer Transcription - 2026-07-13

- Review event `MR-2EC4192-20260713-01` records verdict `accepted_with_documented_deferral` at reviewed/accepted commit `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`.
- Historical embedded artefact versus child-row reconciliation remains `not run`; the authenticated 501 legacy sync routes remain quarantine shells. No live data result is claimed by this transcription.
- Residual risk is possible legacy artefact count/identity mismatch and intentionally unavailable successful indexing/retrieval/logging. Data Reconciliation Owner retains the import/fallback-deletion/mismatch triggers; Phase 9 RAG Replacement Owner may act only after Phase 9 authorization.

## Current Corrective Status

The earlier reviewer-attention-only statement below is superseded. Materials
ownership is a P1 remediation: authenticated writes now retain ownership,
retrieval filters by material id and owner, and pre-existing ownerless rows
remain quarantined without arbitrary backfill or deletion. Security Owner and
Backend Owner must approve a verified legacy-data disposition before Phase 7
acceptance or any multi-user/production use. The authenticated legacy
`vector_sync` HTTP 501 shells are quarantined deferred compatibility surfaces,
not functional parity; Phase 9 RAG Replacement Owner owns any future replacement.

## Governance Reconciliation - 2026-07-10

- At the 2026-07-10 reconciliation, the ledger verdict was `pending` and the reviewer identity/date/raw artifact were unavailable. The current named verdict/artifact is the 2026-07-13 transcription above.
- Implementation commit: `742f1e79f3fb71d44ce21284999e64ca76c5060f`.
- Later status-wording commit: `a2115042771d9e91e9410cf5597031f3c78bee9a`; it is not acceptance evidence.
- Historical capability enumeration and disposition: `capability-inventory.md`.
- Live Postgres artefact-history query: `not run` in this corrective remediation; no data result is claimed. The existing SQL checks only non-empty embedded artefacts with zero child rows, and a zero result alone cannot establish `not applicable`.
- Superseded historical entry: this record previously assigned Materials ownership and legacy `vector_sync` request fields to focused review only, with no implementation change. The Current Corrective Status above is authoritative.

### Capability-matrix verification template

The focused re-review must compare the named exports and internal artefact fan-out in `742f1e79f3fb71d44ce21284999e64ca76c5060f:frontend/src/lib/firebase.js` with `capability-inventory.md`, confirm exactly one approved disposition per row, and attach evidence for any claimed REST parity.

### Artefact-history evidence template (not run)

Data Reconciliation Owner records database/snapshot identity, Alembic revision, date, and the limited zero-child query result, then compares embedded artefact counts and identities with child rows or supplies an equivalent shape-aware audit with documented sampling and data-source provenance. A zero result from the limited query alone is insufficient. Any non-zero result or partial/count/identity mismatch triggers separately authorized reconciliation with backup/rollback notes.

This verification records Phase 5 Round 1, Round 2, Round 3, Round 4, Round 5, Round 6, and closeout repair status.

Round 2 verification is limited to the private Framework owner CRUD contract. It does not verify public library, publish/unpublish, artefact child resources, admin users, generation persistence migration, or Phase 9 RAG.

Round 3 verification is limited to generation persistence, deterministic file metadata convergence, and mock-confidence production-path guarding. It does not verify public library, publish/unpublish, artefact child resources, admin users, frontend Firebase removal, or Phase 9 RAG.

Round 4 verification is limited to backend publish/unpublish semantics, authenticated public library API behavior, publish schema migration, route ordering, and no-frontend-diff boundary checks. It does not verify artefact child resources, admin users, frontend Firebase removal, tenant/workspace publishing, Agent/LLMWiki/Chat/MCP, or Phase 9 RAG.

Round 5 verification is limited to backend artefact subresource CRUD, owner isolation through parent framework ownership, native JSONB dict/list handling, current public-library pagination behavior, route ordering, and no-frontend-diff boundary checks. It does not verify admin users, frontend REST wiring, frontend Firebase removal, tenant/workspace publishing, Agent/LLMWiki/Chat/MCP, historical `frameworks.artefacts_json` backfill, or Phase 9 RAG.

Round 6 verification is limited to backend admin user management, disabled-user login/current-user enforcement, admin user schema migration, Step 5.3 canonical wording cleanup, untracked-file risk reporting, and no-frontend-diff boundary checks. Closeout repair verifies disabled-token enforcement for routes that depend on `get_current_user_id`. It does not verify Phase 6 frontend REST/Firebase removal, Phase 7 tenant/domain cleanup, Phase 9 RAG indexing/retrieval, or Agent/LLMWiki/Chat/MCP.

## Forbidden vector_sync Grep

Command:

```powershell
rg -n "firestore.googleapis.com|identitytoolkit|FIREBASE_|VITE_FIREBASE_|OPENAI_VECTOR_STORE|upload_json|requests" backend_py/app/api/vector_sync.py
```

Result: no matches. `rg` exited `1`.

## Python Syntax Check

Command:

```powershell
backend_py\.venv\Scripts\python.exe -m py_compile backend_py\app\api\vector_sync.py backend_py\app\api\frameworks.py backend_py\main.py backend_py\app\services\rag\__init__.py backend_py\app\services\rag\indexing.py backend_py\tests\test_auth_hardening.py
```

Result: passed with exit code `0` and no output.

## Focused Auth and vector_sync Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py -q
```

Result:

```text
17 passed, 9 warnings in 8.85s
```

Coverage included:

- unauthenticated `POST /api/frameworks/push-framework` returns 401/403.
- unauthenticated `POST /api/frameworks/sync-library` returns 401/403.
- unauthenticated `POST /api/frameworks/log-event` returns 401/403.
- authenticated `POST /api/frameworks/push-framework` returns 501 with `Phase 9` and `deferred` in the body.
- authenticated `POST /api/frameworks/sync-library` returns 501 with `Phase 9` and `deferred` in the body.
- authenticated `POST /api/frameworks/log-event` returns 501 with `Phase 9` and `deferred` in the body.

Warnings are existing Pydantic v2 deprecation warnings in `app/api/users.py` plus existing `datetime.utcnow()` deprecation warnings in JWT creation.

## Full Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
61 passed, 11 warnings in 8.96s
```

Warnings are existing Pydantic v2 deprecation warnings and existing `datetime.utcnow()` deprecation warnings.

## Import Compatibility

`backend_py/app/api/frameworks.py` continues to import and re-export the vector sync request models and route functions.

Command:

```powershell
cd backend_py
$env:JWT_SECRET_KEY='test-secret-for-main-import-check-32-chars'; $env:DATABASE_URL='postgresql+psycopg://test:test@localhost:5432/test'; .\.venv\Scripts\python.exe -c "import main; print('import main ok')"
```

Result:

```text
Frontend static files not found (development mode)
import main ok
```

This records the actual `import main` verification. `tests/test_main.py` also passes in the full backend suite, but it is not the sole evidence claimed for `main.py` import compatibility.

## External Network Requests

No test or verification command made an intentional external network request. The `vector_sync.py` API no longer imports `requests`, no longer calls Firestore REST, no longer calls Identity Toolkit, and no longer calls OpenAI Vector Store upload APIs.

## Deferred Work

This round did not implement Phase 9 indexing/retrieval. `RAGIndexingService` is a quarantine stub that raises a deferred exception mapped to HTTP 501.

## Round 2 Python Syntax Check

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m py_compile app\api\frameworks.py app\api\frameworks_crud.py app\api\frameworks_shared.py tests\test_framework_owner_crud.py main.py
```

Result: passed with exit code `0` and no output.

## Round 2 Owner Parameter Grep

Command:

```powershell
rg -n "user_id\s*[:=].*(Body|Query|Form)|creator_id\s*[:=].*(Body|Query|Form)" backend_py\app\api\frameworks_crud.py backend_py\app\api\frameworks_shared.py
```

Result: no matches. `rg` exited `1`.

This confirms `frameworks_crud.py` and `frameworks_shared.py` do not receive `user_id` or `creator_id` through `Body`, `Query`, or `Form` parameters.

## Round 2 Full Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
66 passed, 37 warnings in 5.43s
```

Coverage added in `tests/test_framework_owner_crud.py`:

- `POST /api/frameworks` creates a framework owned by the JWT subject.
- Legacy camelCase `creatorId` in the request body does not override the JWT owner.
- Snake_case `user_id` and `creator_id` in create request bodies return 422 validation errors.
- `GET /api/frameworks/my-frameworks` ignores a malicious `?user_id=` query and returns only the JWT user's frameworks.
- `GET /api/frameworks/my-frameworks/by-family` returns only the JWT user's frameworks.
- Cross-user access to `GET /api/frameworks/{id}` returns 404.
- Cross-user access to `GET /api/frameworks/{id}/binding` returns 404.
- Cross-user access to `PUT /api/frameworks/{id}` returns 404 and does not mutate the owner record.
- Cross-user access to `DELETE /api/frameworks/{id}` returns 404 and does not delete the owner record.
- Owner update keeps JSONB fields as native dict/list values.
- Legacy `_raw` JSON text is parsed into native JSON before assignment.

Warnings are existing Pydantic v2 deprecation warnings in `app/api/users.py`, existing `datetime.utcnow()` deprecation warnings in JWT creation, and existing `datetime.utcnow()` deprecation warnings in `save_framework_to_db`.

## Round 2 Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

## Round 2 Boundaries

No `frontend/` files were modified.

Round 2 did not implement public library, publish/unpublish, artefacts CRUD, admin users, generation persistence changes, vector indexing, RAG retrieval, Firebase SDK removal, tenants/workspaces, Agent, LLMWiki, Chat, or MCP.

## Round 3 Python Syntax Check

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m py_compile app\api\generation.py app\api\frameworks_shared.py tests\test_generation_persistence.py tests\test_provider_abstractions.py
```

Result: passed with exit code `0` and no output.

## Round 3 Focused Generation Persistence Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_generation_persistence.py tests\test_provider_abstractions.py::test_generate_from_file_default_path_avoids_legacy_local -q
```

Result:

```text
7 passed, 14 warnings in 4.92s
```

Coverage added in `tests/test_generation_persistence.py`:

- authenticated `POST /api/frameworks/generate-from-text` saves a Framework row owned by the JWT subject and returns `framework_id` plus `framework_ids`.
- authenticated `POST /api/frameworks/generate-from-file` on the deterministic metadata path saves a Framework row and returns saved IDs.
- authenticated `POST /api/frameworks/generate-from-files` with multiple provider outputs saves all Framework rows and returns all saved IDs.
- generation routes without authentication return 401/403.
- saved JSONB fields remain native dict/list values rather than JSON strings.
- `creator_id` and `user_id` supplied in text JSON or multipart form data do not override the JWT owner.
- production mock generation is rejected unless `dry_run=true`; explicit dry-run mock generation remains available.

## Round 3 Focused Auth, Owner CRUD, Vector Sync, and Generation Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_framework_owner_crud.py tests\test_generation_persistence.py -q
```

Result:

```text
28 passed, 49 warnings in 5.87s
```

This confirms Round 1 vector sync routes remain authenticated 501, Round 2 owner CRUD tests still pass, and Round 3 generation persistence tests pass together.

## Round 3 Owner Parameter Grep

Command:

```powershell
rg -n "user_id\s*[:=].*(Body|Query|Form)|creator_id\s*[:=].*(Body|Query|Form)" backend_py\app\api\generation.py backend_py\app\api\frameworks_shared.py
```

Result: no matches. `rg` exited `1`.

This confirms generation/shared code does not define `user_id` or `creator_id` as request `Body`, `Query`, or `Form` parameters.

## Round 3 Mock Confidence Grep

Command:

```powershell
rg -n "calculate_mock_confidence|use_mock|ENV|dry_run" backend_py\app\api\generation.py backend_py\app\api\frameworks_shared.py
```

Result: matches are limited to:

- `TextGenerateRequest.dry_run` and `GenerateResponse`-adjacent request handling.
- `should_use_mock_generation(dry_run)`, which allows mock generation only for `dry_run=true` or `ENV=dev`.
- `process_with_global_llm(..., use_mock=True, dry_run=...)`, which returns HTTP 503 outside those allowed mock contexts.
- generation routes passing `use_mock=should_use_mock_generation(...)`.
- `calculate_mock_confidence()` inside `build_mock_framework`, reached only through the guarded mock path in active generation routes.
- one existing commented-out historical line in `save_framework_to_db`.

## Round 3 Forbidden vector_sync Grep

Command:

```powershell
rg -n "firestore.googleapis.com|identitytoolkit|FIREBASE_|VITE_FIREBASE_|OPENAI_VECTOR_STORE|upload_json|requests" backend_py\app\api\vector_sync.py
```

Result: no matches. `rg` exited `1`.

## Round 3 Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

## Round 3 Full Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
72 passed, 51 warnings in 5.35s
```

Warnings are existing Pydantic v2 deprecation warnings in `app/api/users.py`, existing `datetime.utcnow()` deprecation warnings in JWT creation, and existing `datetime.utcnow()` deprecation warnings in `save_framework_to_db`.

## Round 3 Boundaries

No `frontend/` files were modified.

Round 3 did not implement public library, publish/unpublish, artefacts CRUD, admin users, vector indexing, RAG retrieval, `PgVectorProvider`, `EmbeddingProvider`, Firebase SDK removal, tenants/workspaces, Agent, LLMWiki, Chat, MCP, or Phase 6 frontend Firebase removal.

## Round 4 Python Syntax Check

Command:

```powershell
backend_py\.venv\Scripts\python.exe -m py_compile backend_py\app\models.py backend_py\app\api\frameworks.py backend_py\app\api\frameworks_public.py backend_py\tests\test_framework_publish_public.py backend_py\alembic\versions\0002_phase5_framework_publish_fields.py
```

Result: passed with exit code `0` and no output.

## Round 4 Focused Publish/Public Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_framework_publish_public.py -q
```

Result:

```text
6 passed, 16 warnings in 5.13s
```

Coverage added in `tests/test_framework_publish_public.py`:

- unauthenticated `GET /api/frameworks/public` returns 401/403.
- authenticated `GET /api/frameworks/public` returns 200.
- the public list returns only published frameworks.
- unpublished frameworks do not appear in the public list.
- owner publish sets `is_public=true`, sets `published_at`, saves category/tags/version, and makes the framework appear in the public list.
- owner unpublish sets `is_public=false`, clears `published_at`, keeps category/tags, and removes the framework from the public list.
- non-owner publish/unpublish returns 404 and does not mutate the owner row.
- public list items contain only the simplified schema and do not expose `creator_id`, metadata JSON, or raw framework JSON.
- `/api/frameworks/public` reaches the public-list handler instead of the dynamic `/{framework_id}` handler.

Warnings are existing `datetime.utcnow()` deprecation warnings in JWT creation.

## Round 4 Focused Regression Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_framework_owner_crud.py tests\test_generation_persistence.py tests\test_framework_publish_public.py -q
```

Result:

```text
34 passed, 65 warnings in 5.77s
```

This confirms Round 1 vector sync authenticated 501 behavior, Round 2 owner CRUD isolation, Round 3 generation persistence, and Round 4 publish/public library behavior pass together.

## Round 4 Alembic History

Command:

```powershell
backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini history --verbose
```

Result: passed with exit code `0`. The history shows:

```text
Rev: 0002_phase5_framework_publish_fields (head)
Parent: 0001_phase4_postgres_pgvector

Rev: 0001_phase4_postgres_pgvector
Parent: <base>
```

## Round 4 Alembic Offline SQL

Initial command:

```powershell
backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini upgrade head --sql
```

Initial result: failed with `RuntimeError: DATABASE_URL environment variable is required`.

Rerun command:

```powershell
$env:DATABASE_URL='postgresql+psycopg://test:test@localhost:5432/test'; backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini upgrade head --sql
```

Rerun result: passed with exit code `0`. The generated offline SQL includes the Round 4 migration:

```sql
ALTER TABLE frameworks ADD COLUMN is_public BOOLEAN DEFAULT false NOT NULL;
ALTER TABLE frameworks ADD COLUMN category VARCHAR;
ALTER TABLE frameworks ADD COLUMN tags_json JSONB DEFAULT '[]'::jsonb NOT NULL;
ALTER TABLE frameworks ADD COLUMN published_at TIMESTAMP WITHOUT TIME ZONE;
CREATE INDEX ix_frameworks_is_public ON frameworks (is_public);
CREATE INDEX ix_frameworks_category ON frameworks (category);
CREATE INDEX ix_frameworks_published_at ON frameworks (published_at);
```

## Round 4 Tenant/Workspace Publish Grep

Command:

```powershell
rg -n "tenant|tenant_id|tenantId|workspace|publishedToOrganization" backend_py/app backend_py/alembic
```

Result: no matches. `rg` exited `1`.

This confirms Round 4 did not add tenant, workspace, organization, or `publishedToOrganization` publish behavior in backend app code or Alembic migrations.

## Round 4 Forbidden vector_sync Grep

Command:

```powershell
rg -n "firestore.googleapis.com|identitytoolkit|FIREBASE_|VITE_FIREBASE_|OPENAI_VECTOR_STORE|upload_json|requests" backend_py/app/api/vector_sync.py
```

Result: no matches. `rg` exited `1`.

This confirms Round 1 vector sync quarantine remained intact after Round 4.

## Round 4 Frontend Diff Check

Command:

```powershell
git diff -- frontend
```

Result: passed with exit code `0` and no output.

No `frontend/` files were modified in Round 4.

## Round 4 Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

## Round 4 Final Git Snapshot

Command:

```powershell
git status --short
```

Result:

```text
 M backend_py/app/api/frameworks.py
 M backend_py/app/api/frameworks_crud.py
 M backend_py/app/api/frameworks_shared.py
 M backend_py/app/api/generation.py
 M backend_py/app/api/vector_sync.py
 M backend_py/app/models.py
 M backend_py/main.py
 M backend_py/tests/test_auth_hardening.py
 M backend_py/tests/test_provider_abstractions.py
?? backend_py/alembic/versions/0002_phase5_framework_publish_fields.py
?? backend_py/app/api/frameworks_public.py
?? backend_py/app/services/rag/
?? backend_py/tests/test_framework_owner_crud.py
?? backend_py/tests/test_framework_publish_public.py
?? backend_py/tests/test_generation_persistence.py
?? docs/migration/phases/phase-05-backend-firestore-business/
```

The status includes prior Round 1/2/3 backend and doc files that were already part of the cumulative Phase 5 working tree, plus Round 4's new migration, public framework API module, publish/public tests, model update, aggregate router update, and Phase 5 doc updates.

Command:

```powershell
git diff --stat
```

Result:

```text
 backend_py/app/api/frameworks.py               |  17 +-
 backend_py/app/api/frameworks_crud.py          | 413 +++++++++++++------------
 backend_py/app/api/frameworks_shared.py        |  76 ++++-
 backend_py/app/api/generation.py               | 353 ++++++++-------------
 backend_py/app/api/vector_sync.py              | 335 ++------------------
 backend_py/app/models.py                       |   6 +
 backend_py/main.py                             |  35 ---
 backend_py/tests/test_auth_hardening.py        |  29 ++
 backend_py/tests/test_provider_abstractions.py |   8 +-
 9 files changed, 495 insertions(+), 777 deletions(-)
```

`git diff --stat` reports tracked-file diffs only; new untracked Round 4 files are shown in `git status --short`.

## Round 4 Full Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
78 passed, 67 warnings in 4.94s
```

Warnings are existing Pydantic v2 deprecation warnings in `app/api/users.py`, existing `datetime.utcnow()` deprecation warnings in JWT creation, and existing `datetime.utcnow()` deprecation warnings in `save_framework_to_db`.

## Round 4 Boundaries

No `frontend/` files were modified.

Round 4 did not implement artefacts CRUD, admin users, new generation logic beyond Round 3 persistence, vector indexing, RAG retrieval, `PgVectorProvider`, `EmbeddingProvider`, Firebase SDK removal, `AuthContext` changes, tenant/workspace/organization publishing, Agent, LLMWiki, Chat, MCP, or Phase 6 frontend Firebase removal.

## Round 5 Python Syntax Check

Command:

```powershell
backend_py\.venv\Scripts\python.exe -m py_compile backend_py\app\api\artefacts.py backend_py\app\api\frameworks.py backend_py\tests\test_framework_artefacts.py backend_py\tests\test_framework_publish_public.py
```

Result: passed with exit code `0` and no output.

## Round 5 Focused Artefact and Public Pagination Tests

Initial command:

```powershell
cd backend_py
backend_py\.venv\Scripts\python.exe -m pytest tests\test_framework_artefacts.py tests\test_framework_publish_public.py -q
```

Initial result: failed before tests ran because the command was executed from `backend_py` while still prefixing the venv path with `backend_py\`.

Rerun command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_framework_artefacts.py tests\test_framework_publish_public.py -q
```

Rerun result:

```text
22 passed, 64 warnings in 5.35s
```

Coverage added in `tests/test_framework_artefacts.py`:

- unauthenticated list/create/get/update/delete artefact routes return 401/403.
- owner can create, list, get, update, and delete artefacts under their framework.
- non-owner cannot list, create, get, update, or delete artefacts under another user's framework.
- child get/update/delete require `artefact_id` to match the path `framework_id`.
- create and update keep `content_json` and `metadata_json` as native dict/list containers.
- mutation bodies reject `user_id`, `creator_id`, and `framework_id`.
- `ord` defaults to `0`.
- omitted `artefact_type` defaults to `custom`.
- the model cascade contract is configured with `Artefact.framework_id` `ondelete=CASCADE` and ORM `delete-orphan`.

Coverage added in `tests/test_framework_publish_public.py`:

- blank `?limit=` returns 422.
- `limit=51` returns 422 under the current max `50` behavior.
- second-page cursor returns the next page under the existing sort order.
- invalid cursor returns 400 with `Invalid public library cursor`.

## Round 5 Full Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
94 passed, 115 warnings in 5.94s
```

Warnings are existing Pydantic v2 deprecation warnings in `app/api/users.py`, existing `datetime.utcnow()` deprecation warnings in JWT creation, and existing `datetime.utcnow()` deprecation warnings in `save_framework_to_db`.

## Round 5 Owner Parameter Grep

Command:

```powershell
rg -n "user_id\s*[:=].*(Body|Query|Form)|creator_id\s*[:=].*(Body|Query|Form)" backend_py\app\api
```

Result: no matches. `rg` exited `1`.

This confirms Round 5 did not add any backend API route parameters that accept `user_id` or `creator_id` through `Body`, `Query`, or `Form`.

## Round 5 Tenant/Workspace Grep

Command:

```powershell
rg -n "tenant|tenant_id|tenantId|workspace|publishedToOrganization" backend_py\app backend_py\alembic
```

Result: no matches. `rg` exited `1`.

This confirms Round 5 did not add tenant, workspace, organization, or `publishedToOrganization` behavior in backend app code or Alembic migrations.

## Round 5 Forbidden vector_sync Grep

Command:

```powershell
rg -n "firestore.googleapis.com|identitytoolkit|FIREBASE_|VITE_FIREBASE_|OPENAI_VECTOR_STORE|upload_json|requests" backend_py\app\api\vector_sync.py
```

Result: no matches. `rg` exited `1`.

This confirms Round 1 vector sync quarantine remained intact after Round 5.

## Round 5 Frontend Diff Check

Command:

```powershell
git diff -- frontend
```

Result: passed with exit code `0` and no output.

No `frontend/` files were modified in Round 5.

## Round 5 Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

## Round 5 Final Git Snapshot

Command:

```powershell
git status --short
```

Result:

```text
 M backend_py/app/api/frameworks.py
 M backend_py/app/api/frameworks_crud.py
 M backend_py/app/api/frameworks_shared.py
 M backend_py/app/api/generation.py
 M backend_py/app/api/vector_sync.py
 M backend_py/app/models.py
 M backend_py/main.py
 M backend_py/tests/test_auth_hardening.py
 M backend_py/tests/test_provider_abstractions.py
?? backend_py/alembic/versions/0002_phase5_framework_publish_fields.py
?? backend_py/app/api/artefacts.py
?? backend_py/app/api/frameworks_public.py
?? backend_py/app/services/rag/
?? backend_py/tests/test_framework_artefacts.py
?? backend_py/tests/test_framework_owner_crud.py
?? backend_py/tests/test_framework_publish_public.py
?? backend_py/tests/test_generation_persistence.py
?? docs/migration/phases/phase-05-backend-firestore-business/
```

The status includes prior cumulative Round 1/2/3/4 work plus Round 5's new artefact API module, artefact tests, public pagination test updates, aggregate router update, and Phase 5 doc updates.

Command:

```powershell
git diff --stat
```

Result:

```text
 backend_py/app/api/frameworks.py               |  19 +-
 backend_py/app/api/frameworks_crud.py          | 413 +++++++++++++------------
 backend_py/app/api/frameworks_shared.py        |  76 ++++-
 backend_py/app/api/generation.py               | 353 ++++++++-------------
 backend_py/app/api/vector_sync.py              | 335 ++------------------
 backend_py/app/models.py                       |   6 +
 backend_py/main.py                             |  35 ---
 backend_py/tests/test_auth_hardening.py        |  29 ++
 backend_py/tests/test_provider_abstractions.py |   8 +-
 9 files changed, 497 insertions(+), 777 deletions(-)
```

`git diff --stat` reports tracked-file diffs only. New untracked Round 4 and Round 5 files are listed in `git status --short`.

## Round 5 DB Migration Decision

No new Alembic revision was added.

Reason: `backend_py/alembic/versions/0001_phase4_postgres_pgvector.py` already creates the `artefacts` table with the columns required by Round 5 and an `ondelete="CASCADE"` FK to `frameworks.id`. `backend_py/app/models.py` already maps the same table and relationship. Round 5 only added REST behavior and tests.

## Round 5 Deferred Work

Round 5 did not migrate or backfill existing generated framework `frameworks.artefacts_json` values into child `artefacts` rows. Historical synchronization remains deferred.

## Round 5 Boundaries

No `frontend/` files were modified.

Round 5 did not implement admin users, Phase 6 frontend REST rewiring, frontend Firebase removal, RAG document upload, vector indexing, RAG retrieval, `PgVectorProvider`, `EmbeddingProvider`, Firebase SDK deletion, tenant/workspace behavior, public organization sharing, Agent, LLMWiki, Chat, MCP, new Firebase setup, or real API key writes.

This verification does not claim full Phase 5 completion.

## Round 6 Preflight Git Tracking Check

Command:

```powershell
git status --short
```

Initial result before Round 6 edits:

```text
 M backend_py/app/api/frameworks.py
 M backend_py/app/api/frameworks_crud.py
 M backend_py/app/api/frameworks_shared.py
 M backend_py/app/api/generation.py
 M backend_py/app/api/vector_sync.py
 M backend_py/app/models.py
 M backend_py/main.py
 M backend_py/tests/test_auth_hardening.py
 M backend_py/tests/test_provider_abstractions.py
?? backend_py/alembic/versions/0002_phase5_framework_publish_fields.py
?? backend_py/app/api/artefacts.py
?? backend_py/app/api/frameworks_public.py
?? backend_py/app/services/rag/
?? backend_py/tests/test_framework_artefacts.py
?? backend_py/tests/test_framework_owner_crud.py
?? backend_py/tests/test_framework_publish_public.py
?? backend_py/tests/test_generation_persistence.py
?? docs/migration/phases/phase-05-backend-firestore-business/
```

This confirmed the audit warning: cumulative Phase 5 implementation, tests, Alembic revision, and docs included untracked files before Round 6 began. These files must be staged before commit/review; `git diff --stat` omits their contents.

Expanded final tracking command:

```powershell
git status --short --untracked-files=all
```

Final result after Round 6 documentation updates and final checks:

```text
 M MIGRATION_PHASES.md
 M backend_py/app/api/frameworks.py
 M backend_py/app/api/frameworks_crud.py
 M backend_py/app/api/frameworks_shared.py
 M backend_py/app/api/generation.py
 M backend_py/app/api/users.py
 M backend_py/app/api/vector_sync.py
 M backend_py/app/auth.py
 M backend_py/app/models.py
 M backend_py/main.py
 M backend_py/scripts/seed_admin.py
 M backend_py/tests/test_auth_hardening.py
 M backend_py/tests/test_provider_abstractions.py
?? backend_py/alembic/versions/0002_phase5_framework_publish_fields.py
?? backend_py/alembic/versions/0003_phase5_admin_user_disabled.py
?? backend_py/app/api/admin_users.py
?? backend_py/app/api/artefacts.py
?? backend_py/app/api/frameworks_public.py
?? backend_py/app/services/rag/__init__.py
?? backend_py/app/services/rag/indexing.py
?? backend_py/tests/test_admin_users.py
?? backend_py/tests/test_framework_artefacts.py
?? backend_py/tests/test_framework_owner_crud.py
?? backend_py/tests/test_framework_publish_public.py
?? backend_py/tests/test_generation_persistence.py
?? docs/migration/phases/phase-05-backend-firestore-business/checklist.md
?? docs/migration/phases/phase-05-backend-firestore-business/phase-report.md
?? docs/migration/phases/phase-05-backend-firestore-business/verification.md
```

## Round 6 Python Syntax Check

Command:

```powershell
backend_py\.venv\Scripts\python.exe -m py_compile backend_py\app\api\admin_users.py backend_py\app\api\users.py backend_py\app\auth.py backend_py\app\models.py backend_py\main.py backend_py\scripts\seed_admin.py backend_py\alembic\versions\0003_phase5_admin_user_disabled.py backend_py\tests\test_admin_users.py
```

Result: passed with exit code `0` and no output.

## Round 6 Focused Admin User Tests

Initial command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_admin_users.py -q
```

Initial result: failed with `1 failed, 10 passed`. The failure was in the new test assertion order: the test checked the fake user object after the same test had already re-enabled the user. The implementation was not changed for this failure; the test was fixed to capture disabled state before the enable call.

Rerun command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_admin_users.py -q
```

Rerun result:

```text
11 passed, 25 warnings in 4.41s
```

Coverage added in `tests/test_admin_users.py`:

- unauthenticated admin user endpoints return 401/403.
- non-admin authenticated users receive 403 for `/api/admin/users`.
- super-admin can list users.
- list user responses exclude `password_hash`.
- super-admin can create a user with plaintext password and stored Argon2id hash.
- admin create rejects request bodies containing `password_hash`.
- public `/api/users/register` remains disabled by default.
- super-admin can disable a user.
- disabled user cannot log in.
- disabled user is rejected by `/api/users/me`.
- super-admin can enable the user again.
- enabled user can log in again.
- super-admin cannot disable self/configured super-admin.

Warnings are existing Pydantic v2 deprecation warnings in `app/api/users.py`, existing `datetime.utcnow()` deprecation warnings in auth/shared code, and new `datetime.utcnow()` deprecation warnings in the Round 6 admin user timestamps.

## Round 6 Cumulative Phase 5 Regression Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_framework_owner_crud.py tests\test_generation_persistence.py tests\test_framework_publish_public.py tests\test_framework_artefacts.py tests\test_admin_users.py -q
```

Result:

```text
61 passed, 136 warnings in 7.19s
```

This confirms Round 1 vector sync authenticated 501 behavior, Round 2 owner CRUD isolation, Round 3 generation persistence, Round 4 publish/authenticated public library behavior, Round 5 artefact subresources, and Round 6 admin users pass together.

## Round 6 Full Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
105 passed, 137 warnings in 7.38s
```

Warnings are existing Pydantic v2 deprecation warnings in `app/api/users.py`, existing `datetime.utcnow()` deprecation warnings in JWT/framework timestamps, and new `datetime.utcnow()` warnings in the Round 6 admin user timestamp writes.

## Round 6 Alembic History

Command:

```powershell
backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini history --verbose
```

Result: passed with exit code `0`. The history shows:

```text
Rev: 0003_phase5_admin_user_disabled (head)
Parent: 0002_phase5_framework_publish_fields

Rev: 0002_phase5_framework_publish_fields
Parent: 0001_phase4_postgres_pgvector

Rev: 0001_phase4_postgres_pgvector
Parent: <base>
```

## Round 6 Alembic Offline SQL

Command:

```powershell
$env:DATABASE_URL='postgresql+psycopg://test:test@localhost:5432/test'; backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini upgrade head --sql
```

Result: passed with exit code `0`. The generated SQL includes the Round 6 migration:

```sql
ALTER TABLE users ADD COLUMN is_disabled BOOLEAN DEFAULT false NOT NULL;
ALTER TABLE users ADD COLUMN disabled_at TIMESTAMP WITHOUT TIME ZONE;
CREATE INDEX ix_users_is_disabled ON users (is_disabled);
```

## Round 6 Owner and Password Hash API Grep

Command:

```powershell
rg -n "user_id\s*[:=].*(Body|Query|Form)|creator_id\s*[:=].*(Body|Query|Form)|password_hash" backend_py\app\api
```

Result:

```text
backend_py\app\api\admin_users.py:154:        password_hash=hash_password(request.password),
backend_py\app\api\users.py:148:        password_hash=hashed_password,
backend_py\app\api\users.py:200:        request.password, user.password_hash
backend_py\app\api\users.py:214:        user.password_hash = hash_password(request.password)
```

No `user_id` or `creator_id` Body/Query/Form route parameters were found. `password_hash` matches are limited to internal hashing, login verification, and password rehash/write paths; admin user list/create responses are tested to exclude `password_hash`.

## Round 6 Tenant/Workspace Grep

Command:

```powershell
rg -n "tenant|tenant_id|tenantId|workspace|publishedToOrganization|invites|members" backend_py\app backend_py\alembic
```

Result: no matches. `rg` exited `1`.

## Round 6 Vector/Firebase Greps

Broad command:

```powershell
rg -n "firestore.googleapis.com|identitytoolkit|FIREBASE_|VITE_FIREBASE_|OPENAI_VECTOR_STORE|upload_json|requests" backend_py\app
```

Result: matches are limited to `backend_py/app/services/vectorstore/openai_legacy.py`, which remains the intentionally disabled legacy provider from Phase 2. No active API route path matched.

Narrow active-route command:

```powershell
rg -n "firestore.googleapis.com|identitytoolkit|FIREBASE_|VITE_FIREBASE_|OPENAI_VECTOR_STORE|upload_json|requests" backend_py\app\api\vector_sync.py
```

Result: no matches. `rg` exited `1`.

## Round 6 Admin/Disabled Env Grep

Command:

```powershell
rg -n "SUPER_ADMIN_EMAIL|ALLOWED_EMAILS|ENABLE_PUBLIC_REGISTER|is_disabled|disabled" backend_py\app backend_py\scripts backend_py\tests
```

Result: matches show the expected Round 6 admin/disabled code and tests, existing `ENABLE_PUBLIC_REGISTER` / `ALLOWED_EMAILS` registration guard, and unrelated provider tests using "disabled" terminology. No unexpected public registration or frontend-admin trust path was found in backend code.

## Round 6 Frontend Diff Check

Command:

```powershell
git diff -- frontend
```

Result: passed with exit code `0` and no output.

No `frontend/` files were modified in Round 6.

## Round 6 Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output after Round 6 documentation edits.

## Round 6 Final Git Diff Stat

Command:

```powershell
git diff --stat
```

Result:

```text
 MIGRATION_PHASES.md                            |   6 +-
 backend_py/app/api/frameworks.py               |  19 +-
 backend_py/app/api/frameworks_crud.py          | 413 +++++++++++++------------
 backend_py/app/api/frameworks_shared.py        |  76 ++++-
 backend_py/app/api/generation.py               | 353 ++++++++-------------
 backend_py/app/api/users.py                    |   6 +
 backend_py/app/api/vector_sync.py              | 335 ++------------------
 backend_py/app/auth.py                         |   6 +
 backend_py/app/models.py                       |  10 +
 backend_py/main.py                             |  37 +--
 backend_py/scripts/seed_admin.py               |  18 +-
 backend_py/tests/test_auth_hardening.py        |  29 ++
 backend_py/tests/test_provider_abstractions.py |   8 +-
 13 files changed, 533 insertions(+), 783 deletions(-)
```

At that Round 6 checkpoint, this tracked-file stat still omitted untracked Phase 5 files. The later closeout tracking section records the successful staged state.

## Round 6 Deferrals and Non-Goals

- Real embedding, pgvector upsert/search, indexing, retrieval, and citation retrieval remain deferred to Phase 9.
- `RAGIndexingService.index_framework(...)` remains an authenticated 501 stub in Phase 5.
- The Round 6 limitation for routes using only `get_current_user_id` is superseded by closeout repair; ID-only private routes now perform a disabled-user DB check.
- Phase 6 frontend REST/Firebase removal was not implemented.
- Phase 7 tenant/domain cleanup was not implemented.
- Agent, LLMWiki, Chat, and MCP were not implemented.
- No frontend files were changed.
- No real API keys or new Firebase project configuration were added.

## Closeout Repair Disabled-Token Enforcement

Code change verified:

- `get_current_user_id` now decodes the JWT, loads the `User` row through `get_db`, rejects missing users, rejects `is_disabled=true`, and only then returns the user id.
- `get_current_user` uses the same active-user helper.
- Routes depending only on `get_current_user_id` now reject disabled users with already-issued valid bearer tokens.

Focused admin/user command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_admin_users.py -q
```

Result:

```text
11 passed, 26 warnings in 9.90s
```

Coverage includes:

- disabled user cannot log in.
- disabled user with an already-issued valid token cannot access `/api/users/me`.
- disabled user with an already-issued valid token cannot access `/api/frameworks/my-frameworks`.
- disabled user with an already-issued valid token cannot access `/api/frameworks/public`.
- disabled user with an already-issued valid token cannot access `/api/frameworks/fw_owner/artefacts`.
- disabled user with an already-issued valid token cannot access `/api/frameworks/push-framework`.
- re-enabled user can access `/api/users/me` and `/api/frameworks/my-frameworks` again with the same token.
- non-admin still receives 403 for admin endpoints.

Focused cumulative Phase 5 command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_framework_owner_crud.py tests\test_generation_persistence.py tests\test_framework_publish_public.py tests\test_framework_artefacts.py tests\test_admin_users.py -q
```

Result:

```text
61 passed, 136 warnings in 10.78s
```

Full backend command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
105 passed, 138 warnings in 11.22s
```

Warnings are the existing Pydantic v2 deprecation warnings, existing `datetime.utcnow()` deprecation warnings, and the Round 6 admin timestamp warnings.

## Closeout Repair Required Scans

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

Command:

```powershell
git diff -- frontend
```

Result: passed with exit code `0` and no output. No `frontend/` files were modified.

Command:

```powershell
rg -n "user_id\s*[:=].*(Body|Query|Form)|creator_id\s*[:=].*(Body|Query|Form)" backend_py\app\api
```

Result: no matches. `rg` exited `1`.

Command:

```powershell
rg -n "firestore.googleapis.com|identitytoolkit|FIREBASE_|VITE_FIREBASE_|OPENAI_VECTOR_STORE|upload_json|requests" backend_py\app\api\vector_sync.py
```

Result: no matches. `rg` exited `1`.

Command:

```powershell
backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini history --verbose
```

Result: passed with exit code `0`. The history head remains `0003_phase5_admin_user_disabled` with parent `0002_phase5_framework_publish_fields`.

Command:

```powershell
$env:DATABASE_URL='postgresql+psycopg://test:test@localhost:5432/test'; backend_py\.venv\Scripts\alembic.exe -c backend_py\alembic.ini upgrade head --sql
```

Result: passed with exit code `0`. Offline SQL includes both Phase 5 migrations:

```sql
ALTER TABLE frameworks ADD COLUMN is_public BOOLEAN DEFAULT false NOT NULL;
ALTER TABLE frameworks ADD COLUMN category VARCHAR;
ALTER TABLE frameworks ADD COLUMN tags_json JSONB DEFAULT '[]'::jsonb NOT NULL;
ALTER TABLE frameworks ADD COLUMN published_at TIMESTAMP WITHOUT TIME ZONE;
ALTER TABLE users ADD COLUMN is_disabled BOOLEAN DEFAULT false NOT NULL;
ALTER TABLE users ADD COLUMN disabled_at TIMESTAMP WITHOUT TIME ZONE;
CREATE INDEX ix_users_is_disabled ON users (is_disabled);
```

## Closeout Repair Git Tracking

Pre-closeout command:

```powershell
git status --short --untracked-files=all
```

Pre-closeout result showed the same cumulative Phase 5 untracked files that Round 6 documented:

```text
 M MIGRATION_PHASES.md
 M backend_py/app/api/frameworks.py
 M backend_py/app/api/frameworks_crud.py
 M backend_py/app/api/frameworks_shared.py
 M backend_py/app/api/generation.py
 M backend_py/app/api/users.py
 M backend_py/app/api/vector_sync.py
 M backend_py/app/auth.py
 M backend_py/app/models.py
 M backend_py/main.py
 M backend_py/scripts/seed_admin.py
 M backend_py/tests/test_auth_hardening.py
 M backend_py/tests/test_provider_abstractions.py
?? backend_py/alembic/versions/0002_phase5_framework_publish_fields.py
?? backend_py/alembic/versions/0003_phase5_admin_user_disabled.py
?? backend_py/app/api/admin_users.py
?? backend_py/app/api/artefacts.py
?? backend_py/app/api/frameworks_public.py
?? backend_py/app/services/rag/__init__.py
?? backend_py/app/services/rag/indexing.py
?? backend_py/tests/test_admin_users.py
?? backend_py/tests/test_framework_artefacts.py
?? backend_py/tests/test_framework_owner_crud.py
?? backend_py/tests/test_framework_publish_public.py
?? backend_py/tests/test_generation_persistence.py
?? docs/migration/phases/phase-05-backend-firestore-business/checklist.md
?? docs/migration/phases/phase-05-backend-firestore-business/phase-report.md
?? docs/migration/phases/phase-05-backend-firestore-business/verification.md
```

Staging command attempted:

```powershell
git add MIGRATION_PHASES.md backend_py\app\api\frameworks.py backend_py\app\api\frameworks_crud.py backend_py\app\api\frameworks_shared.py backend_py\app\api\generation.py backend_py\app\api\users.py backend_py\app\api\vector_sync.py backend_py\app\auth.py backend_py\app\models.py backend_py\main.py backend_py\scripts\seed_admin.py backend_py\tests\test_auth_hardening.py backend_py\tests\test_provider_abstractions.py backend_py\alembic\versions\0002_phase5_framework_publish_fields.py backend_py\alembic\versions\0003_phase5_admin_user_disabled.py backend_py\app\api\admin_users.py backend_py\app\api\artefacts.py backend_py\app\api\frameworks_public.py backend_py\app\services\rag\__init__.py backend_py\app\services\rag\indexing.py backend_py\tests\test_admin_users.py backend_py\tests\test_framework_artefacts.py backend_py\tests\test_framework_owner_crud.py backend_py\tests\test_framework_publish_public.py backend_py\tests\test_generation_persistence.py docs\migration\phases\phase-05-backend-firestore-business\checklist.md docs\migration\phases\phase-05-backend-firestore-business\phase-report.md docs\migration\phases\phase-05-backend-firestore-business\verification.md
```

First non-escalated result:

```text
fatal: Unable to create 'C:/Users/micha/Desktop/project/framework/.git/index.lock': Permission denied
```

Historical note: the same `git add` was retried twice with `require_escalated`; both escalation reviews timed out before approval. No commit was attempted.

Current post-staging command:

```powershell
git status --short --untracked-files=all
```

Current result, with no untracked Phase 5 files:

```text
M  MIGRATION_PHASES.md
A  backend_py/alembic/versions/0002_phase5_framework_publish_fields.py
A  backend_py/alembic/versions/0003_phase5_admin_user_disabled.py
A  backend_py/app/api/admin_users.py
A  backend_py/app/api/artefacts.py
M  backend_py/app/api/frameworks.py
M  backend_py/app/api/frameworks_crud.py
A  backend_py/app/api/frameworks_public.py
M  backend_py/app/api/frameworks_shared.py
M  backend_py/app/api/generation.py
M  backend_py/app/api/users.py
M  backend_py/app/api/vector_sync.py
M  backend_py/app/auth.py
M  backend_py/app/models.py
A  backend_py/app/services/rag/__init__.py
A  backend_py/app/services/rag/indexing.py
M  backend_py/main.py
M  backend_py/scripts/seed_admin.py
A  backend_py/tests/test_admin_users.py
M  backend_py/tests/test_auth_hardening.py
A  backend_py/tests/test_framework_artefacts.py
A  backend_py/tests/test_framework_owner_crud.py
A  backend_py/tests/test_framework_publish_public.py
A  backend_py/tests/test_generation_persistence.py
M  backend_py/tests/test_provider_abstractions.py
A  docs/migration/phases/phase-05-backend-firestore-business/checklist.md
A  docs/migration/phases/phase-05-backend-firestore-business/phase-report.md
A  docs/migration/phases/phase-05-backend-firestore-business/verification.md
```

Command:

```powershell
git diff --cached --stat
```

Result: staged Phase 5 implementation, docs, tests, and migrations are present; 28 files changed, 5423 insertions(+), 816 deletions(-).

## Historical Closeout Status

The disabled-token enforcement blocker was resolved and verified. Historical closeout verification recorded 28 staged Phase 5 files, `git status --short --untracked-files=all` showing no untracked Phase 5 files, `git diff --cached --check` passing, full backend pytest passing with 105 passed, and Alembic head `0003_phase5_admin_user_disabled`. The historical acceptance prose is not independently supported by a retained reviewer artifact; use the current ledger verdict.
