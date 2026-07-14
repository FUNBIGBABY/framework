# Phase 05 Report - Backend Firestore Business Logic

## Current Reviewer Transcription - 2026-07-13

- Review event `MR-2EC4192-20260713-01` records verdict `accepted_with_documented_deferral` at reviewed/accepted commit `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`.
- Condition: historical embedded artefact versus child-row reconciliation remains `not run`; the three legacy sync routes remain authenticated HTTP 501 quarantine shells.
- Residual risk: legacy artefact count/identity mismatches could exist; successful indexing/retrieval/logging is intentionally unavailable.
- Owners/triggers: Data Reconciliation Owner acts before importing legacy rows, deleting the embedded fallback, or on any mismatch; Phase 9 RAG Replacement Owner acts only after that phase is authorized.
- This accepted-with-deferral verdict does not claim a live data inspection and does not authorize or implement Phase 9.

## Governance Reconciliation - 2026-07-10

- At the 2026-07-10 reconciliation, the ledger verdict was `pending`; the 2026-07-13 named review transcription above supersedes that statement for current status without deleting this historical record.
- `742f1e79f3fb71d44ce21284999e64ca76c5060f` is the implementation commit.
- `a2115042771d9e91e9410cf5597031f3c78bee9a` added later status wording. Neither commit independently proves reviewer acceptance.
- At the 2026-07-10 reconciliation, the original reviewer identity, date, and raw verdict artifact were unavailable and focused re-review was required; `MR-2EC4192-20260713-01` now supplies the current named re-review artifact.
- `capability-inventory.md` is the superseding capability disposition for historical `firebase.js`.
- Historical embedded artefacts are `conditional data reconciliation`, owned by Data Reconciliation Owner and triggered by legacy-data import, removal of the embedded fallback, any embedded-with-zero-child result, or any partial/count/identity mismatch. The existing SQL detects only non-empty embedded artefacts with zero child rows; a zero result cannot alone establish `not applicable`. Shape-aware count/identity comparison, or equivalent audit evidence with sampling and data-source provenance, is still required. This repair did not inspect a live database; status remains `not run`.

The round-by-round report below remains historical execution evidence.

## Scope

This report records Phase 5 Round 1, Round 2, Round 3, Round 4, Round 5, Round 6, and closeout repair status.

Round 1 does not complete Phase 5. It removes the active Firestore REST, Identity Toolkit, and OpenAI Vector Store upload paths from the backend vector sync API surface, while preserving the existing routes as authenticated endpoints that return HTTP 501. Real indexing and retrieval remain deferred to Phase 9.

Round 2 does not complete Phase 5. It adds the private owner Framework CRUD contract only. Public library, publish/unpublish, artefact child resources, admin users, generation persistence, and Phase 9 RAG remain outside this round.

Round 3 does not complete Phase 5. It migrates generation persistence for `generate-from-text`, `generate-from-file`, and `generate-from-files` so generated Framework rows are saved in Postgres under the authenticated JWT user. It also converges deterministic file metadata fallback and restricts mock confidence generation to `ENV=dev` or explicit `dry_run=true`. Public library, publish/unpublish, artefact child resources, admin users, and Phase 9 RAG remain outside this round.

Round 4 does not complete Phase 5. It implements the backend-owned publish/unpublish semantics and an authenticated public library endpoint for later frontend consumption. It adds publish fields to the Postgres model and Alembic history, keeps `/api/frameworks/public` authenticated, fixes non-owner publish/unpublish as 404, and returns only a simplified public-library schema. Frontend Firebase removal, formal `Library.jsx` / `PublishModal.jsx` REST rewiring, artefact child resources, admin users, tenant/workspace publishing, and Phase 9 RAG remain outside this round.

Round 5 does not complete Phase 5. It implements backend REST CRUD for framework `artefacts` subresources on the Phase 4 `artefacts` table and adds the missing Round 4 public pagination regression tests. Artefact routes are authenticated, owner-gated through the parent framework, and keep JSONB `content_json` / `metadata_json` as native dict/list containers. Frontend REST wiring, Firebase SDK removal, admin users, tenant/workspace publishing, historical sync from legacy `frameworks.artefacts_json`, and Phase 9 RAG remain outside this round.

Round 6 implements backend-only admin user management at `/api/admin/users`, adds disabled-user fields and enforcement, and cleans up the Phase 5 Step 5.3 canonical wording conflict. Admin authority is derived only from `SUPER_ADMIN_EMAIL` in the backend. Admin-created users are an explicit admin-only bypass of `ALLOWED_EMAILS`; public `/api/users/register` remains disabled by default. Disabled users cannot log in and are rejected by `get_current_user`, including `/api/users/me` and admin-protected routes.

Closeout repair resolves the disabled-token full-review blocker: `get_current_user_id` now performs a database active-user check so disabled users with already-issued valid JWTs are rejected on private routes that use the ID-only dependency. The earlier untracked-file/staging blocker is resolved: 28 Phase 5 files are staged with 5423 insertions and 816 deletions, and no untracked Phase 5 files remain.

## Round 1 Files Changed

- `backend_py/app/api/vector_sync.py`
- `backend_py/app/services/rag/__init__.py`
- `backend_py/app/services/rag/indexing.py`
- `backend_py/main.py`
- `backend_py/tests/test_auth_hardening.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

No `frontend/` files were modified.

## Implementation Notes

- `vector_sync.py` now keeps the three legacy route names:
  - `POST /api/frameworks/sync-library`
  - `POST /api/frameworks/push-framework`
  - `POST /api/frameworks/log-event`
- Each route still depends on `get_current_user_id`, so unauthenticated requests remain blocked with 401/403.
- After authentication, each route calls `RAGIndexingService`, which raises `RAGIndexingDeferredError`.
- The API maps that service exception to HTTP 501 with a body that states RAG indexing and retrieval are deferred to Phase 9.
- The old Firestore document parsing, Identity Toolkit token creation, OpenAI Vector Store `upload_json`, vector store provider lookup, and `requests` imports were removed from `vector_sync.py`.
- The old `main.py` startup loop that could call `sync_library` with `current_user_id="startup-sync"` was removed. This prevents a background path from bypassing normal request authentication or reintroducing old external sync behavior.
- `backend_py/app/api/frameworks.py` was left structurally intact and still re-exports `SyncLibraryRequest`, `PushFrameworkRequest`, `EventLogRequest`, `sync_library`, `push_framework`, and `log_event`.

## Boundaries Honored

- Did not implement `PgVectorProvider`.
- Did not implement `EmbeddingProvider`.
- Did not add pgvector upsert, search, or delete behavior.
- Did not call OpenAI Vector Store from the API.
- Did not call Firestore REST from the API.
- Did not call Identity Toolkit from the API.
- Did not add tenants or workspaces.
- Did not implement Agent, RAG document upload, LLMWiki, Chat, or MCP.
- Did not remove the Firebase SDK.
- Did not modify `Library` or `PublishModal`.

## Round 2 Scope

Round 2 implemented the private owner CRUD REST surface for frameworks:

- `POST /api/frameworks`
- `GET /api/frameworks/my-frameworks`
- `GET /api/frameworks/my-frameworks/by-family`
- `GET /api/frameworks/{framework_id}`
- `GET /api/frameworks/{framework_id}/binding`
- `PUT /api/frameworks/{framework_id}`
- `DELETE /api/frameworks/{framework_id}`

All owner decisions in these routes are derived from the JWT dependency `get_current_user_id`. The create path sets `Framework.creator_id` from the token subject, not from request body data. Existing get/update/delete/binding/list queries are owner-filtered by `Framework.creator_id == user_id`.

Round 2 uses 404 for cross-user access to another user's framework. Tests now fix that behavior for get, binding, update, and delete.

## Round 2 Files Changed

- `backend_py/app/api/frameworks.py`
- `backend_py/app/api/frameworks_crud.py`
- `backend_py/app/api/frameworks_shared.py`
- `backend_py/main.py`
- `backend_py/tests/test_framework_owner_crud.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

No `frontend/` files were modified in Round 2.

## Round 2 Implementation Notes

- Added `FrameworkCreateRequest`, `FrameworkUpdateRequest`, and `FrameworkMutationResponse` schemas.
- Create and update request schemas do not expose `user_id` or `creator_id`.
- Snake_case `user_id` and `creator_id` in create/update request bodies return FastAPI validation errors.
- Extra legacy body fields are ignored, so camelCase `creatorId` does not override the JWT owner.
- `POST /api/frameworks` is registered on the aggregate router to preserve the no-trailing-slash REST path.
- Missing or blank create `family` defaults to `Other`, matching the non-null database column.
- JSONB fields continue to be assigned as native Python dict/list values. No `json.dumps` path was added.
- Legacy `_raw` JSON text is parsed back to native JSON before assignment, preventing double-encoded JSON strings.
- `GET /api/frameworks/{framework_id}/binding` remains owner protected and now prefers the stored `pov` column, with native raw JSON fallback.
- The known P3 trailing EOF blank line in `backend_py/main.py` was removed.

## Round 2 Boundaries Honored

- Did not implement public library.
- Did not implement publish/unpublish.
- Did not implement artefacts CRUD.
- Did not implement admin users.
- Did not implement generation persistence changes.
- Did not implement vector indexing or RAG retrieval.
- Did not remove Firebase SDK.
- Did not add tenant/workspace behavior.
- Did not modify `frontend/`.

## Round 3 Scope

Round 3 implemented generation persistence for the existing authenticated generation routes:

- `POST /api/frameworks/generate-from-text`
- `POST /api/frameworks/generate-from-file`
- `POST /api/frameworks/generate-from-files`

All three routes keep deriving the owner from the JWT dependency `get_current_user_id`. Request body or form fields named `user_id` or `creator_id` are not accepted as route parameters and are not trusted for persistence.

The response remains backward-compatible through `framework_id`, `framework`, `frameworks`, and `metadata`, and now also includes `framework_ids` when one or more frameworks were saved.

## Round 3 Files Changed

- `backend_py/app/api/generation.py`
- `backend_py/app/api/frameworks_shared.py`
- `backend_py/tests/test_generation_persistence.py`
- `backend_py/tests/test_provider_abstractions.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

No `frontend/` files were modified in Round 3.

## Round 3 Implementation Notes

- Added `framework_ids` to `GenerateResponse` while preserving the existing `framework_id` field.
- Added `dry_run` to text generation request handling and file generation query handling.
- Added `should_use_mock_generation(dry_run)` so mock framework generation is allowed only when `ENV=dev` or `dry_run=true`.
- `process_with_global_llm(..., use_mock=True)` now returns HTTP 503 outside those allowed mock contexts instead of silently calling `calculate_mock_confidence`.
- Added a single generation persistence helper that calls `save_framework_to_db` for each generated framework and returns the saved IDs.
- `generate-from-text` now saves generated framework rows to Postgres.
- `generate-from-file` continues to save generated framework rows, now returning both `framework_id` and `framework_ids`.
- `generate-from-files` now saves every generated framework row instead of generating unsaved client-side IDs.
- `generate-from-file` and `generate-from-files` now share `build_deterministic_file_metadata_from_paths`, which delegates to `build_deterministic_file_metadata`.
- Deterministic file metadata now consistently records `processing_mode=direct_file_metadata`.
- JSONB fields continue to be assigned native Python dict/list values through `save_framework_to_db`; no `json.dumps` double-encoding path was added.

## Round 3 Boundaries Honored

- Did not implement public library.
- Did not implement publish/unpublish.
- Did not implement artefacts CRUD.
- Did not implement admin users.
- Did not implement vector indexing or RAG retrieval.
- Did not implement `PgVectorProvider`.
- Did not implement `EmbeddingProvider`.
- Did not implement Agent, LLMWiki, Chat, or MCP.
- Did not remove Firebase SDK.
- Did not add tenants or workspaces.
- Did not modify `frontend/`.

## Round 4 Scope

Round 4 implemented backend-owned publish semantics and the authenticated public library API:

- `POST /api/frameworks/{framework_id}/publish`
- `POST /api/frameworks/{framework_id}/unpublish`
- `GET /api/frameworks/public?cursor=&limit=20`

All three endpoints require the backend JWT dependency. `GET /api/frameworks/public` is public-library data, but it is not anonymous access. Unauthenticated requests return 401/403 before any database data is returned.

Publish and unpublish are owner-only operations. Round 4 follows the Round 2 owner CRUD convention and returns 404 when another authenticated user attempts to publish or unpublish a framework they do not own.

## Round 4 Files Changed

- `backend_py/app/api/frameworks.py`
- `backend_py/app/api/frameworks_public.py`
- `backend_py/app/models.py`
- `backend_py/alembic/versions/0002_phase5_framework_publish_fields.py`
- `backend_py/tests/test_framework_publish_public.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

No `frontend/` files were modified in Round 4.

## Round 4 DB Changes

Alembic revision `0002_phase5_framework_publish_fields` adds these columns to `frameworks`:

- `is_public` boolean, not null, server default `false`, indexed.
- `category` string, nullable, indexed.
- `tags_json` JSONB, not null, server default `[]`.
- `published_at` datetime, nullable, indexed.

No tenant, workspace, organization, or `publishedToOrganization` column was added.

## Round 4 Implementation Notes

- Added `backend_py/app/api/frameworks_public.py` and included it in `backend_py/app/api/frameworks.py` before `frameworks_crud.router`, so `/api/frameworks/public` is resolved before the dynamic `/{framework_id}` route.
- `publish` sets `is_public=true`, sets `published_at` to the current UTC timestamp, updates `updated_at`, stores optional `version`, stores `category`, and stores sanitized tags in `tags_json`.
- If publish is called without a category and the framework has no stored category, the backend defaults category to the framework family or `Other`.
- Tags are trimmed, deduplicated, capped to 20 tags, and each tag is capped to 80 characters.
- `unpublish` sets `is_public=false`, clears `published_at`, updates `updated_at`, and leaves `category` and `tags_json` unchanged for possible future republish.
- The public library query returns only rows where `is_public=true` and `published_at` is not null.
- The public library response is an object with `items`, `next_cursor`, and `limit`. Each item contains only `id`, `title`, `version`, `family`, `confidence`, `category`, `tags`, `published_at`, `updated_at`, and `preview_artefacts`.
- The public library response does not expose `creator_id`, metadata JSON, raw framework JSON, steps, risks, escalation, or other private/raw JSON fields.
- Pagination uses `limit` with FastAPI validation bounds `1..50`. Cursor pagination is implemented with an opaque token containing the last item's `published_at` and `id`, ordered by `published_at desc, id desc`.

## Round 4 Boundaries Honored

- Did not implement artefacts CRUD.
- Did not implement admin users.
- Did not implement generation logic beyond the existing Round 3 persistence work.
- Did not implement vector indexing or RAG retrieval.
- Did not implement `PgVectorProvider`.
- Did not implement `EmbeddingProvider`.
- Did not delete Firebase SDK.
- Did not modify `AuthContext`.
- Did not formally rewire `Library.jsx` or `PublishModal.jsx`.
- Did not add tenant, workspace, organization, or `publishedToOrganization` publish behavior.
- Did not implement Agent, LLMWiki, Chat, or MCP.
- Did not modify `frontend/`.

## Round 5 Scope

Round 5 implemented backend-owned artefact subresource semantics for:

- `GET /api/frameworks/{framework_id}/artefacts`
- `POST /api/frameworks/{framework_id}/artefacts`
- `GET /api/frameworks/{framework_id}/artefacts/{artefact_id}`
- `PUT /api/frameworks/{framework_id}/artefacts/{artefact_id}`
- `DELETE /api/frameworks/{framework_id}/artefacts/{artefact_id}`

All five endpoints require the backend JWT dependency. They first load the parent `Framework` with both `Framework.id == framework_id` and `Framework.creator_id == current_user_id`. Child get/update/delete then load the `Artefact` with both the path `framework_id` and the path `artefact_id`, so an artefact row cannot be reached through a different framework path.

Round 5 also completed a small Round 4 cleanup by pinning current public-library pagination behavior:

- blank `?limit=` returns FastAPI validation status `422`.
- `limit=51` returns FastAPI validation status `422` because Round 4 capped the limit at `50`.
- a second-page cursor returns the next page under the existing `published_at desc, id desc` ordering.
- an invalid cursor returns `400` with `Invalid public library cursor`.

No public-library behavior was changed.

## Round 5 Files Changed

- `backend_py/app/api/frameworks.py`
- `backend_py/app/api/artefacts.py`
- `backend_py/tests/test_framework_artefacts.py`
- `backend_py/tests/test_framework_publish_public.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

No `frontend/` files were modified in Round 5.

## Round 5 DB Changes

No new Alembic revision was added.

Reason: Phase 4 already created the `artefacts` table with the fields required by this round:

- `id`
- `framework_id`
- `name`
- `artefact_type`
- `content_json`
- `metadata_json`
- `ord`
- `created_at`
- `updated_at`

The Phase 4 schema already has `framework_id` indexed, an `(framework_id, ord)` index, and an `ondelete="CASCADE"` foreign key to `frameworks.id`. The SQLAlchemy model also has `Framework.artefact_rows` configured with `cascade="all, delete-orphan"`.

## Round 5 Implementation Notes

- Added `backend_py/app/api/artefacts.py` with local Pydantic request/response schemas.
- Included `artefacts.router` from the aggregate `backend_py/app/api/frameworks.py` router after `frameworks_public.router` and before the owner CRUD router.
- `POST /api/frameworks/{framework_id}/artefacts` creates `Artefact.framework_id` only from the path after parent owner verification.
- Mutation request schemas use `extra="forbid"`, so body fields such as `framework_id`, `user_id`, and `creator_id` are not accepted.
- `ord` defaults to `0`.
- Omitted `artefact_type` defaults to `custom`, matching the Phase 4 server default.
- `content_json` and `metadata_json` accept dict/list JSON containers and are assigned directly as Python values. No `json.dumps` path was added.
- `GET /api/frameworks/{framework_id}/artefacts` returns owner-visible artefacts ordered by `ord`, then `created_at`, then `id`.
- `GET`, `PUT`, and `DELETE` for a single artefact require both the parent framework owner check and an artefact row matching the path framework id.
- Deleting an artefact deletes only the child row and returns a small mutation response.
- Deleting a framework is covered by the existing Phase 4 database FK `ondelete=CASCADE` and ORM `delete-orphan` relationship configuration. Round 5 added a model-level test for this contract.
- Generated framework legacy `frameworks.artefacts_json` values were not backfilled or synchronized into the new `artefacts` child table. That remains deferred.

## Round 5 Boundaries Honored

- Did not implement admin users.
- Did not implement frontend REST wiring.
- Did not remove Firebase SDK.
- Did not modify `Library.jsx`, `PublishModal.jsx`, or any other `frontend/` file.
- Did not implement RAG document upload, vector indexing, or retrieval.
- Did not implement `PgVectorProvider`.
- Did not implement `EmbeddingProvider`.
- Did not add tenants or workspaces.
- Did not add public organization sharing.
- Did not implement Agent, LLMWiki, Chat, or MCP.
- Did not create a new Firebase project or write real API keys.
- Did not migrate legacy `frameworks.artefacts_json` values into the `artefacts` table.

## Round 6 Scope

Round 6 implemented the backend admin user API:

- `GET /api/admin/users`
- `POST /api/admin/users`
- `POST /api/admin/users/{user_id}/disable`
- `POST /api/admin/users/{user_id}/enable`

All four endpoints require an authenticated user whose email exactly matches `SUPER_ADMIN_EMAIL` after normalization. Non-admin authenticated users receive 403, and unauthenticated requests are rejected by the existing bearer auth dependency.

## Round 6 Files Changed

- `MIGRATION_PHASES.md`
- `backend_py/app/api/admin_users.py`
- `backend_py/app/api/users.py`
- `backend_py/app/auth.py`
- `backend_py/app/models.py`
- `backend_py/main.py`
- `backend_py/scripts/seed_admin.py`
- `backend_py/alembic/versions/0003_phase5_admin_user_disabled.py`
- `backend_py/tests/test_admin_users.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

No `frontend/` files were modified in Round 6.

## Round 6 DB Changes

Alembic revision `0003_phase5_admin_user_disabled` adds these columns to `users`:

- `is_disabled` boolean, not null, server default `false`, indexed.
- `disabled_at` datetime, nullable.

The SQLAlchemy User model maps the same fields. No `is_admin`, tenant, workspace, organization, member, or invite columns were added.

## Round 6 Implementation Notes

- `backend_py/app/api/admin_users.py` contains the new admin-only API.
- Admin checks run in the backend and use `SUPER_ADMIN_EMAIL`; frontend admin button hiding is not trusted.
- The User model still intentionally has no `is_admin` column.
- User list responses include derived `is_super_admin`, `is_disabled`, and `disabled_at`, but do not expose `password_hash`.
- Admin create accepts plaintext `password`, hashes it with the existing Argon2id helper, and rejects request bodies containing `password_hash`.
- Admin create explicitly bypasses `ALLOWED_EMAILS` because it is admin-only account creation. `ALLOWED_EMAILS` still applies to public registration when public registration is enabled.
- Public `/api/users/register` remains disabled by default through `ENABLE_PUBLIC_REGISTER=false`.
- `seed_admin.py` still creates the first administrator through the CLI path and now ensures the configured super-admin is enabled.
- `disable` sets `is_disabled=true` and `disabled_at=now`.
- `enable` sets `is_disabled=false` and clears `disabled_at`.
- Disabling the configured super-admin/self returns 400 to avoid lockout.
- `login_user` rejects disabled users after password verification.
- `get_current_user` rejects disabled users, covering `/api/users/me` and admin-protected endpoints.
- Closeout repair supersedes the Round 6 limitation for ID-only dependencies: `get_current_user_id` now validates that the token subject maps to an existing, enabled `User` row before returning the user id.

## Round 6 MIGRATION_PHASES.md Change

`MIGRATION_PHASES.md` was changed only for Phase 5 Step 5.3. The old wording required Phase 5 to implement embedding plus `VectorStoreProvider.upsert_vectors(...)`; that conflicted with the accepted Round 1 quarantine/stub split. The new wording says Phase 5 quarantines Firestore REST / Identity Toolkit / OpenAI Vector Store active paths and keeps `RAGIndexingService.index_framework(...)` as an authenticated 501 stub, while real embedding, pgvector upsert/search, indexing, and retrieval remain Phase 9 work.

## Round 6 Boundaries Honored

- Did not modify `frontend/`.
- Did not rewire `AdminPanel.jsx`.
- Did not implement Phase 6 frontend REST/Firebase removal.
- Did not delete Firebase SDK.
- Did not add tenant, workspace, organization member, or invite behavior.
- Did not implement public registration.
- Did not implement OAuth or Authing.
- Did not implement RAG embedding, pgvector indexing, retrieval, `PgVectorProvider`, or `EmbeddingProvider`.
- Did not implement Agent, LLMWiki, Chat, or MCP.
- Did not create a new Firebase project or write real API keys.

## Phase 5 Closeout Repair Scope

Closeout repair fixes the full-review findings after behaviorally accepted Rounds 1-6:

- The `get_current_user_id` dependency now decodes the bearer token, loads the `User` row, and rejects missing or disabled users before returning the id.
- `get_current_user` uses the same active-user helper, keeping `/api/users/me` and admin routes consistent with ID-only private routes.
- Disabled users with already-issued valid tokens are rejected by `/api/users/me`, `/api/frameworks/my-frameworks`, `/api/frameworks/public`, an artefact route, and a vector sync route.
- Re-enabled users can access again with the same already-issued token.
- The test fake DB fixtures were updated to exercise the real active-user dependency instead of relying on token-only auth behavior.
- All cumulative Phase 5 implementation, tests, migrations, RAG stub files, and docs were identified for staging. Earlier staging attempts failed on sandbox `.git/index.lock` permissions, but a later staging pass succeeded for all 28 Phase 5 files.

## Phase 5 Closeout Repair Files Changed

- `backend_py/app/auth.py`
- `backend_py/tests/test_admin_users.py`
- `backend_py/tests/test_auth_hardening.py`
- `backend_py/tests/test_framework_artefacts.py`
- `backend_py/tests/test_framework_owner_crud.py`
- `backend_py/tests/test_framework_publish_public.py`
- `backend_py/tests/test_generation_persistence.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

No `frontend/` files were modified in closeout repair.

## Phase 5 Tracking Status

Resolved in Git after the earlier sandbox failure. Historical `git add` attempts failed because `.git/index.lock` writes were blocked and escalation timed out, but current `git status --short --untracked-files=all` shows no untracked Phase 5 files, and `git diff --cached --stat` shows 28 staged files with 5423 insertions and 816 deletions.

Previously untracked Phase 5 files now staged include:

- `backend_py/alembic/versions/0002_phase5_framework_publish_fields.py`
- `backend_py/alembic/versions/0003_phase5_admin_user_disabled.py`
- `backend_py/app/api/admin_users.py`
- `backend_py/app/api/artefacts.py`
- `backend_py/app/api/frameworks_public.py`
- `backend_py/app/services/rag/__init__.py`
- `backend_py/app/services/rag/indexing.py`
- `backend_py/tests/test_admin_users.py`
- `backend_py/tests/test_framework_artefacts.py`
- `backend_py/tests/test_framework_owner_crud.py`
- `backend_py/tests/test_framework_publish_public.py`
- `backend_py/tests/test_generation_persistence.py`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

## Historical Implementation Completion Status

Phase 5 Round 1 is complete.

Phase 5 Round 2 is complete.

Phase 5 Round 3 is complete.

Phase 5 Round 4 is complete.

Phase 5 Round 5 is complete.

Phase 5 Round 6 is complete.

Phase 5 closeout repair implementation and Git staging are complete; staging now contains 28 Phase 5 files.

Historical prose recorded Phase 5 as accepted, committed, and pushed. Because the original reviewer artifact is unavailable, that prose is not the current verdict; see `docs/migration/REVIEW_LEDGER.md`. The disabled-token implementation evidence remains part of this historical report. Real indexing/retrieval remains explicitly deferred to Phase 9. Frontend REST rewiring/Firebase removal remained Phase 6. Tenant/domain cleanup remained Phase 7. Agent, LLMWiki, Chat, and MCP were not started.
