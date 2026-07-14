# Phase 05 Checklist - Backend Firestore Business Logic

## Current Reviewer Transcription - 2026-07-13

- [x] Review event `MR-2EC4192-20260713-01` records `accepted_with_documented_deferral` for Phase 5 at reviewed/accepted commit `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`.
- [ ] Historical embedded artefact versus child-row reconciliation remains `not run`; the three legacy sync routes remain authenticated HTTP 501 quarantine shells. Legacy count/identity mismatches could exist, while successful indexing/retrieval/logging remains intentionally unavailable.
- [ ] Data Reconciliation Owner triggers the reconciliation before importing legacy rows, deleting the embedded fallback, or on any mismatch. Phase 9 RAG Replacement Owner may act only after Phase 9 is authorized. These unchecked deferred conditions do not change the recorded accepted-with-deferral verdict.

## Governance Reconciliation - 2026-07-10

- [x] Create `capability-inventory.md` from historical `frontend/src/lib/firebase.js` and restrict every item to one approved disposition.
- [x] Record `742f1e79f3fb71d44ce21284999e64ca76c5060f` as the implementation commit.
- [x] Record `a2115042771d9e91e9410cf5597031f3c78bee9a` as later status wording only; neither commit proves reviewer acceptance.
- [x] Assign historical embedded `frameworks.artefacts_json` to `conditional data reconciliation` with Data Reconciliation Owner and an explicit trigger.
- [ ] Attach dated database/snapshot evidence comparing embedded artefact counts and identities with child rows, or an equivalent shape-aware audit with documented sampling and data-source provenance. The existing zero-child SQL result alone cannot prove `not applicable`; any non-zero result or partial/count/identity mismatch requires separately authorized data reconciliation. Status for this corrective remediation: `not run`.
- [x] Focused Migration Reviewer re-review was later recorded by `MR-2EC4192-20260713-01`: reviewer `Migration Reviewer Agent`, timestamp `2026-07-13T21:44:01.9648007+08:00`, verdict `accepted_with_documented_deferral`, and reviewed/accepted commit `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`. At the 2026-07-10 reconciliation this evidence had been pending and unavailable.

Historical round checkmarks and closeout prose below remain execution evidence and do not override the ledger.

## Round 1 - vector_sync Quarantine

- [x] Read `MIGRATION_PHASES.md` Phase 5 Step 5.3.
- [x] Read local `docs/skills/migration-phase-executor/SKILL.md` execution guidance.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read Phase 4 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Read `backend_py/app/api/vector_sync.py`.
- [x] Read `backend_py/app/api/frameworks.py`.
- [x] Read `backend_py/main.py`.
- [x] Read `backend_py/app/services/vectorstore/*.py`.
- [x] Read `backend_py/app/services/embedding/*.py`.
- [x] Read `backend_py/tests/test_auth_hardening.py`.
- [x] Remove Firestore REST active call paths from `backend_py/app/api/vector_sync.py`.
- [x] Remove Identity Toolkit active call paths from `backend_py/app/api/vector_sync.py`.
- [x] Remove OpenAI Vector Store upload active call paths from `backend_py/app/api/vector_sync.py`.
- [x] Ensure `vector_sync.py` does not import or call `requests`.
- [x] Ensure `vector_sync.py` does not read `FIREBASE_*`, `VITE_FIREBASE_*`, or `OPENAI_VECTOR_STORE_*`.
- [x] Add minimal `RAGIndexingService` quarantine stub under `backend_py/app/services/rag/`.
- [x] Keep `/api/frameworks/sync-library`, `/api/frameworks/push-framework`, and `/api/frameworks/log-event` routes registered.
- [x] Keep unauthenticated access protected by JWT dependency.
- [x] Return HTTP 501 after authentication for the three vector sync routes.
- [x] Include a response body that explicitly says indexing/retrieval are deferred to Phase 9.
- [x] Remove the old startup library sync loop from `backend_py/main.py`.
- [x] Keep `backend_py/app/api/frameworks.py` re-export imports intact.
- [x] Confirm `backend_py/main.py` imports normally through backend tests.
- [x] Add/update tests for unauthenticated and authenticated vector sync behavior.
- [x] Run forbidden grep check for `vector_sync.py`.
- [x] Run Python syntax check for changed backend files.
- [x] Run focused auth/vector sync tests.
- [x] Run full backend pytest.
- [x] Do not modify `frontend/`.
- [x] Do not delete Firebase SDK.
- [x] Do not modify `Library` or `PublishModal`.
- [x] Do not implement `PgVectorProvider`.
- [x] Do not implement `EmbeddingProvider`.
- [x] Do not write pgvector upsert/search/delete.
- [x] Do not add tenants/workspaces.
- [x] Do not implement Agent, RAG document upload, LLMWiki, Chat, or MCP.

## Not Completed In Round 1

- [ ] Phase 5 Step 5.1 full Firestore business capability inventory and backend parity.
- [ ] Phase 5 Step 5.2 public Library backendization.
- [ ] Phase 5 Step 5.3 real RAG indexing implementation.
- [ ] Phase 5 Step 5.4 business-level `frameworks.py` split and permission cleanup.
- [ ] Phase 5 Step 5.5 mock confidence production-path cleanup.
- [ ] Full Phase 5 completion gate.

## Round 2 - Framework Owner CRUD Contract

- [x] Read `MIGRATION_PHASES.md` Phase 5 Step 5.1 and Step 5.4.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read Phase 5 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Read `backend_py/app/api/frameworks.py`.
- [x] Read `backend_py/app/api/frameworks_crud.py`.
- [x] Read `backend_py/app/api/frameworks_shared.py`.
- [x] Read `backend_py/app/api/generation.py`.
- [x] Read `backend_py/app/auth.py`.
- [x] Read `backend_py/app/models.py`.
- [x] Read `backend_py/tests/`.
- [x] Fix the known P3 trailing EOF blank line in `backend_py/main.py`.
- [x] Add stable private owner CRUD request/response schemas.
- [x] Register `POST /api/frameworks` for private framework creation.
- [x] Keep `GET /api/frameworks/my-frameworks` owner scoped to JWT user.
- [x] Keep `GET /api/frameworks/my-frameworks/by-family` owner scoped to JWT user.
- [x] Keep `GET /api/frameworks/{framework_id}` owner scoped to JWT user.
- [x] Keep `GET /api/frameworks/{framework_id}/binding` owner scoped to JWT user.
- [x] Keep `PUT /api/frameworks/{framework_id}` owner scoped to JWT user.
- [x] Keep `DELETE /api/frameworks/{framework_id}` owner scoped to JWT user.
- [x] Ensure create owner is derived from `get_current_user_id`.
- [x] Ensure update/delete/get/binding owner checks use `get_current_user_id`.
- [x] Reject snake_case `user_id` and `creator_id` in create/update request bodies.
- [x] Do not define Body/Query/Form/Path parameters for `user_id` or `creator_id`.
- [x] Default missing/blank create `family` to `Other`.
- [x] Preserve native dict/list JSONB assignment for create and update paths.
- [x] Preserve existing generation routes without generation persistence changes.
- [x] Add focused owner CRUD tests for create/list/get/binding/update/delete.
- [x] Test A/B user isolation with 404 for cross-user get/binding/update/delete.
- [x] Test ignored legacy camelCase `creatorId` does not override JWT owner.
- [x] Test JSONB fields remain dict/list rather than JSON strings.
- [x] Run forbidden owner parameter grep.
- [x] Run `git diff --check`.
- [x] Run full backend pytest.
- [x] Do not modify `frontend/`.
- [x] Do not implement public library.
- [x] Do not implement publish/unpublish.
- [x] Do not implement artefacts CRUD.
- [x] Do not implement admin users.
- [x] Do not implement generation persistence changes.
- [x] Do not implement vector indexing or RAG retrieval.
- [x] Do not remove Firebase SDK.
- [x] Do not add tenant/workspace behavior.

## Round 3 - Generation Persistence

- [x] Read `MIGRATION_PHASES.md` Phase 5 Step 5.1, Step 5.4, and Step 5.5.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read Phase 5 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Read `backend_py/app/api/generation.py`.
- [x] Read `backend_py/app/api/frameworks_shared.py`.
- [x] Read `backend_py/app/api/frameworks_crud.py`.
- [x] Read `backend_py/app/models.py`.
- [x] Read `backend_py/tests/test_provider_abstractions.py`.
- [x] Read `backend_py/tests/test_framework_jsonb.py`.
- [x] Fix the known P3 verification wording so `main.py` import compatibility is recorded with an actual `import main` command.
- [x] Persist `generate-from-text` generated framework output to Postgres via the shared framework save helper.
- [x] Keep `generate-from-file` persistence on the shared framework save helper.
- [x] Persist every framework returned by `generate-from-files` via the shared framework save helper.
- [x] Return saved `framework_id` for single-compatible response handling.
- [x] Return saved `framework_ids` for multi-framework response handling.
- [x] Keep `creator_id` derived from the JWT dependency rather than request body data.
- [x] Preserve native dict/list JSONB assignment and avoid `json.dumps` double encoding.
- [x] Converge deterministic file metadata fallback for `generate-from-file` and `generate-from-files` through one helper.
- [x] Keep deterministic file metadata `processing_mode=direct_file_metadata`.
- [x] Restrict mock framework confidence generation to `ENV=dev` or explicit `dry_run=true`.
- [x] Add focused generation persistence tests for text, single file, multi-file, auth, JSONB native values, JWT owner, and mock guard behavior.
- [x] Run focused generation persistence tests.
- [x] Run owner parameter grep for generation/shared code.
- [x] Run mock-confidence grep for generation/shared code.
- [x] Run forbidden vector sync grep.
- [x] Run actual `import main` compatibility check.
- [x] Run `git diff --check`.
- [x] Run full backend pytest.
- [x] Do not modify `frontend/`.
- [x] Do not implement public library.
- [x] Do not implement publish/unpublish.
- [x] Do not implement artefacts CRUD.
- [x] Do not implement admin users.
- [x] Do not implement vector indexing or RAG retrieval.
- [x] Do not implement `PgVectorProvider` or `EmbeddingProvider`.
- [x] Do not implement Agent, LLMWiki, Chat, or MCP.
- [x] Do not remove Firebase SDK.
- [x] Do not add tenant/workspace behavior.

## Not Completed After Round 3

- [ ] Phase 5 Step 5.1 full Firestore business capability inventory and backend parity.
- [ ] Phase 5 Step 5.2 public Library backendization.
- [ ] Phase 5 Step 5.3 real RAG indexing implementation.
- [ ] Broader Phase 5 Step 5.4 business cleanup beyond private owner CRUD.
- [ ] Public library REST endpoints.
- [ ] Publish/unpublish workflow.
- [ ] Framework artefact child-resource API.
- [ ] Admin users backendization.
- [ ] Phase 9 RAG indexing/retrieval.
- [ ] Full Phase 5 completion gate.

## Round 4 - Publish + Authenticated Public Library

- [x] Read `MIGRATION_PHASES.md` Phase 5 Step 5.1, Step 5.2, and Step 5.4.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read Phase 5 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Read `backend_py/app/api/frameworks.py`.
- [x] Read `backend_py/app/api/frameworks_crud.py`.
- [x] Read `backend_py/app/api/frameworks_shared.py`.
- [x] Read `backend_py/app/models.py`.
- [x] Read `backend_py/alembic/versions/`.
- [x] Read `frontend/src/components/Library.jsx`.
- [x] Read `frontend/src/components/PublishModal.jsx`.
- [x] Read `backend_py/tests/`.
- [x] Add publish fields to the SQLAlchemy `Framework` model.
- [x] Add Alembic revision `0002_phase5_framework_publish_fields`.
- [x] Add `is_public` boolean with `false` default and index.
- [x] Add nullable `category` with index.
- [x] Add `tags_json` JSONB with `[]` default.
- [x] Add nullable `published_at` with index.
- [x] Add `backend_py/app/api/frameworks_public.py`.
- [x] Register `GET /api/frameworks/public` before the dynamic `/{framework_id}` CRUD route.
- [x] Register `POST /api/frameworks/{framework_id}/publish`.
- [x] Register `POST /api/frameworks/{framework_id}/unpublish`.
- [x] Keep `GET /api/frameworks/public` authenticated with the backend JWT dependency.
- [x] Keep `public != anonymous`: unauthenticated public list requests return 401/403.
- [x] Return a simplified public list item schema only.
- [x] Do not return `creator_id`, metadata JSON, raw framework JSON, or other private/raw fields in the public list.
- [x] Filter the public list to `is_public=true` and non-null `published_at`.
- [x] Sort the public list by `published_at` descending and `id` descending.
- [x] Enforce `limit` bounds with maximum `50`.
- [x] Implement cursor pagination with an opaque cursor based on `published_at` and `id`.
- [x] Keep publish/unpublish owner-only by filtering on `Framework.creator_id == JWT sub`.
- [x] Fix non-owner publish/unpublish behavior as 404.
- [x] Set `is_public=true` and `published_at=now` on publish.
- [x] Save `category`, sanitized `tags_json`, and optional `version` on publish.
- [x] Set `is_public=false` on unpublish.
- [x] Clear `published_at` on unpublish and keep `category/tags_json` unchanged.
- [x] Add focused publish/public library tests.
- [x] Test unauthenticated public list returns 401/403.
- [x] Test authenticated public list returns 200.
- [x] Test unpublished frameworks do not appear in the public list.
- [x] Test owner publish makes a framework appear in the public list.
- [x] Test owner unpublish removes a framework from the public list.
- [x] Test non-owner publish/unpublish returns 404 and does not mutate the owner row.
- [x] Test category/tags save and return through the public list.
- [x] Test `/api/frameworks/public` is not swallowed by `/{framework_id}`.
- [x] Run Alembic history.
- [x] Run Alembic offline SQL; first run without `DATABASE_URL` failed, rerun with explicit test `DATABASE_URL` passed.
- [x] Run focused publish/public tests.
- [x] Run focused Round 1/2/3/4 regression tests.
- [x] Run full backend pytest.
- [x] Run forbidden tenant/workspace/publishedToOrganization grep for backend app and Alembic.
- [x] Run forbidden vector_sync grep.
- [x] Run `git diff -- frontend`.
- [x] Do not modify `frontend/`.
- [x] Do not formally rewire `Library.jsx` or `PublishModal.jsx`.
- [x] Do not implement artefacts CRUD.
- [x] Do not implement admin users.
- [x] Do not implement generation logic beyond existing Round 3 persistence.
- [x] Do not implement vector indexing or RAG retrieval.
- [x] Do not implement `PgVectorProvider` or `EmbeddingProvider`.
- [x] Do not delete Firebase SDK.
- [x] Do not modify `AuthContext`.
- [x] Do not add organization, tenant, workspace, or `publishedToOrganization` publish behavior.
- [x] Do not implement Agent, LLMWiki, Chat, or MCP.

## Not Completed After Round 4

- [ ] Phase 5 Step 5.1 full Firestore business capability inventory and backend parity.
- [ ] Frontend `Library.jsx` REST rewiring; Phase 6 owns frontend Firebase removal and formal REST switch.
- [ ] Frontend `PublishModal.jsx` REST rewiring; Phase 6 owns frontend Firebase removal and formal REST switch.
- [ ] Framework artefact child-resource API.
- [ ] Admin users backendization.
- [ ] Phase 9 RAG indexing/retrieval.
- [ ] `PgVectorProvider` / `EmbeddingProvider` implementation.
- [ ] Agent, LLMWiki, Chat, MCP, and related later-phase work.
- [ ] Tenant/workspace/organization publishing.
- [ ] Full Phase 5 completion gate.

## Round 5 - Artefact Subresources

- [x] Read `MIGRATION_PHASES.md` Phase 5 Step 5.1.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read Phase 5 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Read `backend_py/app/models.py`.
- [x] Read `backend_py/app/api/frameworks.py`.
- [x] Read `backend_py/app/api/frameworks_crud.py`.
- [x] Read `backend_py/app/api/frameworks_public.py`.
- [x] Read `backend_py/app/api/frameworks_shared.py`.
- [x] Read `backend_py/alembic/versions/0001_phase4_postgres_pgvector.py`.
- [x] Read `backend_py/tests/`.
- [x] Add Round 4 public pagination tests for blank `?limit=`.
- [x] Add Round 4 public pagination test for `limit > 50` current behavior.
- [x] Add Round 4 public pagination test for second-page cursor.
- [x] Add Round 4 public pagination test for invalid cursor.
- [x] Do not change public library implementation behavior.
- [x] Add `backend_py/app/api/artefacts.py`.
- [x] Register artefact routes from `backend_py/app/api/frameworks.py` after public routes and before owner CRUD routes.
- [x] Implement `GET /api/frameworks/{framework_id}/artefacts`.
- [x] Implement `POST /api/frameworks/{framework_id}/artefacts`.
- [x] Implement `GET /api/frameworks/{framework_id}/artefacts/{artefact_id}`.
- [x] Implement `PUT /api/frameworks/{framework_id}/artefacts/{artefact_id}`.
- [x] Implement `DELETE /api/frameworks/{framework_id}/artefacts/{artefact_id}`.
- [x] Ensure every artefact operation first checks parent `Framework.creator_id == current_user_id`.
- [x] Ensure child get/update/delete also match both path `framework_id` and `artefact_id`.
- [x] Keep `framework_id` sourced from the path only.
- [x] Reject body fields such as `framework_id`, `user_id`, and `creator_id` on artefact mutation requests.
- [x] Keep `content_json` and `metadata_json` as native dict/list containers.
- [x] Default `ord` to `0`.
- [x] Default omitted `artefact_type` to `custom`, matching the Phase 4 schema default.
- [x] Do not migrate generated framework legacy `frameworks.artefacts_json` into the `artefacts` table.
- [x] Do not add a new Alembic revision because the Phase 4 `artefacts` table already supports this API.
- [x] Add focused artefact tests for unauthenticated access.
- [x] Add focused artefact tests for owner create/list/get/update/delete.
- [x] Add focused artefact tests for non-owner list/create/get/update/delete blocking.
- [x] Add focused artefact tests for framework-path and artefact-row binding.
- [x] Add focused artefact tests for native dict/list JSON roundtrip.
- [x] Add focused artefact tests that mutation request bodies do not accept identity or parent fields.
- [x] Add model-level cascade contract test for `Artefact.framework_id` `ondelete=CASCADE` and ORM delete-orphan cascade.
- [x] Run Python syntax check for artefact/public test files.
- [x] Run focused artefact and public pagination tests.
- [x] Run forbidden owner parameter grep.
- [x] Run forbidden tenant/workspace grep.
- [x] Run forbidden vector sync grep.
- [x] Run `git diff -- frontend`.
- [x] Run full backend pytest.
- [x] Do not modify `frontend/`.
- [x] Do not implement admin users.
- [x] Do not implement frontend REST rewiring or Firebase removal.
- [x] Do not implement RAG document upload, vector indexing, or retrieval.
- [x] Do not implement `PgVectorProvider` or `EmbeddingProvider`.
- [x] Do not add tenant/workspace behavior.
- [x] Do not implement Agent, LLMWiki, Chat, or MCP.

## Not Completed After Round 5

- [ ] Phase 5 Step 5.1 full Firestore business capability inventory and backend parity.
- [ ] Frontend `Library.jsx` REST rewiring; Phase 6 owns frontend Firebase removal and formal REST switch.
- [ ] Frontend `PublishModal.jsx` REST rewiring; Phase 6 owns frontend Firebase removal and formal REST switch.
- [ ] Frontend artefact REST rewiring; Phase 6 owns frontend REST wiring.
- [ ] Admin users backendization.
- [ ] Phase 9 RAG indexing/retrieval.
- [ ] `PgVectorProvider` / `EmbeddingProvider` implementation.
- [ ] Agent, LLMWiki, Chat, MCP, and related later-phase work.
- [ ] Tenant/workspace/organization publishing.
- [ ] Historical sync from `frameworks.artefacts_json` into `artefacts`.
- [ ] Full Phase 5 completion gate.

## Round 6 - Admin Users + Disabled User Enforcement + Integrity Cleanup

- [x] Run `git status --short` before implementation.
- [x] Identify that cumulative Phase 5 implementation, tests, Alembic revisions, and docs include untracked files that must be staged before commit/review.
- [x] Read `MIGRATION_PHASES.md` Phase 5 Step 5.1, Step 5.3, Step 5.4, Step 5.5, and acceptance context.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read Phase 5 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Read `backend_py/app/api/users.py`.
- [x] Read `backend_py/app/auth.py`.
- [x] Read `backend_py/app/models.py`.
- [x] Read `backend_py/scripts/seed_admin.py`.
- [x] Read `backend_py/main.py`.
- [x] Read `backend_py/alembic/versions/`.
- [x] Read `backend_py/tests/`.
- [x] Read `frontend/src/components/AdminPanel.jsx` and admin-related `frontend/src/lib/firebase.js` only as parity reference.
- [x] Add backend-only `/api/admin/users` route module.
- [x] Register the admin users router in `backend_py/main.py`.
- [x] Enforce admin access in the backend with `SUPER_ADMIN_EMAIL`.
- [x] Keep the User model without an `is_admin` column.
- [x] Implement admin-only user listing.
- [x] Ensure admin user listing responses do not include `password_hash`.
- [x] Implement admin-only user creation with plaintext password input and Argon2id hashed storage.
- [x] Reject `password_hash` in admin create-user request bodies.
- [x] Document and test that admin-created users explicitly bypass `ALLOWED_EMAILS` because creation is admin-only.
- [x] Keep `/api/users/register` disabled by default.
- [x] Keep first admin creation through `backend_py/scripts/seed_admin.py`; no HTTP seed endpoint added.
- [x] Add `is_disabled` and `disabled_at` to the SQLAlchemy User model.
- [x] Add Alembic revision `0003_phase5_admin_user_disabled`.
- [x] Update `seed_admin.py` so the configured super-admin is created/enforced as enabled.
- [x] Implement admin-only disable user endpoint.
- [x] Implement admin-only enable user endpoint.
- [x] Prevent disabling the configured super-admin/self.
- [x] Reject disabled users at login.
- [x] Reject disabled users through `get_current_user`, including `/api/users/me` and admin-protected routes.
- [x] Record that routes using only `get_current_user_id` do not perform immediate disabled-user DB checks in this round; superseded by the Phase 5 closeout repair below.
- [x] Update canonical Phase 5 Step 5.3 wording in `MIGRATION_PHASES.md` to match the accepted quarantine/stub split.
- [x] Keep Phase 9 responsible for real embedding, pgvector upsert/search, indexing, and retrieval.
- [x] Add focused admin user tests.
- [x] Run Python syntax checks for Round 6 code/tests/migration.
- [x] Run focused admin user tests.
- [x] Run cumulative Phase 5 regression tests.
- [x] Run full backend pytest.
- [x] Run Alembic history and offline SQL.
- [x] Run requested owner/password hash, tenant/workspace, vector/Firebase, admin/env scans.
- [x] Run `git diff -- frontend` and confirm no frontend diff.
- [x] Run `git diff --check`.
- [x] Do not modify frontend files.
- [x] Do not implement Phase 6 frontend REST/Firebase removal.
- [x] Do not delete Firebase SDK.
- [x] Do not rewrite `AdminPanel.jsx`.
- [x] Do not add tenants, workspaces, organization members, or invites.
- [x] Do not implement public registration.
- [x] Do not implement OAuth/Authing.
- [x] Do not implement RAG embedding, pgvector indexing, retrieval, `PgVectorProvider`, or `EmbeddingProvider`.
- [x] Do not implement Agent, LLMWiki, Chat, or MCP.
- [x] Do not create new Firebase configuration or write real API keys.

## Phase 5 Closeout Repair - Tracking + Disabled Token Enforcement

- [x] Run `git status --short --untracked-files=all` before closeout repair.
- [x] Identify all untracked cumulative Phase 5 implementation, docs, tests, RAG stub, and Alembic migration files.
- [x] Update `get_current_user_id` so it decodes the JWT, loads the `User` row, and rejects missing or disabled users.
- [x] Keep `get_current_user` on the same active-user validation helper.
- [x] Verify disabled users still cannot log in.
- [x] Verify disabled users with an already-issued valid token cannot access `/api/users/me`.
- [x] Verify disabled users with an already-issued valid token cannot access `/api/frameworks/my-frameworks`.
- [x] Verify disabled users with an already-issued valid token cannot access `/api/frameworks/public`.
- [x] Verify disabled users with an already-issued valid token cannot access an artefact route.
- [x] Verify disabled users with an already-issued valid token cannot access a vector sync route.
- [x] Verify an enabled user can access again after re-enable.
- [x] Verify non-admin users still cannot access admin endpoints.
- [x] Update fake DB fixtures in route tests so they exercise the real active-user dependency.
- [x] Run focused admin user tests.
- [x] Run cumulative Phase 5 regression tests.
- [x] Run full backend pytest.
- [x] Run `git diff --check`.
- [x] Run `git diff -- frontend`.
- [x] Run owner parameter grep for `user_id` / `creator_id` Body/Query/Form.
- [x] Run forbidden external-path grep for `vector_sync.py`.
- [x] Run Alembic history and offline SQL because Phase 5 migration files are staged for closeout.
- [x] Stage all 28 Phase 5 files required for a coherent commit; earlier sandbox `.git/index.lock` failures were later superseded by successful staging.
- [x] Run `git status --short --untracked-files=all` after staging and record no untracked Phase 5 files.
- [x] Run `git diff --cached --stat` after staging and record 28 files changed, 5423 insertions, 816 deletions.
- [x] Do not modify `frontend/`.
- [x] Do not implement Phase 6 frontend REST/Firebase removal.
- [x] Do not implement RAG/Agent/LLMWiki/Chat/MCP.
- [x] Do not commit.

## Historical Closeout Note (not the current ledger verdict)

- Historical prose states that Phase 5 final review accepted the closeout and the package was committed/pushed. No original reviewer identity/date/raw verdict artifact is retained, so this statement does not establish the current ledger verdict.

## Remaining Deferred After Closeout
- [ ] Phase 9 RAG indexing/retrieval, embedding, pgvector upsert/search, and citation retrieval.
- [ ] Phase 6 frontend REST rewiring and Firebase SDK removal.
- [ ] Phase 7 tenant/domain cleanup.
- [ ] Agent, LLMWiki, Chat, MCP, and related later-phase work.
- [ ] Historical sync from `frameworks.artefacts_json` into `artefacts`.
