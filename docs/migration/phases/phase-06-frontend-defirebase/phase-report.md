# Phase 06 Round 0/1/2 Report - Frontend de-Firebase

Round 0/1/2 implementation status: Round 0 inventory, Round 1 cookie-session/AuthContext foundation, Round 2 core framework REST wiring, and Round 2 review repairs have been implemented with static scan, lint, unit-test, and build verification. No Round 2 browser smoke test has been run. Phase 6 is not complete; Rounds 3-6 remain open.

## Status

This report is now the Round 0/1/2 implementation and review-repair record. Earlier planning-only wording has been superseded; full Phase 6 remains incomplete until Rounds 3-6 and reviewer closeout pass.

Current Phase 6 status:

- Planning package created: `checklist.md`, `phase-plan.md`, `verification.md`, and this `phase-report.md`.
- Canonical auth route decision recorded: Phase 6 uses only the `/api/users/*` auth route family.
- Round 0, Round 1, and Round 2 implementation is complete with recorded static scan, lint, test, and build verification.
- Current repair passes fix the Round 2 update payload, route-gate, tenant-modal, and verification wording review findings.
- Round 1 repaired backend cookie-session support because the Phase 1 token strategy debt was still present.
- Protected backend endpoints now reject refresh JWTs on both access-cookie and temporary Bearer paths.
- Shared frontend API requests now attempt one `/api/users/refresh` on normal expired-access `401` responses, then retry the original request once.
- CSRF/Origin/Referer verification requirements are explicit.
- Phase 5 final review accepted the closeout; Phase 6 planning may proceed.
- Phase 6 is not complete; Rounds 3-6 remain open.

## Current Round 2 Review Repair Scope

This repair fixes only the remaining Round 2 review findings. It does not implement Rounds 3-6 and does not mark Phase 6 complete.

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
- `TenantCreationModal.jsx`, Firebase SDK files, Library, PublishModal, AdminPanel, artefacts, tenant/invite components, and semantic tenant/domain cleanup remain deferred to their existing owner rounds/phases.

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

Package inventory: `frontend/package.json` and `frontend/package-lock.json` still include `firebase`. This is intentionally deferred to Round 6 because Rounds 2-5 still own active Firebase import rewrites.

Post-change exact identity-token scans for `frontend/src` found no `access_token`, `Authorization: Bearer`, `getAuthToken`, `user_id`, `creator_id`, `tenant_id`, `X-Tenant-ID`, or `getFirebaseUserId` matches. Camel-case tenant/domain route residue such as `tenantId`, invite, migration, and Valorie wording remains a Phase 7 deferral unless Round 6 must isolate it to remove the SDK.

## Round 1 Scope

Round 1 implemented the cookie-session strategy and active auth foundation only.

Backend changes:

- `backend_py/app/auth.py` now creates 1-hour access tokens by default, creates 30-day refresh tokens, requires `typ: "access"` for protected endpoint auth, requires `typ: "refresh"` for refresh-token decoding, and reads the access token from the `access_token` httpOnly cookie before falling back to temporary bearer compatibility.
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

Temporary bearer compatibility remains only in the backend dependency layer for existing tests and transitional clients. It cannot satisfy Phase 6 closeout. Removal gate: after Rounds 3-6 remove remaining transitional clients/tests from that path, remove the `HTTPBearer` fallback in `backend_py/app/auth.py`, and stop returning `access_token` as a frontend contract.

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

Round 2 implements core owner framework and generation REST wiring only. It does not complete Phase 6; Rounds 3-6 remain open.

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

## Round 2 Reviewer Attention

- `PublishModal.jsx`, `Library.jsx`, `AdminPanel.jsx`, tenant/invite components, and Firebase SDK/package removal are intentionally still open for Rounds 3-6.
- `FrameworkCard.jsx` now prevents the owner card from launching the Firebase-backed `PublishModal`; formal publish/unpublish UI rewiring remains Round 3.
- Backend temporary Bearer compatibility remains the Phase 6 closeout blocker already documented from Round 1.
- No browser smoke test was run in Round 2; verification is static scans plus frontend lint/tests/build. Owner-flow browser behavior remains unchecked in `verification.md`.

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
- Phase 6 remains incomplete; Rounds 3-6 and reviewer closeout remain open.

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
- The full Phase 6 completion state remains unchanged: Phase 6 is not complete, and Rounds 3-6 remain open.

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
- Temporary Bearer compatibility, if retained during transition, must have a documented removal gate and cannot satisfy Phase 6 closeout.
- Temporary Bearer compatibility cannot accept refresh JWTs as protected endpoint credentials.
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
- Backend tests prove refresh tokens fail through both access-cookie and temporary Bearer protected endpoint paths, access tokens still work, and `/api/users/refresh` accepts only refresh tokens.

2. P2 frontend refresh only worked during initial session restore:

- `frontend/src/lib/api.js` now attempts one `/api/users/refresh` after normal `401` responses, then retries the original request once.
- The refresh retry skips login/logout/refresh/register auth endpoints and does not run for `403` authorization failures.
- No frontend localStorage token or Bearer fallback was reintroduced.
- `frontend/src/lib/api.test.js` verifies the retry, 403, auth-endpoint guard, and failed-refresh stop behavior.

3. P3 stale planning-only report wording:

- This report now states that Round 0/1 implementation has happened and is under review repair.
- Phase 6 remains explicitly not complete, with Rounds 3-6 and Phase 7 deferrals still open after the Round 2 implementation.

## Open Risks

- Phase 5 acceptance documentation has been corrected in the Phase 5 closeout docs; Phase 6 may proceed from the accepted Phase 5 REST surfaces without reopening Phase 5 implementation.
- Temporary backend Bearer compatibility remains for transitional clients and tests; it is blocked from satisfying Phase 6 closeout and now rejects refresh JWTs.
- CSRF policy is currently Origin/Referer based with SameSite=None clamped to Lax; if SameSite=None is later allowed, stronger CSRF protection such as double-submit token must be added and tested.
- Some Firebase-importing files are also Phase 7 residue. Phase 6 may isolate or delete them only to remove active Firebase dependency.
- Admin UI may expose whitelist-domain concepts without a Phase 5 backend endpoint.
- Artefact UI may still be coupled to legacy `frameworks.artefacts_json`; historical backfill is not Phase 6 scope.

## Completion Note

Phase 6 is not complete. This report records Round 0/1/2 implementation and current review repairs; Rounds 3-6, Firebase SDK removal, and reviewer closeout remain open.
