# Phase 06 Round 0/1/2/3/4/5/6 Report - Frontend de-Firebase

## Current Audit Correction

`P6-DEFIREBASE-CORRECTION-01` supersedes the status assertions below without
deleting their historical evidence. The current audit-grade verdict is
`pending`; `27679f8ff832a70a7f69782d8d45a52eab343525` is an implementation
candidate only, `accepted_commit` is absent, and reviewer identity, reviewed
SHA, review date, and raw verdict artifact remain unavailable. Phase 7 remains
`pending`, so the Phase 8 gate remains closed.

## Governance Reconciliation - 2026-07-10

Historical owner handoff states `accepted_with_documented_deferral` for browser smoke on reviewed implementation commit `27679f8ff832a70a7f69782d8d45a52eab343525`. The repository does not retain the original reviewer identity, review date, or raw verdict artifact, so those fields are `artifact unavailable` and require focused re-review before the evidence is audit-grade. This does not downgrade the historical verdict.

Browser smoke remains `not run`. The recorded blocker is an unavailable Docker Desktop Linux engine plus no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded admin credentials. Migration Verification Owner owns the condition; trigger when the complete authorized environment becomes available, before a release relying on these browser flows, or as an explicit later reviewer condition. Missing smoke is not automatically a blocker.

Round 0/1/2/3/4/5/6 implementation status: Round 0 inventory, Round 1 cookie-session/AuthContext foundation, Round 2 core framework REST wiring, Round 2 review repairs, Round 3 Library plus publish/unpublish REST wiring, Round 4 Admin users REST wiring, Round 5 artefact child-resource UI wiring, and Round 6 Firebase SDK removal/Bearer closeout have been implemented with static scan, lint, unit-test, backend-test, and build verification. Phase 6 closeout was accepted by Migration Reviewer with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable. Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.

## Status

This report is now the Round 0/1/2/3/4/5/6 implementation and review-repair record. Earlier planning-only wording has been superseded; Phase 6 closeout acceptance is recorded here after Migration Reviewer accepted Round 6.

Current Phase 6 status:

- Planning package created: `checklist.md`, `phase-plan.md`, `verification.md`, and this `phase-report.md`.
- Canonical auth route decision recorded: Phase 6 uses only the `/api/users/*` auth route family.
- Round 0, Round 1, Round 2, Round 3, Round 4, Round 5, and Round 6 implementation is complete with recorded static scan, lint, test, backend-test, and build verification.
- Historical Phase 6 verdict is `accepted_with_documented_deferral`; original reviewer artifact is unavailable for independent audit.
- Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable; this report does not claim browser smoke was run.
- Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- Current repair passes fix the Round 2 update payload, route-gate, tenant-modal, and verification wording review findings.
- Round 1 repaired backend cookie-session support because the Phase 1 token strategy debt was still present.
- Protected backend endpoints now read only the access cookie; Bearer compatibility has been removed and Bearer credentials are rejected.
- Shared frontend API requests now attempt one `/api/users/refresh` on normal expired-access `401` responses, then retry the original request once.
- CSRF/Origin/Referer verification requirements are explicit.
- Phase 5 final review accepted the closeout; Phase 6 planning may proceed.
- Phase 7 may use the accepted Phase 6 closeout status recorded in this report, `checklist.md`, and `verification.md`.

## Earlier Round 2 Review Repair Scope

This historical repair fixed only the remaining Round 2 review findings. Rounds 3, 4, 5, and 6 are now implemented, and Migration Reviewer accepted the Phase 6 closeout after Round 6.

Frontend files changed by this repair:

- `frontend/src/App.jsx`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/TenantRoute.jsx`
- `frontend/src/components/CreateFramework.jsx`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/App.route.test.jsx`
- `frontend/src/components/Login.test.jsx`
- `frontend/src/components/TenantRoute.test.jsx`

Documentation files changed by this repair:

- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`

Implementation decisions:

- `AuthContext` still builds backend-cookie users with `tenantId: null`; this repair does not invent a tenant, workspace, or SaaS ownership model.
- `Login.jsx` now sends successful backend-cookie logins without `tenantId` to `/personal/frameworks`.
- `App.jsx` no longer imports, mounts, or opens `TenantCreationModal` on the normal authenticated route path. Root `/` redirects authenticated users to `/{user.tenantId || "personal"}/frameworks`.
- `TenantRoute.jsx` allows authenticated users without `user.tenantId` through the route shell. The legacy path segment remains a UI route shim only.
- `CreateFramework.jsx` cancel and `FrameworkEditor.jsx` fallback/discard navigation use the existing route shim instead of `/` or `/frameworks`.
- No request body, query string, or header was changed to send `tenant_id`, `X-Tenant-ID`, `user_id`, `creator_id`, or any route tenant value to backend framework APIs.
- `TenantCreationModal.jsx`, Firebase SDK files, artefact child-resource UI wiring, tenant/invite components, and semantic tenant/domain cleanup remain deferred to their existing owner rounds/phases.

## Round 0 Inventory

Round 0 confirmed Phase 5 final closeout status from the Phase 5 docs: final review accepted closeout, the Phase 5 package was committed and pushed, and Phase 6 may proceed without reopening Phase 5.

Backend cookie-session support was missing before Round 1. The backend still used a 7-day bearer token contract from `HTTPBearer`, `/api/users/login` returned a token body without cookies, `/api/users/me` required bearer auth, `/api/users/refresh` did not exist, and `/api/users/logout` only represented frontend token deletion.

Firebase-importing frontend files remain outside the Round 1 auth shell and are classified for later rounds:

- Rewrite in Round 2: `frontend/src/components/CreateFramework.jsx`, `frontend/src/components/FrameworkCard.jsx`, `frontend/src/components/FrameworkEditor.jsx`, `frontend/src/components/UpdateFrameworksButton.jsx`, `frontend/src/components/YourFrameworks.jsx`.
- Rewrite in Round 3: `frontend/src/components/Library.jsx`, `frontend/src/components/PublishModal.jsx`.
- Rewrite in Round 4: `frontend/src/components/AdminPanel.jsx`.
- Rewrite in Round 5: `frontend/src/components/FrameworkEditor.jsx` for artefact child-resource behavior.
- Remove or isolate in Round 6 only after active imports are gone: `frontend/src/lib/firebase.js`.
- Phase 7 semantic residue, to remove or isolate only as needed for SDK uninstall: `frontend/src/migrate-data.js`, `frontend/src/utils/cleanupData.js`, `frontend/src/utils/updateFrameworkTenants.js`, `frontend/src/components/InviteAccept.jsx`, `frontend/src/components/TenantCreationModal.jsx`, `frontend/src/components/TenantSettings.jsx`, `frontend/src/components/YourOrganization.jsx`.

Round 0 package inventory: `frontend/package.json` and `frontend/package-lock.json` still included `firebase`. That package removal was intentionally deferred until Round 6 because Rounds 2-5 still owned active Firebase import rewrites.

Post-change exact identity-token scans for `frontend/src` found no `access_token`, `Authorization: Bearer`, `getAuthToken`, `user_id`, `creator_id`, `tenant_id`, `X-Tenant-ID`, or `getFirebaseUserId` matches. Camel-case tenant/domain route residue such as `tenantId`, invite, migration, and Valorie wording remains a Phase 7 deferral unless Round 6 must isolate it to remove the SDK.

## Round 1 Scope

Round 1 implemented the cookie-session strategy and active auth foundation only.

Backend changes:

- `backend_py/app/auth.py` now creates 1-hour access tokens by default, creates 30-day refresh tokens, requires `typ: "access"` for protected endpoint auth, requires `typ: "refresh"` for refresh-token decoding, and reads the access token from the `access_token` httpOnly cookie. Round 6 removed the temporary Bearer fallback.
- `backend_py/app/api/users.py` now sets `access_token` and `refresh_token` httpOnly cookies on login/refresh, uses `SameSite=Lax`, uses `Secure` when `ENV`/`APP_ENV` is production or `AUTH_COOKIE_SECURE=true`, exposes `POST /api/users/refresh`, and clears cookies on `POST /api/users/logout`.
- `backend_py/app/models.py` and Alembic revision `0004_phase6_refresh_session_version` add `users.refresh_token_version`, allowing logout to revoke already-issued refresh cookies by version.
- `backend_py/main.py` adds `CookieCSRFMiddleware`, which enforces Origin/Referer checks on unsafe methods when auth cookies are present.
- Disabled users are rejected on login, cookie-auth protected access, and refresh, including already-issued cookies.

Frontend changes:

- `frontend/src/contexts/AuthContext.jsx` now uses only backend REST auth. It restores from `/api/users/me`, logs in through `/api/users/login`, logs out through `/api/users/logout`, keeps session state in React memory only, and does not import Firebase.
- `frontend/src/lib/api.js` no longer imports Firebase, reads `access_token`, writes bearer headers, sends tenant headers, or appends frontend identity fields. Shared backend requests use `credentials: 'include'`, attempt one refresh-and-retry on expired-access `401`, skip refresh for auth endpoints, and do not refresh true `403` authorization failures.
- `frontend/src/components/Login.jsx` no longer checks Firebase blocked-user state; disabled-user behavior comes from backend 401/403 responses.
- `frontend/src/components/Navbar.jsx` no longer imports Firebase for super-admin or member-count checks. It uses the backend `is_super_admin` response as display convenience only; backend admin routes remain the authority.
- `frontend/src/lib/api.test.js` covers the shared API-client refresh retry behavior, 403 non-refresh behavior, refresh-endpoint retry guard, and failed-refresh retry stop.

Temporary bearer compatibility remained only in the backend dependency layer after Round 1. Round 6 removed the `HTTPBearer` fallback in `backend_py/app/auth.py` and stopped returning `access_token` as a frontend contract.

## Round 1 Files Changed

- `backend_py/app/auth.py`
- `backend_py/app/api/users.py`
- `backend_py/app/models.py`
- `backend_py/main.py`
- `backend_py/alembic/versions/0004_phase6_refresh_session_version.py`
- `backend_py/tests/test_cookie_sessions.py`
- `frontend/src/lib/api.js`
- `frontend/src/lib/api.test.js`
- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/Navbar.jsx`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`

## Round 1 Boundaries Honored

- Did not rewire framework CRUD components beyond removing identity propagation from the shared API helper.
- Did not rewire `Library.jsx`, `PublishModal.jsx`, `AdminPanel.jsx`, artefact editing, tenant/invite/migration residue, or Firebase SDK removal.
- Did not uninstall Firebase.
- Did not delete `frontend/src/lib/firebase.js`.
- Did not implement Phase 7 semantic cleanup.
- Did not add Chat UI, Agent loop, RAG, LLMWiki, MCP, public registration, SaaS tenant features, invite/workspace redesign, or tenant cleanup.
- Did not add `/api/auth/*` aliases.
- Did not mark Phase 6 complete.

## Round 2 Scope

Round 2 implemented core owner framework and generation REST wiring only. At that time it did not complete Phase 6, and Rounds 3-6 remained open.

Frontend files changed:

- `frontend/src/lib/api.js`
- `frontend/src/components/YourFrameworks.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/CreateFramework.jsx`
- `frontend/src/components/AIMergeMode.jsx`
- `frontend/src/lib/api.test.js`
- `frontend/src/components/UpdateFrameworksButton.jsx`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`

Backend files were not changed in Round 2.

## Round 2 Endpoint Mapping

- Owner list: `YourFrameworks.jsx` -> `getMyFrameworks()` -> `GET /api/frameworks/my-frameworks`.
- Owner detail/load: `FrameworkEditor.jsx` -> `getFramework()` -> `GET /api/frameworks/{framework_id}`.
- Owner update/save/autosave: `FrameworkEditor.jsx` -> `updateFramework()` -> `PUT /api/frameworks/{framework_id}`.
- Owner delete: `FrameworkCard.jsx` -> `deleteFramework()` -> `DELETE /api/frameworks/{framework_id}`.
- Owner create helper: `api.js` `createFramework()` -> `POST /api/frameworks`; retained for owner CRUD parity and sanitized by the shared payload allowlist.
- Owner binding helper: `api.js` `getFrameworkBinding()` -> `GET /api/frameworks/{framework_id}/binding`; exported for the Phase 5 contract but not currently needed by the editor UI.
- Text generation: `CreateFramework.jsx` -> `generateFrameworkFromText()` -> `POST /api/frameworks/generate-from-text`.
- Multi-file generation: `CreateFramework.jsx` -> `generateFrameworkFromFiles()` -> `POST /api/frameworks/generate-from-files`.
- Single-file helper remains available: `generateFrameworkFromFile()` -> `POST /api/frameworks/generate-from-file`.
- Regeneration: `FrameworkEditor.jsx` -> `regenerateFramework()` -> `POST /api/frameworks/regenerate`.
- AI merge: `AIMergeMode.jsx` -> `mergeFrameworksWithAI()` -> `POST /api/frameworks/ai-merge`.
- Library unpublish from the owner card uses the existing backend endpoint: `unpublishFramework()` -> `POST /api/frameworks/{framework_id}/unpublish`. `PublishModal.jsx` itself was not modified and publish/unpublish flows remain Round 3 scope.

## Round 2 Implementation Notes

- `api.js` now normalizes backend framework list/detail responses into the frontend editor/card shape and whitelists framework mutation fields before create/update/regenerate requests.
- Create/regenerate payloads retain full-payload semantics with backend-compatible defaults for `title`, `version`, `family`, `confidence`, `metadata`, `steps`, `artefacts`, `risks`, and `escalation`.
- Update payloads now use patch semantics: only caller-provided fields are sent, missing `family` is not defaulted to `Other`, missing `confidence` is not defaulted to `0`, and missing or empty `_raw` is omitted.
- Empty `_raw` objects are omitted so editor autosave/save cannot clear existing backend raw framework JSON.
- No Round 2 request body, query string, or header sends frontend-supplied owner or tenant identity authority.
- `YourFrameworks.jsx` now loads owner frameworks through the backend list endpoint instead of Firestore realtime listeners.
- `CreateFramework.jsx` now uses backend-returned `framework_id` / `framework_ids` from generation responses and no longer performs an extra Firebase save.
- `FrameworkEditor.jsx` now loads, autosaves, saves, and regenerates through the backend REST helpers. Local draft backup remains limited to draft content under `framework-draft-*`.
- `FrameworkCard.jsx` deletes through backend owner REST and no longer calls Firestore or `push-framework`. Organization sharing actions are inert in this round.
- `UpdateFrameworksButton.jsx` is isolated to a null component because the old organization-field repair path was Firebase/tenant residue. Semantic cleanup remains Phase 7.
- `ManualMergeMode.jsx` was inspected and left unchanged because it is local drag-and-drop state only and had no Firebase or REST identity path.

## Round 2 Boundaries Honored

- Did not modify backend code.
- Did not rewire `Library.jsx` or `LibraryCard.jsx`.
- Did not modify `PublishModal.jsx`.
- Did not rewire `AdminPanel.jsx`.
- Did not implement artefact child-resource CRUD.
- Did not uninstall Firebase or delete `frontend/src/lib/firebase.js`.
- Did not implement Phase 7 Valorie/domain/tenant/invite/migration semantic cleanup.
- Did not add Chat UI, Agent loop, RAG retrieval/indexing/citations, LLMWiki, MCP marketplace, public registration, SaaS tenant features, org sharing, or invite cleanup.
- Did not claim vector sync/indexing succeeded; the Round 2 card path no longer calls the Phase 9-deferred `push-framework` route.

## Round 3 Scope

Round 3 implemented the Library plus publish/unpublish REST wiring only. It did not complete Phase 6.

Frontend files changed:

- `frontend/src/lib/api.js`
- `frontend/src/lib/api.test.js`
- `frontend/src/components/Library.jsx`
- `frontend/src/components/Library.test.jsx`
- `frontend/src/components/LibraryCard.jsx`
- `frontend/src/components/PublishModal.jsx`
- `frontend/src/components/PublishModal.test.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/FrameworkCard.test.jsx`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`

Backend files were not changed in Round 3.

## Round 3 Endpoint Mapping

- Authenticated public library: `Library.jsx` -> `getPublicFrameworks()` -> `GET /api/frameworks/public?limit=20` with optional `cursor`.
- Library pagination: `Library.jsx` load-more -> `getPublicFrameworks({ cursor })` -> `GET /api/frameworks/public?cursor=...&limit=20`.
- Owner publish: `PublishModal.jsx` -> `publishFramework()` -> `POST /api/frameworks/{framework_id}/publish`.
- Owner-card publish launcher: `FrameworkCard.jsx` opens the REST-backed `PublishModal`.
- Owner unpublish: `FrameworkCard.jsx` -> `unpublishFramework()` -> `POST /api/frameworks/{framework_id}/unpublish`.

## Round 3 Implementation Notes

- `Library.jsx` no longer imports Firestore or `frontend/src/lib/firebase.js`.
- The old realtime Firestore `onSnapshot` public-list subscription was replaced with one-shot backend REST loading, a manual `Reload` action, and cursor-based `Load more`.
- `Library.jsx` requests the backend public-list endpoint with cookie credentials through the shared API client and suppresses automatic redirect so a 401/403 can render an auth-required state inside the already protected route shell.
- `api.js` now normalizes backend public-list items with `items`, `next_cursor`, `limit`, `preview_artefacts`, `published_at`, and `tags`.
- `LibraryCard.jsx` renders backend `preview_artefacts`, `published_at`, and `tags` without Firestore timestamp assumptions.
- `PublishModal.jsx` no longer imports Firestore, no longer writes Firestore publish fields, and no longer calls the Phase 9-deferred `push-framework` route.
- `PublishModal.jsx` sends only `category`, `tags`, and `version` to the backend publish endpoint. It does not send frontend owner or tenant identity.
- `FrameworkCard.jsx` now opens `PublishModal` for owner publish and uses backend unpublish responses to update local published state.
- `api.js` no longer exports the frontend `PUSH_FRAMEWORK` endpoint constant because no active Round 3 UI should call that Phase 9-deferred route.

## Round 3 Boundaries Honored

- Did not modify backend code.
- Did not rewire `AdminPanel.jsx`.
- Did not implement artefact child-resource UI wiring.
- Did not uninstall Firebase or delete `frontend/src/lib/firebase.js`.
- Did not implement Phase 7 Valorie/domain/tenant/invite/migration semantic cleanup.
- Did not add anonymous public library access; `/library` remains behind `PrivateRoute`, and backend public-list requests still rely on cookie-session auth.
- Did not add public registration, SaaS tenant/org sharing, Chat UI, Agent loop, RAG indexing/retrieval/citations, LLMWiki, MCP marketplace, or tool registry work.
- Did not show or log vector sync success from publish UI; real vector sync/indexing/retrieval remains Phase 9.

## Round 4 Scope

Round 4 implemented Admin users REST wiring only. Historical Round 4 handoff did not complete Phase 6 because Round 5 and Round 6 had not run yet; the current Phase 6 closeout status is accepted by Migration Reviewer after Round 6, with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable.

Frontend files changed:

- `frontend/src/lib/api.js`
- `frontend/src/lib/api.test.js`
- `frontend/src/components/AdminPanel.jsx`
- `frontend/src/components/AdminPanel.test.jsx`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`

Backend files were not changed in Round 4.

## Round 4 Endpoint Mapping

- Admin user list: `AdminPanel.jsx` -> `getAdminUsers()` -> `GET /api/admin/users`.
- Admin user create: `AdminPanel.jsx` -> `createAdminUser()` -> `POST /api/admin/users`.
- Admin user disable: `AdminPanel.jsx` -> `disableAdminUser(user.id)` -> `POST /api/admin/users/{user_id}/disable`.
- Admin user enable: `AdminPanel.jsx` -> `enableAdminUser(user.id)` -> `POST /api/admin/users/{user_id}/enable`.

## Round 4 Implementation Notes

- `AdminPanel.jsx` no longer imports `frontend/src/lib/firebase.js` or Firebase admin helpers.
- The old frontend `isSuperAdmin()` gate was removed from `AdminPanel.jsx`; the first admin list request is the authorization check, and backend `403` renders an admin-unavailable state.
- `api.js` added focused admin helpers that use the shared cookie-session client and keep `credentials: "include"`.
- Admin create sends only `email`, `password`, and optional `username`; it does not expose or submit `password_hash`.
- Admin list and status controls use backend `id`, `is_disabled`, `disabled_at`, and `is_super_admin`. Firebase `uid` and `isBlocked` are no longer used.
- Disable/enable calls put the backend user id in the accepted Phase 5 URL path and do not send frontend identity fields in request bodies or headers.
- Whitelist/domain add/remove UI was removed from active admin behavior. The panel shows a small unsupported-domain-policy note because Phase 5 did not accept a whitelist-domain endpoint.
- Public registration remains disabled; Round 4 adds no signup or self-service registration path.

## Round 4 Boundaries Honored

- Did not modify backend code.
- Did not rewire artefact child-resource UI behavior.
- Did not uninstall Firebase or delete `frontend/src/lib/firebase.js`.
- Did not implement Phase 7 Valorie/domain/tenant/invite/migration semantic cleanup.
- Did not add a whitelist-domain/domain-management backend feature.
- Did not add public registration, SaaS tenant/org sharing, invites, Chat UI, Agent loop, RAG indexing/retrieval/citations, LLMWiki, MCP marketplace, or tool registry work.

## Round 4 Reviewer Attention

- Tenant/invite components and Firebase SDK/package removal were intentionally left for Round 6 and Phase 7; Round 6 isolated the SDK-dependent residue while leaving semantics to Phase 7.
- `AdminPanel.jsx` is now rewired to the accepted Phase 5 backend admin REST contract.
- The domain-policy note is intentionally non-functional because no accepted Phase 5 whitelist-domain endpoint exists.
- Backend temporary Bearer compatibility was the Phase 6 closeout blocker documented from Round 1 and was removed in Round 6.
- No browser smoke test was run in Round 2, Round 3, or Round 4; verification is static scans plus frontend lint/tests/build. Owner-flow, public-library, and admin browser behavior remain unchecked in `verification.md`.

## Round 5 Scope

Round 5 implemented artefact child-resource UI wiring only. Historical Round 5 handoff did not complete Phase 6 because Round 6 and Migration Reviewer acceptance had not happened yet; the current Phase 6 closeout status is accepted by Migration Reviewer after Round 6, with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable.

Frontend files changed:

- `frontend/src/lib/api.js`
- `frontend/src/lib/api.test.js`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/FrameworkEditor.test.jsx`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`

Backend files were not changed in Round 5.

## Round 5 Endpoint Mapping

- Artefact list: `FrameworkEditor.jsx` -> `listFrameworkArtefacts(frameworkId)` -> `GET /api/frameworks/{framework_id}/artefacts`.
- Artefact create: `FrameworkEditor.jsx` -> `createFrameworkArtefact(frameworkId, artefactData)` -> `POST /api/frameworks/{framework_id}/artefacts`.
- Artefact get helper: `getFrameworkArtefact(frameworkId, artefactId)` -> `GET /api/frameworks/{framework_id}/artefacts/{artefact_id}`.
- Artefact update: `FrameworkEditor.jsx` -> `updateFrameworkArtefact(frameworkId, artefactId, artefactData)` -> `PUT /api/frameworks/{framework_id}/artefacts/{artefact_id}`.
- Artefact delete: `FrameworkEditor.jsx` -> `deleteFrameworkArtefact(frameworkId, artefactId)` -> `DELETE /api/frameworks/{framework_id}/artefacts/{artefact_id}`.

## Round 5 Implementation Notes

- `api.js` added artefact child-resource helpers that use the shared cookie-session client, so every request carries `credentials: "include"`.
- Artefact create/update payloads are allowlisted to `name`, `artefact_type`, `content_json`, `metadata_json`, and `ord`.
- Parent `framework_id` remains only in the URL path. Mutation bodies strip frontend-supplied parent, user, creator, tenant, and tenant-header fields.
- `FrameworkEditor.jsx` now loads child artefacts separately after framework detail load and renders them through the existing `ArtefactEditor` rich-text surface.
- Artefact create/update/delete now persist through the child-resource REST helpers instead of mutating embedded framework artefact JSON.
- Whole-framework autosave, manual save, and regenerate-save no longer send `artefacts` to `PUT /api/frameworks/{framework_id}`.
- Local draft backup remains under `framework-draft-*` and stores draft content plus normalized artefact content only. It does not store auth/session tokens or headers.
- Backend `403` and `404` artefact-list failures are surfaced from backend responses. Cross-user access remains a backend responsibility, not a frontend ownership check.
- Legacy `_raw.framework.artefact_variants` may still render as read-only reference when no child resources exist. Round 5 does not backfill or synchronize it into child rows.

## Round 5 Boundaries Honored

- Did not modify backend code.
- Did not backfill or migrate historical `frameworks.artefacts_json` or `_raw.artefact_variants` into child artefact rows.
- Did not uninstall Firebase or delete `frontend/src/lib/firebase.js`.
- Did not implement Round 6 Firebase SDK/package/env cleanup.
- Did not implement Phase 7 Valorie/domain/tenant/invite/migration semantic cleanup.
- Did not rework AdminPanel, Library, publish/unpublish, or core framework ownership flows beyond the artefact editor touchpoint.
- Did not add public registration, SaaS tenant/org sharing, invites, Chat UI, Agent loop, RAG indexing/retrieval/citations, LLMWiki, MCP marketplace, or tool registry work.

## Round 5 Reviewer Attention

- Artefact UI is now wired to the accepted Phase 5 child-resource contract, with API and editor tests for list/create/get/update/delete mapping, 403/404 handling, and local draft storage.
- Historical embedded artefacts remain a read-only fallback only; no synchronization into child rows was added.
- Backend temporary Bearer compatibility remained the Phase 6 closeout blocker from Round 1 and was removed in Round 6.
- No browser smoke test was run for Round 5. Verification is static scans, focused tests, full frontend tests, lint, build, and `git diff --check`.

## Round 6 Scope

Round 6 removed the frontend Firebase SDK runtime dependency, isolated remaining Firebase-dependent Phase 7 residue, removed frontend/container Firebase env hooks, and closed the backend Bearer compatibility gate. Migration Reviewer accepted the Phase 6 closeout with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable. Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.

Frontend files removed:

- `frontend/src/lib/firebase.js`

Frontend files isolated as technical Phase 6 SDK-removal placeholders:

- `frontend/src/migrate-data.js`
- `frontend/src/utils/cleanupData.js`
- `frontend/src/utils/updateFrameworkTenants.js`
- `frontend/src/utils/DataCleanupButton.jsx`
- `frontend/src/components/MigrationTool.jsx`
- `frontend/src/components/InviteAccept.jsx`
- `frontend/src/components/TenantCreationModal.jsx`
- `frontend/src/components/TenantSettings.jsx`
- `frontend/src/components/YourOrganization.jsx`

These files were isolated only because they imported the Firebase SDK or depended on Firebase-backed helper modules. Their tenant, invite, organization, domain, and historical migration semantics remain Phase 7 or later deferrals.

Frontend/package/container cleanup:

- Removed `firebase` from `frontend/package.json` with `npm uninstall firebase --ignore-scripts --no-audit --fund=false`.
- Updated `frontend/package-lock.json` through the same uninstall workflow.
- Removed the stray root `firebase` dependency from `package.json` with `npm pkg delete dependencies.firebase`.
- Updated root `package-lock.json` with `npm install --package-lock-only --ignore-scripts --no-audit --fund=false --offline` after a normal root uninstall attempted a blocked registry fetch for unrelated `redux`.
- Removed frontend Firebase build args/env injection from `Dockerfile` and `docker-compose.yml`.

Backend Bearer closeout:

- `backend_py/app/auth.py` no longer imports or depends on `HTTPBearer` / `HTTPAuthorizationCredentials`.
- Protected endpoint auth now extracts the access JWT only from the `access_token` cookie.
- Optional auth now reads only the access cookie.
- `backend_py/app/api/users.py` no longer returns `access_token` or `token_type` fields from login, refresh, or enabled registration responses.
- Backend tests now authenticate protected test traffic through the access cookie and include negative Bearer checks in `test_cookie_sessions.py`.

Round 6 backend test files changed:

- `backend_py/tests/test_cookie_sessions.py`
- `backend_py/tests/test_admin_users.py`
- `backend_py/tests/test_auth_hardening.py`
- `backend_py/tests/test_framework_artefacts.py`
- `backend_py/tests/test_framework_owner_crud.py`
- `backend_py/tests/test_framework_publish_public.py`
- `backend_py/tests/test_generation_persistence.py`

Round 6 verification:

- Required Firebase SDK, Firebase helper, Firestore API, Firebase env, package dependency, and frontend bearer/localStorage scans returned no matches.
- Frontend lint passed.
- Frontend tests passed on escalated rerun after the sandboxed Vitest config-read failure: 10 files, 49 tests.
- Frontend production build passed on escalated rerun after the sandboxed Vite config-read failure; build output has no Firebase string matches.
- Backend compileall passed.
- Focused backend auth/session/REST tests passed: 73 tests.
- Full backend tests passed: 117 tests.

Browser smoke:

- Browser smoke was not run. `docker compose ps` failed because Docker Desktop's Linux engine pipe was unavailable: `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`.
- The backend requires `DATABASE_URL` at import time, and the app models/Alembic migrations use PostgreSQL JSONB and pgvector types, so SQLite is not a faithful local fallback.
- No live Postgres service and seeded admin credentials were available in this environment. Do not convert the deferred browser-smoke item into a run result until a local DB/server smoke session is actually run.

## Round 6 Boundaries Honored

- Did not perform Phase 7 semantic cleanup of tenant, organization, invite, domain, migration, or Valorie residue.
- Did not redesign tenants, organizations, workspaces, invites, or sharing.
- Did not add public registration, anonymous library access, Firebase ID token compatibility, Firebase Auth, Firestore, or a new Firebase project.
- Did not add Chat UI, Agent loop, RAG, LLMWiki, MCP marketplace, tool registry, or embedding work.
- Did not perform historical artefact backfill or embedded artefact synchronization.

## Round 6 Reviewer Attention

- Phase 6 closeout was accepted by Migration Reviewer after Round 6.
- Browser smoke remains the main reviewer attention point because it was blocked by local Docker/Postgres unavailability, not by a known app assertion failure.
- Phase 7 should own semantic removal or redesign of the isolated tenant/invite/organization/migration route shells.

## Round 2 Review Repairs Addressed

1. P1 owner update/save payload corruption:

- `frontend/src/lib/api.js` now preserves separate create/regenerate and update payload semantics.
- Create/regenerate helpers may still send backend-compatible defaults required for full framework payloads.
- `updateFramework(id, partialData)` now sends a sparse patch only; absent `family`, `confidence`, and `_raw` are omitted.
- `updateFramework(id, { _raw: {} })` omits `_raw` rather than sending an empty object.
- Editor autosave/save-style payloads no longer clear backend raw framework JSON when raw data is absent or empty.
- Focused API payload tests cover sparse updates, empty raw omission, editor autosave-style payloads, create/regenerate validity, and omission of frontend identity fields.

2. P2 verification overclaims behavior coverage:

- Round 2 verification now distinguishes static scans, lint, unit tests, and build from browser smoke tests.
- No browser smoke test was run for Round 2, and the docs now say so in the status, reviewer attention, verification section, and browser checklist.
- Focused REST UI behavior tests remain unchecked until implemented.
- Phase 6 closeout acceptance is now recorded in the Phase 6 docs.

## Round 2 Remaining Review Repairs Addressed

1. P1 backend-cookie users could not reach core framework routes without tenant/Firebase setup:

- `frontend/src/App.jsx` no longer mounts `TenantCreationModal` after authenticated backend-cookie login, so the normal path no longer writes Firestore tenant documents.
- Root `/` and successful no-tenant login now route to `/personal/frameworks`, where `personal` is only a legacy UI route shim.
- `frontend/src/components/TenantRoute.jsx` no longer redirects authenticated users with `user.tenantId: null` away from core framework route shells.
- `frontend/src/components/CreateFramework.jsx` and `frontend/src/components/FrameworkEditor.jsx` now navigate back through the same route shim when they need an owner framework route.
- Focused tests cover login to `/personal/frameworks`, app-root modal suppression, and `TenantRoute` pass-through for authenticated backend-cookie no-tenant users.

2. P3 checklist verification stale identity scan wording:

- `checklist.md` and `verification.md` now scope exact identity-field scan claims to active Round 2 production files.
- Test files may contain exact identity strings only as intentional negative assertions.
- The full Phase 6 closeout state is now updated: Migration Reviewer accepted Phase 6 after Round 6, with browser smoke deferred for environment reasons.

## Scope

Phase 6 owns frontend de-Firebase work required to remove active frontend Firebase runtime dependency and SDK usage.

Included:

- Narrow backend cookie-session repair if required for Phase 6 cookie auth.
- AuthContext migration to backend cookie session.
- Shared frontend REST client cleanup.
- Core framework REST wiring.
- Library and publish/unpublish REST wiring.
- Admin users REST wiring.
- Artefact subresource REST wiring.
- Firebase SDK package/env removal.
- Isolation or deletion of Firebase-importing frontend residue only when required to uninstall the SDK.

Excluded:

- Phase 7 semantic cleanup of Valorie/domain/tenant/invite/migration residue.
- Tenant, workspace, invite, organization, or sharing redesign.
- Public registration or anonymous API/library access.
- Firebase Auth, Firebase ID token, Firestore, or new Firebase project setup.
- Agent, LLMWiki, Chat UI, MCP, RAG retrieval, pgvector indexing, or embedding.
- Reopening Phase 5 implementation.

## Round Breakdown

Round 0: canonical doc alignment and focused inventory.

Round 1: cookie session strategy, narrow backend session repair if needed, CSRF/Origin protection, and AuthContext foundation.

Round 2: core framework REST wiring.

Round 3: Library plus publish/unpublish REST.

Round 4: Admin users REST.

Round 5: artefact subresource wiring.

Round 6: Firebase SDK removal and closeout.

## Current Round 0/1 State

The Round 0/1 implementation now establishes:

- Phase 6 must not preserve 7d Bearer plus `localStorage` as the final path.
- The frontend restore flow uses `/api/users/me` from cookie auth.
- Expired access uses `POST /api/users/refresh`, including normal shared API-client `401` retry.
- Logout uses `POST /api/users/logout`.
- Temporary Bearer compatibility had a documented removal gate and could not satisfy Phase 6 closeout.
- Round 6 removed Bearer compatibility; protected endpoint credentials now come only from the access cookie.
- Unsafe cookie-authenticated methods require explicit CSRF/Origin/Referer protection and tests.
- Phase 6 implementation can proceed from the accepted Phase 5 REST surfaces without reopening Phase 5 implementation.

## Earlier Planning Reviewer Findings Addressed

1. Auth endpoint canonical conflict:

- `MIGRATION_PHASES.md` was updated from `/api/auth/refresh` and `/api/auth/logout` to `/api/users/refresh` and `/api/users/logout`.
- Phase 6 docs now explicitly use `POST /api/users/login`, `GET /api/users/me`, `POST /api/users/refresh`, and `POST /api/users/logout`.
- Phase 6 docs now say not to introduce dual `/api/auth/*` and `/api/users/*` contracts.

2. CSRF/Origin verification gap:

- Round 1 now requires concrete positive and negative backend tests for cookie-authenticated unsafe methods.
- Required cases include allowed same-origin unsafe pass, missing or invalid Origin/Referer rejection where policy requires it, disallowed Origin rejection, safe methods not incorrectly blocked, and SameSite=None stronger-token success/failure if applicable.

3. Missing `phase-report.md`:

- This initial planning report was created.

4. Phase 5 acceptance gate:

- Phase 6 docs now record that Phase 5 final review accepted the closeout, the staged package was committed and pushed, and Phase 6 planning may proceed.
- Phase 6 must not reopen Phase 5 implementation.

## Round 0/1 Review Repairs Addressed

1. P1 refresh JWTs could authenticate protected endpoints:

- Protected endpoint auth now accepts only JWTs with `typ: "access"`.
- `decode_refresh_token` continues to require `typ: "refresh"`.
- Backend tests prove refresh tokens fail through the access-cookie protected endpoint path, Bearer credentials are rejected, access cookies still work, and `/api/users/refresh` accepts only refresh tokens.

2. P2 frontend refresh only worked during initial session restore:

- `frontend/src/lib/api.js` now attempts one `/api/users/refresh` after normal `401` responses, then retries the original request once.
- The refresh retry skips login/logout/refresh/register auth endpoints and does not run for `403` authorization failures.
- No frontend localStorage token or Bearer fallback was reintroduced.
- `frontend/src/lib/api.test.js` verifies the retry, 403, auth-endpoint guard, and failed-refresh stop behavior.

3. P3 stale planning-only report wording:

- This report now states that Round 0/1 implementation has happened and is under review repair.
- Phase 6 closeout is accepted; Phase 7 semantic deferrals continue after Round 6.

## Open Risks

- Phase 5 acceptance documentation has been corrected in the Phase 5 closeout docs; Phase 6 may proceed from the accepted Phase 5 REST surfaces without reopening Phase 5 implementation.
- Temporary backend Bearer compatibility has been removed; the remaining closeout risk is browser smoke coverage blocked by local Docker/Postgres unavailability.
- CSRF policy is currently Origin/Referer based with SameSite=None clamped to Lax; if SameSite=None is later allowed, stronger CSRF protection such as double-submit token must be added and tested.
- Some Firebase-importing files are also Phase 7 residue. Phase 6 may isolate or delete them only to remove active Firebase dependency.
- The old whitelist-domain admin controls are removed from active Round 4 behavior; real domain/allowlist semantics remain outside Phase 6 unless a later accepted backend contract adds them.
- Historical embedded artefacts are not migrated into child rows; Round 5 keeps them as read-only reference when present.

## Completion Note

Phase 6 closeout is accepted by Migration Reviewer. This report records Round 0/1/2/3/4/5/6 implementation and current review repairs. Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable, and Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
