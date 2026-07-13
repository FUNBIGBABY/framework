# Phase 06 Plan - Frontend de-Firebase

## Current Audit Correction

`P6-DEFIREBASE-CORRECTION-01` supersedes the status assertions below without
deleting their historical evidence. The current audit-grade verdict is
`pending`; `27679f8ff832a70a7f69782d8d45a52eab343525` is an implementation
candidate only, `accepted_commit` is absent, and reviewer identity, reviewed
SHA, review date, and raw verdict artifact remain unavailable.

Historical planning status: documentation only. This plan did not implement backend or frontend code and did not mark Phase 6 complete when written; the current Phase 6 closeout status is accepted by Migration Reviewer after Round 6, with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable.

## Governance Reconciliation - 2026-07-10

- Preserve the historical owner-handoff verdict exactly as `accepted_with_documented_deferral`; do not downgrade it to ordinary conditional status.
- Reviewed implementation commit: `27679f8ff832a70a7f69782d8d45a52eab343525`.
- Original reviewer identity, review date, and raw verdict artifact: `artifact unavailable`; none may be inferred from commit messages or later docs wording.
- Browser smoke: `not run`. Exact recorded blocker: Docker Desktop Linux engine unavailable, with no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded admin credentials.
- Owner: Migration Verification Owner. Trigger: the complete authorized smoke environment becomes available, before a release that relies on these browser flows, or as an explicit later reviewer condition.
- Missing browser smoke is not automatically a blocker. A focused re-review is required only to attach a named reviewer/date/evidence and make the historical verdict audit-grade.

## Recommended Plan

Phase 6 should remove the active Firebase frontend runtime dependency and SDK usage by moving auth, framework data, public library, publish/unpublish, admin users, and artefact editing onto the backend REST contracts delivered by Phase 5.

The recommended sequence is seven rounds:

1. Round 0: canonical doc alignment.
2. Round 1: cookie session strategy + AuthContext foundation.
3. Round 2: core framework REST wiring.
4. Round 3: Library + publish/unpublish REST.
5. Round 4: Admin users REST.
6. Round 5: artefact subresource wiring.
7. Round 6: Firebase SDK removal + closeout.

This sequencing removes the auth trust-chain issue first, then replaces data flows by surface area, and only uninstalls the SDK after all active imports are gone.

## Sources And Current Facts

Required source documents:

- `MIGRATION_PHASES.md`
- `docs/PERSONAL_USE_BOUNDARY.md`
- `docs/migration/README.md`
- `docs/migration/decisions/ADR-0001-auth-strategy.md`
- `docs/migration/phases/phase-05-backend-firestore-business/checklist.md`
- `docs/migration/phases/phase-05-backend-firestore-business/phase-report.md`
- `docs/migration/phases/phase-05-backend-firestore-business/verification.md`

Focused repo facts from planning scans:

- `frontend/package.json` still depends on `firebase`.
- `frontend/src/lib/firebase.js` is the central Firebase Auth/Firestore helper.
- `frontend/src/contexts/AuthContext.jsx` still uses Firebase Auth, Firestore user documents, and `localStorage` bearer compatibility.
- `frontend/src/lib/api.js` still imports Firebase auth, reads `access_token`, sends `Authorization: Bearer`, and derives tenant/user identity from the frontend.
- Phase 1 token strategy debt is known: current auth may still have 7d Bearer plus `localStorage` compatibility paths. Phase 6 Round 1 owns the narrow backend session repair if cookie-session support is missing.
- Canonical Phase 6 auth endpoints use the existing `/api/users/*` route family: `POST /api/users/login`, `GET /api/users/me`, `POST /api/users/refresh`, and `POST /api/users/logout`. Do not introduce a parallel `/api/auth/*` contract.
- Phase 5 is the dependency for Phase 6. Phase 5 final review accepted the closeout, the staged package was committed and pushed, and Phase 6 planning may proceed. Phase 6 implementation should use the accepted Phase 5 REST surfaces without reopening Phase 5 implementation.
- Active components still import Firebase or `../lib/firebase`, including `Library.jsx`, `PublishModal.jsx`, `FrameworkCard.jsx`, `FrameworkEditor.jsx`, `AdminPanel.jsx`, `Navbar.jsx`, `YourFrameworks.jsx`, `UpdateFrameworksButton.jsx`, `TenantCreationModal.jsx`, `TenantSettings.jsx`, `YourOrganization.jsx`, and `InviteAccept.jsx`.
- Phase 5 reports backend REST contracts for private framework CRUD, generation persistence, authenticated public library, publish/unpublish, admin users, and artefact subresources.

## Scope

Phase 6 owns:

- Narrow backend cookie-session repair if required to retire Firebase Auth and localStorage bearer compatibility.
- Canonicalizing frontend/backend auth integration on the `/api/users/*` route family only.
- Frontend auth migration from Firebase Auth/localStorage bearer compatibility to backend cookie session flow.
- Shared frontend REST client cleanup so all private requests use `credentials: "include"`.
- Removal of frontend Firebase Auth and Firestore imports from active runtime code.
- REST rewiring for core framework flows, public library, publish/unpublish, admin users, and artefact subresources.
- Removing or isolating Firebase-importing frontend files when that is required to uninstall the Firebase SDK.
- Package/env cleanup needed to remove the Firebase SDK from the frontend build.

Phase 6 may isolate Phase 7 residue if it imports Firebase, but only to break active Firebase dependency. The semantic cleanup remains Phase 7.

## Phase 5 Acceptance Gate

Phase 6 depends on accepted Phase 5 backend REST surfaces. Before any Phase 6 implementation is merged:

- Record that Phase 5 final review accepted the closeout.
- Record that the staged Phase 5 package was committed and pushed.
- Do not reopen Phase 5 implementation as part of Phase 6 planning or execution.

## Explicit Non-Goals

- No Phase 7 semantic cleanup of Valorie/domain/tenant/invite/migration residue.
- No redesign of tenants, organizations, workspaces, invites, or sharing.
- No public registration or anonymous API/library access.
- No Firebase Auth, Firebase ID token, Firestore, Firebase SDK compatibility layer, or new Firebase project.
- No Agent, LLMWiki, Chat UI, MCP, RAG retrieval, pgvector indexing, embedding, or Phase 9 vector work.
- No broad UI redesign beyond necessary frontend REST rewiring.
- No historical backfill from `frameworks.artefacts_json` to child `artefacts` rows.

## Round 0 - Canonical Doc Alignment

Objective: confirm the execution boundary and produce a file-by-file inventory before changing code.

Likely scans:

```powershell
rg -n "firebase|Firebase|from ['\"]firebase|../lib/firebase|./firebase" frontend/src frontend/package.json
rg -n "localStorage|Authorization|Bearer|access_token|getAuthToken|X-Tenant-ID|user_id|tenant_id" frontend/src
rg -n "valorie|tenant|invite|migration|MigrationTool|migrate-data" frontend/src
```

Key decisions:

- Classify each Firebase-importing file as rewrite, remove, or isolate.
- Identify any backend cookie-session blocker before AuthContext work begins.
- Record Phase 7 residue explicitly instead of cleaning it semantically in Phase 6.

Acceptance:

- Phase 6 plan, checklist, and verification docs are internally consistent.
- Phase 6/7 ownership is clear.
- The executor has a concrete inventory and stop/go decision for Round 1.

## Round 1 - Cookie Session Strategy + AuthContext Foundation

Objective: make backend cookie session the only auth foundation for Phase 6. If the backend still lacks the required cookie-session contract, Round 1 owns that narrow backend repair; missing cookie support is not a reason to preserve Bearer/localStorage as the Phase 6 path.

Likely files:

- `backend_py/app/auth.py`
- `backend_py/app/api/users.py`
- backend auth/session tests
- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/lib/api.js`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/PrivateRoute.jsx`
- `frontend/src/components/Navbar.jsx`

Required backend auth contract:

- Use only the `/api/users/*` auth route family for Phase 6:
  - `POST /api/users/login`
  - `GET /api/users/me`
  - `POST /api/users/refresh`
  - `POST /api/users/logout`
- Login issues a 1h access token cookie.
- Login or refresh issues a 30d refresh token cookie.
- Auth cookies are `httpOnly`.
- Auth cookies are `Secure` in production.
- Auth cookies use `SameSite=Lax` or stricter unless a documented local-dev exception is required.
- `POST /api/users/refresh` renews the access cookie from the refresh cookie.
- `POST /api/users/logout` clears cookies and revokes or expires the refresh session as appropriate.
- Disabled users are rejected on protected access and refresh, including already-issued cookies.
- Backend auth dependencies read the access token from the cookie.
- Temporary Bearer compatibility, if retained during transition, has a documented removal gate and cannot satisfy Phase 6 closeout.
- Do not add `/api/auth/*` aliases or require the frontend to support both route families.

CSRF/cookie-auth unsafe method protection:

- Unsafe methods must have explicit protection for cookie-authenticated requests.
- At minimum, enforce Origin/Referer checks for unsafe methods.
- If `SameSite=None` is used, require stronger CSRF protection such as a double-submit token.
- Backend tests must prove:
  - allowed same-origin unsafe requests pass.
  - missing or invalid Origin/Referer rejects where policy requires it.
  - disallowed Origin rejects.
  - safe methods are not incorrectly blocked by the unsafe-method policy.
  - if `SameSite=None` is used, the stronger CSRF path is tested for both success and failure.

Target behavior:

- `login(email, password)` calls `POST /api/users/login`.
- The browser session is carried by httpOnly cookies, not localStorage.
- Refresh calls `GET /api/users/me` to restore the user.
- Expired access uses the `/api/users/refresh` contract.
- `logout()` calls `POST /api/users/logout` and clears React state.
- All API calls use `credentials: "include"`.
- `signup()` remains disabled for public self-service registration.
- Disabled-user behavior comes from backend login/current-user responses.
- There is no localStorage token fallback.

Acceptance:

- Login sets cookie session, refresh renews access, logout clears cookies/session, and 401/403 handling works without Firebase.
- `/api/users/me` restores the user from cookie auth.
- Disabled users cannot refresh or access protected routes with already-issued cookies.
- CSRF/Origin/Referer tests cover allowed same-origin, missing/invalid Origin/Referer, disallowed Origin, safe-method behavior, and SameSite=None stronger-token behavior when applicable.
- `AuthContext` has no Firebase import.
- No active auth token or session user object is persisted in `localStorage`.
- `apiFetch` includes cookies by default.

## Round 2 - Core Framework REST Wiring

Objective: move owner framework and generation flows to backend REST without frontend-supplied identity.

Likely files:

- `frontend/src/lib/api.js`
- `frontend/src/components/YourFrameworks.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/CreateFramework.jsx`
- `frontend/src/components/AIMergeMode.jsx`
- `frontend/src/components/ManualMergeMode.jsx`
- `frontend/src/components/UpdateFrameworksButton.jsx`

Backend contracts:

- `POST /api/frameworks`
- `GET /api/frameworks/my-frameworks`
- `GET /api/frameworks/my-frameworks/by-family`
- `GET /api/frameworks/{framework_id}`
- `GET /api/frameworks/{framework_id}/binding`
- `PUT /api/frameworks/{framework_id}`
- `DELETE /api/frameworks/{framework_id}`
- `POST /api/frameworks/generate-from-text`
- `POST /api/frameworks/generate-from-file`
- `POST /api/frameworks/generate-from-files`
- `POST /api/frameworks/regenerate`
- `POST /api/frameworks/ai-merge`
- `POST /api/frameworks/ai-fill`

Acceptance:

- Framework owner CRUD works through backend REST.
- Generation calls no longer attach `user_id`, `creator_id`, `tenant_id`, or tenant headers.
- No core framework data component imports Firebase.
- Deferred indexing/vector-sync UI does not report success for Phase 9-deferred 501 routes.

## Round 3 - Library + Publish/Unpublish REST

Objective: replace Firestore public library and publish flows with Phase 5 backend contracts.

Likely files:

- `frontend/src/components/Library.jsx`
- `frontend/src/components/LibraryCard.jsx`
- `frontend/src/components/PublishModal.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/lib/api.js`

Backend contracts:

- `GET /api/frameworks/public?cursor=&limit=`
- `POST /api/frameworks/{framework_id}/publish`
- `POST /api/frameworks/{framework_id}/unpublish`

Acceptance:

- Authenticated users can load published frameworks through backend REST.
- Unauthenticated users do not receive library data.
- Publish/unpublish are owner-only through backend responses.
- Library and publish components have no Firebase imports.

## Round 4 - Admin Users REST

Objective: replace Firebase admin helpers with backend admin user management.

Likely files:

- `frontend/src/components/AdminPanel.jsx`
- `frontend/src/lib/api.js`
- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/components/Navbar.jsx`

Backend contracts:

- `GET /api/admin/users`
- `POST /api/admin/users`
- `POST /api/admin/users/{user_id}/disable`
- `POST /api/admin/users/{user_id}/enable`

Acceptance:

- Super-admin can list, create, disable, and enable users through backend REST.
- Non-admin users are blocked by backend 403.
- UI does not expose or send `password_hash`.
- Admin UI uses backend `id` and `is_disabled`, not Firebase `uid` and `isBlocked`.
- Whitelist-domain Firebase UI is removed or isolated as unsupported unless a backend endpoint exists.

## Round 5 - Artefact Subresource Wiring

Objective: connect artefact editing to the Phase 5 child-resource API.

Likely files:

- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/ArtefactEditor.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/lib/api.js`

Backend contracts:

- `GET /api/frameworks/{framework_id}/artefacts`
- `POST /api/frameworks/{framework_id}/artefacts`
- `GET /api/frameworks/{framework_id}/artefacts/{artefact_id}`
- `PUT /api/frameworks/{framework_id}/artefacts/{artefact_id}`
- `DELETE /api/frameworks/{framework_id}/artefacts/{artefact_id}`

Acceptance:

- Artefact child resources are listed and mutated through backend REST.
- Parent framework identity stays in the URL path only.
- Mutation bodies do not include `framework_id`, `user_id`, or `creator_id`.
- Local draft backup, if retained, stores draft content only and no session material.

## Round 6 - Firebase SDK Removal + Closeout

Objective: remove the SDK dependency after all active imports are gone.

Likely files:

- `frontend/src/lib/firebase.js`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/.env*` references if present
- Any remaining Firebase-importing source files

Required closeout:

- Delete `frontend/src/lib/firebase.js` after imports are gone.
- Remove `firebase` from frontend dependencies.
- Remove active `VITE_FIREBASE_*` runtime references.
- Build and verify no Firebase chunk remains.
- Document Phase 7 residue still present by intent.

Acceptance:

- Active frontend source has no Firebase SDK imports.
- `frontend/package.json` and lockfile no longer include `firebase`.
- Frontend lint, tests, and build pass.
- Phase 6 verification evidence is ready for reviewer handoff.

## Security Requirements

- Backend JWT cookie is the only session trust source.
- All private requests use `credentials: "include"`.
- No frontend bearer token storage or header after the removal gate.
- No frontend-provided identity authority: no `user_id`, `creator_id`, `tenant_id`, or `X-Tenant-ID`.
- Public library remains authenticated, not anonymous.
- Admin permissions are enforced by the backend.
- Production credentialed CORS must use explicit origins, not wildcard origins.
- Cookie settings must be compatible with the selected deployment: httpOnly, secure in production, and appropriate SameSite behavior.
- Unsafe cookie-authenticated methods require explicit CSRF/cookie safeguards: at minimum Origin/Referer checks, and stronger protection such as a double-submit token if `SameSite=None` is used.
- CSRF/Origin/Referer behavior must be covered by positive and negative backend tests before Round 1 is accepted.

## Bearer/localStorage Compatibility Removal Gate

This is the most important Phase 6 gate. Phase 6 cannot close while the frontend still relies on bearer/localStorage compatibility.

Required state:

- `apiFetch` always sets `credentials: "include"` unless a request is explicitly public and documented.
- No active frontend code reads `localStorage.getItem("access_token")`.
- No active frontend code writes `localStorage.setItem("access_token", ...)`.
- No active frontend code sends `Authorization: Bearer`.
- `AuthContext` stores the current user only in React state.
- Page refresh restores the user through `/api/users/me`.
- Expired access is renewed through `/api/users/refresh`.
- Logout clears the server session and frontend state.
- Disabled users cannot refresh or access protected routes with already-issued cookies.

Non-auth local draft storage may remain only for non-sensitive draft content and must not be used as an auth/session fallback.

## Testing Strategy

Minimum frontend checks:

```powershell
cd frontend
npm run lint
npm test
npm run build
```

Minimum static checks:

```powershell
rg -n "from ['\"]firebase|firebase/" frontend/src
rg -n "frontend/src/lib/firebase|../lib/firebase|./firebase" frontend/src
rg -n "localStorage\\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken" frontend/src
rg -n "user_id|creator_id|tenant_id|X-Tenant-ID|getFirebaseUserId" frontend/src
rg -n "VITE_FIREBASE|FIREBASE_" frontend
rg -n "\"firebase\"|node_modules/firebase" frontend/package.json frontend/package-lock.json
```

Suggested focused test coverage:

- AuthContext login, refresh restore, logout, and 401/403 handling.
- Backend auth/session tests for login cookies, `/api/users/me` cookie auth, `/api/users/refresh`, logout cookie clearing/session expiry, disabled-user protected access, and disabled-user refresh rejection.
- Backend CSRF/Origin tests for allowed same-origin unsafe pass, missing/invalid Origin/Referer rejection where policy requires, disallowed Origin rejection, safe methods not incorrectly blocked, and SameSite=None double-submit or stronger-token behavior if applicable.
- PrivateRoute behavior for unauthenticated users.
- Owner framework list/detail/update/delete flows.
- Generation request payloads exclude identity fields.
- Authenticated public library list.
- Publish/unpublish owner flow.
- Admin user list/create/disable/enable and non-admin 403 handling.
- Artefact list/create/update/delete.

Backend auth/session tests are required when Round 1 verifies or repairs backend cookie-session behavior.

## Verification Checklist

- Phase 6 final verification should record exact commands and outputs in `verification.md`.
- Forbidden Firebase scans must pass.
- Forbidden bearer/localStorage scans must pass.
- Forbidden frontend identity propagation scans must pass.
- Frontend lint/test/build must pass.
- Browser smoke checks should cover login, refresh, framework list, library, publish/unpublish, admin access, artefact edit, and logout.
- Backend auth/session verification should cover login cookies, cookie-authenticated `/api/users/me`, refresh renewal, logout clearing/revocation, and disabled-user rejection on protected access and refresh.
- Backend CSRF/Origin verification should include positive and negative unsafe-method tests plus safe-method non-blocking tests.
- Phase 5 accepted-closeout evidence should be recorded before Phase 6 implementation is merged.
- The final report should list Phase 7 deferrals and confirm they were not semantically cleaned in Phase 6.

## Reviewer Handoff Criteria

The reviewer should receive:

- File list of all frontend files changed, deleted, or isolated.
- Endpoint mapping for every migrated flow.
- Evidence that active frontend Firebase imports are gone.
- Evidence that the Firebase package is uninstalled.
- Evidence that bearer/localStorage auth compatibility is removed.
- Evidence that the backend cookie-session contract is present or was repaired in Round 1.
- Evidence that only `/api/users/*` auth endpoints are used for Phase 6.
- Evidence that CSRF/Origin/Referer tests pass.
- Evidence that Phase 5 final review accepted the closeout and the staged package was committed and pushed.
- Evidence that no frontend identity fields are sent as authority.
- Frontend lint/test/build outputs.
- Manual smoke-test notes.
- Explicit Phase 7 deferral list.

Do not ask the reviewer to accept Phase 6 if any Firebase SDK import, Firebase package dependency, bearer token storage, or `Authorization: Bearer` path remains active in the frontend.

## Suggested Executor Prompt For Round 0/1 Only

Use this prompt for the first executor pass only:

```text
Use $migration-phase-executor.

Project:
C:\Users\micha\Desktop\project\framework

Task:
Implement Phase 6 Round 0 and Round 1 only. Do not implement Rounds 2-6. Do not perform code review.

Read first:
- MIGRATION_PHASES.md
- docs/PERSONAL_USE_BOUNDARY.md
- docs/migration/README.md
- docs/migration/decisions/ADR-0001-auth-strategy.md
- docs/migration/phases/phase-05-backend-firestore-business/checklist.md
- docs/migration/phases/phase-05-backend-firestore-business/phase-report.md
- docs/migration/phases/phase-05-backend-firestore-business/verification.md
- docs/migration/phases/phase-06-frontend-defirebase/checklist.md
- docs/migration/phases/phase-06-frontend-defirebase/phase-plan.md
- docs/migration/phases/phase-06-frontend-defirebase/phase-report.md
- docs/migration/phases/phase-06-frontend-defirebase/verification.md

Round 0:
- Produce a focused Firebase/auth/token/identity inventory for frontend/src and frontend package files.
- Classify Firebase-importing files as rewrite, remove, or isolate.
- Record whether backend cookie-session support is already present before changing AuthContext.
- Preserve Phase 7 boundary for Valorie/domain/tenant/invite/migration semantic cleanup.

Round 1:
- Replace active Firebase Auth usage in AuthContext with backend cookie-session auth.
- If backend cookie-session support is absent or incomplete, implement the narrow backend auth/session repair in this round.
- Required backend auth contract: 1h access token cookie, 30d refresh token cookie, httpOnly cookies, Secure in production, SameSite=Lax or stricter unless documented local-dev exception, /api/users/refresh, /api/users/logout clearing cookies and revoking/expiring refresh session as appropriate, disabled-user rejection on protected access and refresh including already-issued cookies, and auth dependencies reading access token from cookie.
- Use only the /api/users/* auth route family; do not add or depend on /api/auth/* aliases.
- Protect unsafe cookie-authenticated methods explicitly: at minimum Origin/Referer checks; if SameSite=None is used, add stronger CSRF protection such as a double-submit token.
- Add backend CSRF/Origin tests covering allowed same-origin unsafe pass, missing/invalid Origin/Referer rejection where policy requires, disallowed Origin rejection, safe methods not incorrectly blocked, and SameSite=None stronger-token success/failure if applicable.
- Make the shared API client send credentials: "include".
- Remove bearer/localStorage auth token persistence from active auth flow.
- Use /api/users/login, /api/users/refresh, /api/users/me, and /api/users/logout as the frontend auth contract.
- Restore the frontend user from /api/users/me using cookie auth; expired access must use refresh; do not add any localStorage token fallback.
- Keep public signup disabled.
- Do not rewire framework/library/admin/artefact components except as required to keep auth compilation passing.

Acceptance:
- Login sets cookie session, /api/users/me works with cookie auth, /api/users/refresh renews the access cookie, and logout clears cookies/session.
- Disabled users cannot refresh or access protected routes with already-issued cookies.
- CSRF/Origin/Referer positive and negative backend tests pass.
- AuthContext and login/private-route flow have no active Firebase imports.
- No active frontend code persists access_token to localStorage.
- All private API requests use credentials: "include".
- Temporary Bearer compatibility, if retained during the round, has a documented removal gate and cannot satisfy Phase 6 closeout.
- Update Phase 6 checklist and verification with exact commands/results, but do not mark Phase 6 complete.
```
