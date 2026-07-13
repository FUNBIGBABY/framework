# Phase 06 Checklist - Frontend de-Firebase

## Current Audit Correction

`P6-DEFIREBASE-CORRECTION-01` supersedes the status assertions below without
deleting their historical evidence. The current audit-grade verdict is
`pending`; `27679f8ff832a70a7f69782d8d45a52eab343525` is an implementation
candidate only, `accepted_commit` is absent, and reviewer identity, reviewed
SHA, review date, and raw verdict artifact remain unavailable.

## Governance Reconciliation - 2026-07-10

- [x] Preserve historical verdict `accepted_with_documented_deferral` for browser smoke; do not downgrade it to ordinary conditional status.
- [x] Record reviewed implementation commit `27679f8ff832a70a7f69782d8d45a52eab343525`.
- [x] Record original reviewer identity/date/raw verdict artifact as `artifact unavailable`; do not guess.
- [x] Keep browser smoke as `not run`, not passed. Recorded blocker: unavailable Docker Desktop Linux engine plus no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded admin credentials.
- [x] Assign Migration Verification Owner; trigger when the complete authorized smoke environment is available, before a release relying on these browser flows, or as an explicit later reviewer condition.
- [ ] Focused re-review attaches a named reviewer, date, raw verdict/evidence, conditions, owner, and trigger so the historical verdict becomes audit-grade. This unchecked evidence task does not downgrade the historical verdict.

Missing browser smoke is not automatically a blocker; a named reviewer may retain the documented deferral.

Round 0/1/2/3/4/5/6 implementation status: Round 0 inventory, Round 1 cookie-session/AuthContext foundation, Round 0/1 review repairs, Round 2 core framework REST wiring, Round 2 review repairs, Round 3 Library plus publish/unpublish REST wiring, Round 4 Admin users REST wiring, Round 5 artefact child-resource UI wiring, and Round 6 Firebase SDK removal/Bearer closeout are implemented with static scan, lint, unit-test, backend-test, and build verification. Phase 6 closeout was accepted by Migration Reviewer with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable. Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.

## Closeout Status

- [x] Phase 6 closeout historically accepted with documented browser-smoke deferral.
- [x] Acceptance recorded with browser smoke deferred due to unavailable Docker/Postgres/seeded local environment.
- [x] Round 6 closeout commit recorded: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- [x] Browser smoke is not claimed as run.

## Required Context

- [x] Read `MIGRATION_PHASES.md`, especially Phase 6 and the Phase 7 boundary.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read Phase 5 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Read Phase 6 `phase-report.md` for current planning status and addressed reviewer findings.
- [x] Confirm Phase 5 backend REST surfaces are available for frontend use.
- [x] Record that Phase 5 final review accepted the closeout before any Phase 6 implementation is merged.
- [x] Confirm Phase 6 does not reopen Phase 5 implementation while using accepted Phase 5 REST surfaces.
- [x] Confirm Phase 6 is not being used for semantic Valorie/domain/tenant/invite/migration cleanup.

## Phase Guardrails

- [x] Keep Phase 6 focused on removing active Firebase frontend runtime dependency and SDK usage.
- [x] Round 0/1 execution began only after planning context was read.
- [x] Do not perform code review.
- [x] Do not add public registration, anonymous access, OAuth, Firebase Auth, or Firebase ID token flow.
- [x] Do not trust frontend-provided `user_id`, `creator_id`, `tenant_id`, or tenant headers.
- [x] Do not keep bearer token or session user data in `localStorage` after the compatibility removal gate.
- [x] Do not introduce dual `/api/auth/*` and `/api/users/*` auth contracts.
- [x] Do not reopen Phase 5 implementation while checking the Phase 5 acceptance gate.
- [x] Do not expand Phase 6 into Phase 7 semantic cleanup.

## Round 0 - Canonical Doc Alignment

- [x] Re-read the canonical Phase 6 and Phase 7 sections in `MIGRATION_PHASES.md`.
- [x] Reconcile Phase 6 docs with the personal-use boundary and ADR-0001.
- [x] Scan `frontend/src` for Firebase imports, Firestore calls, Firebase Auth calls, `localStorage` auth token usage, bearer headers, and tenant/user identity propagation.
- [x] Scan `frontend/package.json` and `frontend/package-lock.json` for the `firebase` package.
- [x] Inventory Firebase-importing frontend files and classify each as rewrite, remove, or isolate.
- [x] Record whether backend cookie-session support is already present before starting Round 1.
- [x] Keep any Valorie/domain/tenant/invite/migration semantic residue listed as Phase 7 deferral unless it must be isolated to uninstall Firebase.

Acceptance criteria:

- [x] The executor has a concrete file/module inventory for Phase 6.
- [x] Any conflict between cookie-session expectations and current backend behavior is assigned to Round 1 narrow backend session repair.
- [x] The Phase 6/Phase 7 boundary remains explicit.

## Round 1 - Cookie Session Strategy + AuthContext Foundation

- [x] If backend cookie-session support is absent or incomplete, implement the narrow backend auth/session repair in this round before relying on frontend cookie auth.
- [x] Do not preserve 7d Bearer + `localStorage` as the Phase 6 path.
- [x] Use the canonical Phase 6 auth route family only: `POST /api/users/login`, `GET /api/users/me`, `POST /api/users/refresh`, and `POST /api/users/logout`.
- [x] Do not add or depend on `/api/auth/refresh`, `/api/auth/logout`, or other `/api/auth/*` aliases.
- [x] Ensure backend login issues a 1h access token cookie.
- [x] Ensure backend login or refresh issues a 30d refresh token cookie.
- [x] Ensure auth cookies are `httpOnly`.
- [x] Ensure auth cookies are `Secure` in production.
- [x] Ensure auth cookies use `SameSite=Lax` or stricter unless a documented local-dev exception is required.
- [x] Add or verify `POST /api/users/refresh`.
- [x] Ensure `POST /api/users/logout` clears auth cookies and revokes or expires the refresh session as appropriate.
- [x] Ensure disabled users are rejected on protected access and refresh, including already-issued cookies.
- [x] Ensure backend auth dependencies read the access token from the cookie.
- [x] If temporary Bearer compatibility is retained during the round, document the exact removal gate and keep it blocked from Phase 6 closeout.
- [x] Protect cookie-authenticated unsafe methods with explicit CSRF/cookie safeguards.
- [x] At minimum, enforce Origin/Referer checks for unsafe methods.
- [x] SameSite=None is not used in Round 1; double-submit-token CSRF is not applicable.
- [x] Add positive and negative backend tests for cookie-authenticated unsafe method protection.
- [x] Test allowed same-origin unsafe requests pass.
- [x] Test missing or invalid Origin/Referer rejects where policy requires it.
- [x] Test disallowed Origin rejects.
- [x] Test safe methods are not incorrectly blocked by unsafe-method CSRF policy.
- [x] SameSite=None is not used in Round 1, so stronger-token success/failure tests are not applicable.
- [x] Replace frontend Firebase Auth dependency in `AuthContext`.
- [x] Use backend self-hosted auth only: `POST /api/users/login`, `POST /api/users/refresh`, `GET /api/users/me`, and `POST /api/users/logout`.
- [x] Ensure all frontend API calls use `credentials: "include"`.
- [x] Keep the authenticated user only in React state; do not persist bearer tokens or session user state in `localStorage`.
- [x] Remove `onAuthStateChanged`, `signInWithEmailAndPassword`, Firebase `signOut`, and Firestore user profile reads/writes from active auth flow.
- [x] Keep public signup disabled in the UI and route behavior.
- [x] Replace disabled-user checks with backend responses, not Firebase user-block checks.
- [x] Restore the frontend user from `/api/users/me` using cookie auth on page load.
- [x] When access cookies expire, use the refresh contract instead of any localStorage token fallback.
- [x] Handle 401/403 by clearing in-memory session and routing to `/login`.
- [x] Keep tenant update/refresh helpers from importing Firebase; use `/api/users/me` for refresh and defer tenant semantics to Phase 7.

Likely files:

- [x] `backend_py/app/auth.py`
- [x] `backend_py/app/api/users.py`
- [x] backend auth/session tests
- [x] `frontend/src/lib/api.js`
- [x] `frontend/src/contexts/AuthContext.jsx`
- [x] `frontend/src/components/Login.jsx`
- [x] `frontend/src/components/PrivateRoute.jsx`
- [x] `frontend/src/components/Navbar.jsx`

Acceptance criteria:

- [x] Login sets the required access and refresh cookies.
- [x] Refreshing the page restores session through the httpOnly cookie and `/api/users/me`.
- [x] Expired access uses `/api/users/refresh` to renew the access cookie.
- [x] Logout clears the server session cookie and frontend state.
- [x] Disabled users cannot access protected routes or refresh with already-issued cookies.
- [x] CSRF/Origin/Referer backend tests pass for allowed same-origin, missing/invalid origin, disallowed origin, safe-method behavior, and any SameSite=None stronger-token path.
- [x] `AuthContext` and login UI have no active Firebase imports.
- [x] No auth token is read from or written to `localStorage`.
- [x] All auth and private requests use `credentials: "include"`.

## Round 2 - Core Framework REST Wiring

- [x] Remove Firebase imports from `frontend/src/lib/api.js`.
- [x] Remove `getFirebaseUserId`, frontend `user_id` parameters, frontend `tenant_id` parameters, and `X-Tenant-ID` headers from active API calls.
- [x] Wire framework create/list/detail/update/delete flows to Phase 5 backend REST endpoints.
- [x] Wire generation flows to backend REST without identity fields in JSON bodies, query strings, or forms.
- [x] Keep create payload defaults separate from update patch payloads so partial owner autosave/save requests do not default missing `family`, `confidence`, or `_raw`.
- [x] Omit empty `_raw` objects from update payloads so editor autosave/save cannot clear backend raw framework JSON.
- [x] Rewire `YourFrameworks.jsx` to backend list endpoints.
- [x] Rewire `FrameworkCard.jsx` update/delete/unpublish behavior to backend REST.
- [x] Rewire `FrameworkEditor.jsx` load/save/regenerate/export flows to backend REST.
- [x] Rewire `AIMergeMode.jsx` and `ManualMergeMode.jsx` away from Firestore.
- [x] Rewire or isolate `UpdateFrameworksButton.jsx` so it does not call Firebase or obsolete vector-sync paths as active production behavior.
- [x] Route authenticated backend-cookie users without a real `tenantId` to the legacy `/personal/frameworks` UI shim after login and from `/`.
- [x] Keep `AuthContext` backend users at `tenantId: null`; do not synthesize a real tenant/workspace identity.
- [x] Remove `TenantCreationModal` from the active post-login route path so normal backend-cookie login does not create Firestore tenant documents.
- [x] Allow authenticated users without `user.tenantId` through the core framework `TenantRoute` shell.

Acceptance criteria:

- [x] Owner framework list/detail/update/delete code paths are wired to backend REST helpers.
- [ ] Browser smoke confirms owner framework list/detail/update/delete flows after login.
- [x] Generation requests do not include frontend-supplied user or tenant identity.
- [x] No core framework component imports `frontend/src/lib/firebase.js` or `firebase/firestore`.
- [x] The UI handles Phase 9-deferred indexing paths without pretending vector sync succeeded.
- [x] Legacy tenant route params are treated only as temporary UI route shims and are not sent as backend framework API identity.

## Round 3 - Library + Publish/Unpublish REST

- [x] Rewire `Library.jsx` from Firestore `onSnapshot` to authenticated `GET /api/frameworks/public`.
- [x] Replace realtime Firestore subscription with short polling, manual reload, or one-shot fetch per canonical Phase 6 guidance.
- [x] Adapt Library UI to backend public-list response shape: `items`, `next_cursor`, `limit`, `preview_artefacts`, `published_at`, and `tags`.
- [x] Rewire `PublishModal.jsx` to `POST /api/frameworks/{framework_id}/publish`.
- [x] Rewire unpublish controls to `POST /api/frameworks/{framework_id}/unpublish`.
- [x] Remove non-blocking `push-framework` vector-store call from publish UI unless it remains clearly Phase 9-deferred and non-successful.
- [x] Preserve authenticated public library behavior: public library is not anonymous access.

Acceptance criteria:

- [x] Authenticated users can see published frameworks through `/api/frameworks/public`.
- [x] Unauthenticated public-library access redirects to login or shows an auth-required state.
- [x] Owner publish and unpublish use backend REST and update the UI.
- [x] Library and publish/unpublish UI have no Firebase imports.

## Round 4 - Admin Users REST

- [x] Rewire `AdminPanel.jsx` from Firebase admin helpers to `/api/admin/users`.
- [x] Implement frontend list/create/disable/enable flows against backend admin endpoints.
- [x] Remove whitelist-domain Firestore UI or isolate it as unsupported unless a backend endpoint exists.
- [x] Treat backend 403 as the source of admin authorization truth.
- [x] Ensure admin user list does not assume Firebase `uid`; use backend user `id`.
- [x] Ensure blocked/disabled UI maps to backend `is_disabled`.

Acceptance criteria:

- [x] Super-admin can list users through backend REST.
- [x] Super-admin can create users without exposing `password_hash`.
- [x] Super-admin can disable and enable users through backend REST.
- [x] Non-admin users receive backend 403; frontend checks are convenience only.
- [x] `AdminPanel.jsx` has no Firebase imports.

## Round 5 - Artefact Subresource Wiring

- [x] Wire framework artefact list/create/get/update/delete to `/api/frameworks/{framework_id}/artefacts`.
- [x] Keep parent `framework_id` in the URL path only; never send `framework_id`, `user_id`, or `creator_id` in mutation bodies.
- [x] Adapt `FrameworkEditor.jsx` artefact editing to backend child-resource shape.
- [x] Preserve local draft backup only for non-sensitive draft content; do not store auth/session data.
- [x] Do not backfill or synchronize historical `frameworks.artefacts_json` into child rows unless a later explicit phase owns it.

Acceptance criteria:

- [x] Artefact operations work through backend REST for the owner.
- [x] Cross-user access is enforced by backend responses.
- [x] Artefact requests do not include frontend-supplied identity fields.
- [x] Artefact UI has no Firebase imports.

## Round 6 - Firebase SDK Removal + Closeout

- [x] Remove or isolate every active frontend file that imports `firebase/*` or `frontend/src/lib/firebase.js`.
- [x] Delete `frontend/src/lib/firebase.js` once no active imports remain.
- [x] Remove `firebase` from `frontend/package.json`.
- [x] Update `frontend/package-lock.json` by running package manager uninstall/install workflow.
- [x] Remove `VITE_FIREBASE_*` references from active frontend runtime configuration.
- [x] Ensure Firebase-importing Phase 7 residue is deleted or isolated only as needed to uninstall the SDK, with semantic cleanup deferred.
- [x] Run frontend lint, tests, and production build.
- [x] Run forbidden Firebase and bearer/localStorage scans.
- [x] Update Phase 6 report and verification evidence after implementation.

Acceptance criteria:

- [x] `rg -n "from ['\"]firebase|firebase/" frontend/src` has no active-source matches.
- [x] `rg -n "frontend/src/lib/firebase|../lib/firebase|./firebase" frontend/src` has no active-source matches.
- [x] `rg -n "\"firebase\"|node_modules/firebase" frontend/package.json frontend/package-lock.json` has no dependency matches.
- [x] `rg -n "VITE_FIREBASE|FIREBASE_" frontend` has no active runtime matches.
- [x] Frontend build output contains no Firebase chunk.
- [x] Phase 6 closeout acceptance is recorded only after Migration Reviewer accepted Round 6.

## Explicit Non-Goals

- [ ] Do not perform Phase 7 semantic cleanup of Valorie/domain/tenant/invite/migration residue.
- [ ] Do not implement or redesign tenants, workspaces, invites, organizations, or marketplace sharing semantics.
- [ ] Do not add Firebase ID token compatibility, Firebase Auth, Firestore, or a new Firebase project.
- [ ] Do not implement Agent, LLMWiki, Chat UI, MCP, RAG retrieval, pgvector indexing, or embedding.
- [ ] Do not implement anonymous public library access.
- [ ] Do not create public self-service registration.
- [ ] Do not perform broad UI redesign beyond the frontend de-Firebase rewiring needed for Phase 6.

## Security Requirements

- [x] Backend JWT cookie is the only session trust source for frontend requests.
- [x] Protected endpoint auth reads access cookies only; refresh JWTs cannot authenticate protected endpoints and `Authorization: Bearer` is rejected.
- [x] Cookies must be sent with `credentials: "include"`.
- [x] `localStorage` and `sessionStorage` must not store auth tokens or durable session user objects.
- [x] Frontend must not send `Authorization: Bearer` after the removal gate.
- [x] Shared frontend API requests refresh once on normal expired-access `401` responses and do not refresh true `403` authorization failures.
- [x] Frontend must not send `user_id`, `creator_id`, `tenant_id`, or `X-Tenant-ID` as identity authority.
- [x] Admin permissions must be enforced by backend responses, not frontend button visibility.
- [x] Private APIs and authenticated public library remain login-required.
- [x] Cookie/CORS behavior must not use wildcard credentialed origins in production.
- [x] Any CSRF mitigation required by backend cookie strategy must be wired consistently before write requests are accepted.
- [x] Unsafe cookie-authenticated methods must be protected at minimum by Origin/Referer checks.
- [x] SameSite=None is not used in Round 1; double-submit-token CSRF is not applicable.
- [x] CSRF/Origin/Referer tests must cover both allowed and rejected cookie-authenticated unsafe requests.

## Bearer/localStorage Compatibility Removal Gate

This gate no longer blocks Round 6 implementation. Migration Reviewer closeout acceptance has been recorded in this checklist after Round 6 closeout.

- [x] `/api/users/login` establishes the browser session without requiring frontend token persistence.
- [x] `/api/users/me` restores the current user from the cookie on page refresh.
- [x] `/api/users/refresh` renews the 1h access cookie using the 30d refresh cookie.
- [x] `/api/users/logout` clears the server session cookies and revokes or expires the refresh session as appropriate.
- [x] `frontend/src/lib/api.js` no longer reads `access_token`.
- [x] `frontend/src/lib/api.js` no longer adds `Authorization: Bearer`.
- [x] `AuthContext` no longer writes `access_token` or session user objects to `localStorage`.
- [x] A repository scan confirms no active frontend auth-token storage remains.
- [x] Backend protected auth dependencies no longer accept `Authorization: Bearer`.
- [x] `/api/users/login` and `/api/users/refresh` no longer return bearer token fields in the response body.

## Tests And Verification Checklist

- [x] `npm run lint` from `frontend/`.
- [x] `npm test` from `frontend/`.
- [x] `npm run build` from `frontend/`.
- [ ] Focused auth UI tests cover login, refresh restore, logout, 401/403 handling, and disabled-user login failure.
- [x] Backend auth/session tests cover login cookies, `/api/users/me` cookie auth, `/api/users/refresh`, logout cookie clearing/session expiry, disabled-user protected access, and disabled-user refresh rejection.
- [x] Backend auth/session tests cover strict access-vs-refresh JWT type separation for access cookies, Bearer rejection, and refresh cookies.
- [x] Shared frontend API client tests cover one-shot refresh retry, refresh-endpoint retry guard, no refresh on `403`, and failed-refresh stop behavior.
- [x] Shared frontend API payload tests cover create/update separation, update patch semantics, empty `_raw` omission, create/regenerate payload validity, and omission of frontend identity fields.
- [x] Backend CSRF/Origin tests cover allowed same-origin unsafe request, missing/invalid Origin/Referer rejection where policy requires, disallowed Origin rejection, safe methods not incorrectly blocked, and SameSite=None stronger-token behavior if applicable.
- [ ] Focused REST UI tests cover owner frameworks, public library, publish/unpublish, admin users, and artefacts.
- [x] Focused Round 5 artefact tests cover list/create/get/update/delete helper mapping, editor create/update/delete behavior, backend 403/404 surfacing, and local draft backup without auth/session data.
- [x] Focused Round 4 REST tests cover admin user list/create/disable/enable, backend 403 handling, and whitelist-domain UI absence/unsupported state.
- [x] Focused route-shell tests cover backend-cookie no-tenant login destination, root route modal suppression, and `TenantRoute` core shell pass-through.
- [x] Forbidden Firebase scan passes for active Round 5 production files; full SDK removal remains Round 6.
- [x] Forbidden bearer/localStorage auth scan passes for the active Round 1 auth surface and all `frontend/src`.
- [x] Forbidden frontend identity propagation scan passes for exact `user_id`, `creator_id`, `tenant_id`, `X-Tenant-ID`, and `getFirebaseUserId` patterns in active Round 2 production files.
- [x] Test files may contain exact identity-field strings only as intentional negative assertions.
- [x] Backend auth/session tests are run when Round 1 verifies or repairs cookie-session behavior.

## Reviewer Handoff Criteria

- [x] Phase 6 implementation report lists every frontend file changed, removed, or isolated.
- [x] Phase 6 verification records exact commands and outputs.
- [x] The reviewer receives static scan evidence for Firebase removal, bearer/localStorage removal, and identity propagation removal.
- [x] The reviewer receives frontend lint/test/build output.
- [x] The reviewer receives browser smoke blocker evidence.
- [x] The reviewer receives Phase 5 accepted-closeout evidence.
- [x] The reviewer receives backend auth/session and CSRF/Origin test evidence from Round 1.
- [x] Any Phase 7 residue intentionally left behind is listed as a deferral, not hidden as Phase 6 completion.
- [x] Phase 6 closeout acceptance is recorded in the Phase 6 docs after reviewer acceptance.
