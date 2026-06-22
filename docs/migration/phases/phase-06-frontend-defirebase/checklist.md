# Phase 06 Checklist - Frontend de-Firebase

Planning status: this is a planning checklist only. Do not mark Phase 6 complete from this document. Implementation checkboxes must remain unchecked until an executor performs and verifies the work.

## Required Context

- [ ] Read `MIGRATION_PHASES.md`, especially Phase 6 and the Phase 7 boundary.
- [ ] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [ ] Read `docs/migration/README.md`.
- [ ] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [ ] Read Phase 5 `checklist.md`, `phase-report.md`, and `verification.md`.
- [ ] Read Phase 6 `phase-report.md` for current planning status and addressed reviewer findings.
- [ ] Confirm Phase 5 backend REST surfaces are available for frontend use.
- [ ] Record that Phase 5 final review accepted the closeout before any Phase 6 implementation is merged.
- [ ] Confirm Phase 6 does not reopen Phase 5 implementation while using accepted Phase 5 REST surfaces.
- [ ] Confirm Phase 6 is not being used for semantic Valorie/domain/tenant/invite/migration cleanup.

## Phase Guardrails

- [ ] Keep Phase 6 focused on removing active Firebase frontend runtime dependency and SDK usage.
- [ ] Do not perform backend or frontend implementation while planning.
- [ ] Do not perform code review.
- [ ] Do not add public registration, anonymous access, OAuth, Firebase Auth, or Firebase ID token flow.
- [ ] Do not trust frontend-provided `user_id`, `creator_id`, `tenant_id`, or tenant headers.
- [ ] Do not keep bearer token or session user data in `localStorage` after the compatibility removal gate.
- [ ] Do not introduce dual `/api/auth/*` and `/api/users/*` auth contracts.
- [ ] Do not reopen Phase 5 implementation while checking the Phase 5 acceptance gate.
- [ ] Do not expand Phase 6 into Phase 7 semantic cleanup.

## Round 0 - Canonical Doc Alignment

- [ ] Re-read the canonical Phase 6 and Phase 7 sections in `MIGRATION_PHASES.md`.
- [ ] Reconcile Phase 6 docs with the personal-use boundary and ADR-0001.
- [ ] Scan `frontend/src` for Firebase imports, Firestore calls, Firebase Auth calls, `localStorage` auth token usage, bearer headers, and tenant/user identity propagation.
- [ ] Scan `frontend/package.json` and `frontend/package-lock.json` for the `firebase` package.
- [ ] Inventory Firebase-importing frontend files and classify each as rewrite, remove, or isolate.
- [ ] Record whether backend cookie-session support is already present before starting Round 1.
- [ ] Keep any Valorie/domain/tenant/invite/migration semantic residue listed as Phase 7 deferral unless it must be isolated to uninstall Firebase.

Acceptance criteria:

- [ ] The executor has a concrete file/module inventory for Phase 6.
- [ ] Any conflict between cookie-session expectations and current backend behavior is assigned to Round 1 narrow backend session repair.
- [ ] The Phase 6/Phase 7 boundary remains explicit.

## Round 1 - Cookie Session Strategy + AuthContext Foundation

- [ ] If backend cookie-session support is absent or incomplete, implement the narrow backend auth/session repair in this round before relying on frontend cookie auth.
- [ ] Do not preserve 7d Bearer + `localStorage` as the Phase 6 path.
- [ ] Use the canonical Phase 6 auth route family only: `POST /api/users/login`, `GET /api/users/me`, `POST /api/users/refresh`, and `POST /api/users/logout`.
- [ ] Do not add or depend on `/api/auth/refresh`, `/api/auth/logout`, or other `/api/auth/*` aliases.
- [ ] Ensure backend login issues a 1h access token cookie.
- [ ] Ensure backend login or refresh issues a 30d refresh token cookie.
- [ ] Ensure auth cookies are `httpOnly`.
- [ ] Ensure auth cookies are `Secure` in production.
- [ ] Ensure auth cookies use `SameSite=Lax` or stricter unless a documented local-dev exception is required.
- [ ] Add or verify `POST /api/users/refresh`.
- [ ] Ensure `POST /api/users/logout` clears auth cookies and revokes or expires the refresh session as appropriate.
- [ ] Ensure disabled users are rejected on protected access and refresh, including already-issued cookies.
- [ ] Ensure backend auth dependencies read the access token from the cookie.
- [ ] If temporary Bearer compatibility is retained during the round, document the exact removal gate and keep it blocked from Phase 6 closeout.
- [ ] Protect cookie-authenticated unsafe methods with explicit CSRF/cookie safeguards.
- [ ] At minimum, enforce Origin/Referer checks for unsafe methods.
- [ ] If `SameSite=None` is used, require stronger CSRF protection such as a double-submit token.
- [ ] Add positive and negative backend tests for cookie-authenticated unsafe method protection.
- [ ] Test allowed same-origin unsafe requests pass.
- [ ] Test missing or invalid Origin/Referer rejects where policy requires it.
- [ ] Test disallowed Origin rejects.
- [ ] Test safe methods are not incorrectly blocked by unsafe-method CSRF policy.
- [ ] If `SameSite=None` is used, test the stronger CSRF protection path such as double-submit token success and failure.
- [ ] Replace frontend Firebase Auth dependency in `AuthContext`.
- [ ] Use backend self-hosted auth only: `POST /api/users/login`, `POST /api/users/refresh`, `GET /api/users/me`, and `POST /api/users/logout`.
- [ ] Ensure all frontend API calls use `credentials: "include"`.
- [ ] Keep the authenticated user only in React state; do not persist bearer tokens or session user state in `localStorage`.
- [ ] Remove `onAuthStateChanged`, `signInWithEmailAndPassword`, Firebase `signOut`, and Firestore user profile reads/writes from active auth flow.
- [ ] Keep public signup disabled in the UI and route behavior.
- [ ] Replace disabled-user checks with backend responses, not Firebase user-block checks.
- [ ] Restore the frontend user from `/api/users/me` using cookie auth on page load.
- [ ] When access cookies expire, use the refresh contract instead of any localStorage token fallback.
- [ ] Handle 401/403 by clearing in-memory session and routing to `/login`.
- [ ] Keep tenant update/refresh helpers from importing Firebase; use `/api/users/me` for refresh and defer tenant semantics to Phase 7.

Likely files:

- [ ] `backend_py/app/auth.py`
- [ ] `backend_py/app/api/users.py`
- [ ] backend auth/session tests
- [ ] `frontend/src/lib/api.js`
- [ ] `frontend/src/contexts/AuthContext.jsx`
- [ ] `frontend/src/components/Login.jsx`
- [ ] `frontend/src/components/PrivateRoute.jsx`

Acceptance criteria:

- [ ] Login sets the required access and refresh cookies.
- [ ] Refreshing the page restores session through the httpOnly cookie and `/api/users/me`.
- [ ] Expired access uses `/api/users/refresh` to renew the access cookie.
- [ ] Logout clears the server session cookie and frontend state.
- [ ] Disabled users cannot access protected routes or refresh with already-issued cookies.
- [ ] CSRF/Origin/Referer backend tests pass for allowed same-origin, missing/invalid origin, disallowed origin, safe-method behavior, and any SameSite=None stronger-token path.
- [ ] `AuthContext` and login UI have no active Firebase imports.
- [ ] No auth token is read from or written to `localStorage`.
- [ ] All auth and private requests use `credentials: "include"`.

## Round 2 - Core Framework REST Wiring

- [ ] Remove Firebase imports from `frontend/src/lib/api.js`.
- [ ] Remove `getFirebaseUserId`, frontend `user_id` parameters, frontend `tenant_id` parameters, and `X-Tenant-ID` headers from active API calls.
- [ ] Wire framework create/list/detail/update/delete flows to Phase 5 backend REST endpoints.
- [ ] Wire generation flows to backend REST without identity fields in JSON bodies, query strings, or forms.
- [ ] Rewire `YourFrameworks.jsx` to backend list endpoints.
- [ ] Rewire `FrameworkCard.jsx` update/delete/unpublish behavior to backend REST.
- [ ] Rewire `FrameworkEditor.jsx` load/save/regenerate/export flows to backend REST.
- [ ] Rewire `AIMergeMode.jsx` and `ManualMergeMode.jsx` away from Firestore.
- [ ] Rewire or isolate `UpdateFrameworksButton.jsx` so it does not call Firebase or obsolete vector-sync paths as active production behavior.

Acceptance criteria:

- [ ] Owner framework list/detail/update/delete flows work through backend REST after login.
- [ ] Generation requests do not include frontend-supplied user or tenant identity.
- [ ] No core framework component imports `frontend/src/lib/firebase.js` or `firebase/firestore`.
- [ ] The UI handles Phase 9-deferred indexing paths without pretending vector sync succeeded.

## Round 3 - Library + Publish/Unpublish REST

- [ ] Rewire `Library.jsx` from Firestore `onSnapshot` to authenticated `GET /api/frameworks/public`.
- [ ] Replace realtime Firestore subscription with short polling, manual reload, or one-shot fetch per canonical Phase 6 guidance.
- [ ] Adapt Library UI to backend public-list response shape: `items`, `next_cursor`, `limit`, `preview_artefacts`, `published_at`, and `tags`.
- [ ] Rewire `PublishModal.jsx` to `POST /api/frameworks/{framework_id}/publish`.
- [ ] Rewire unpublish controls to `POST /api/frameworks/{framework_id}/unpublish`.
- [ ] Remove non-blocking `push-framework` vector-store call from publish UI unless it remains clearly Phase 9-deferred and non-successful.
- [ ] Preserve authenticated public library behavior: public library is not anonymous access.

Acceptance criteria:

- [ ] Authenticated users can see published frameworks through `/api/frameworks/public`.
- [ ] Unauthenticated public-library access redirects to login or shows an auth-required state.
- [ ] Owner publish and unpublish use backend REST and update the UI.
- [ ] Library and publish/unpublish UI have no Firebase imports.

## Round 4 - Admin Users REST

- [ ] Rewire `AdminPanel.jsx` from Firebase admin helpers to `/api/admin/users`.
- [ ] Implement frontend list/create/disable/enable flows against backend admin endpoints.
- [ ] Remove whitelist-domain Firestore UI or isolate it as unsupported unless a backend endpoint exists.
- [ ] Treat backend 403 as the source of admin authorization truth.
- [ ] Ensure admin user list does not assume Firebase `uid`; use backend user `id`.
- [ ] Ensure blocked/disabled UI maps to backend `is_disabled`.

Acceptance criteria:

- [ ] Super-admin can list users through backend REST.
- [ ] Super-admin can create users without exposing `password_hash`.
- [ ] Super-admin can disable and enable users through backend REST.
- [ ] Non-admin users receive backend 403; frontend checks are convenience only.
- [ ] `AdminPanel.jsx` has no Firebase imports.

## Round 5 - Artefact Subresource Wiring

- [ ] Wire framework artefact list/create/get/update/delete to `/api/frameworks/{framework_id}/artefacts`.
- [ ] Keep parent `framework_id` in the URL path only; never send `framework_id`, `user_id`, or `creator_id` in mutation bodies.
- [ ] Adapt `FrameworkEditor.jsx` artefact editing to backend child-resource shape.
- [ ] Preserve local draft backup only for non-sensitive draft content; do not store auth/session data.
- [ ] Do not backfill or synchronize historical `frameworks.artefacts_json` into child rows unless a later explicit phase owns it.

Acceptance criteria:

- [ ] Artefact operations work through backend REST for the owner.
- [ ] Cross-user access is enforced by backend responses.
- [ ] Artefact requests do not include frontend-supplied identity fields.
- [ ] Artefact UI has no Firebase imports.

## Round 6 - Firebase SDK Removal + Closeout

- [ ] Remove or isolate every active frontend file that imports `firebase/*` or `frontend/src/lib/firebase.js`.
- [ ] Delete `frontend/src/lib/firebase.js` once no active imports remain.
- [ ] Remove `firebase` from `frontend/package.json`.
- [ ] Update `frontend/package-lock.json` by running package manager uninstall/install workflow.
- [ ] Remove `VITE_FIREBASE_*` references from active frontend runtime configuration.
- [ ] Ensure Firebase-importing Phase 7 residue is deleted or isolated only as needed to uninstall the SDK, with semantic cleanup deferred.
- [ ] Run frontend lint, tests, and production build.
- [ ] Run forbidden Firebase and bearer/localStorage scans.
- [ ] Update Phase 6 report and verification evidence after implementation.

Acceptance criteria:

- [ ] `rg -n "from ['\"]firebase|firebase/" frontend/src` has no active-source matches.
- [ ] `rg -n "frontend/src/lib/firebase|../lib/firebase|./firebase" frontend/src` has no active-source matches.
- [ ] `rg -n "\"firebase\"|node_modules/firebase" frontend/package.json frontend/package-lock.json` has no dependency matches.
- [ ] `rg -n "VITE_FIREBASE|FIREBASE_" frontend` has no active runtime matches.
- [ ] Frontend build output contains no Firebase chunk.
- [ ] Phase 6 remains not marked complete until reviewer acceptance.

## Explicit Non-Goals

- [ ] Do not perform Phase 7 semantic cleanup of Valorie/domain/tenant/invite/migration residue.
- [ ] Do not implement or redesign tenants, workspaces, invites, organizations, or marketplace sharing semantics.
- [ ] Do not add Firebase ID token compatibility, Firebase Auth, Firestore, or a new Firebase project.
- [ ] Do not implement Agent, LLMWiki, Chat UI, MCP, RAG retrieval, pgvector indexing, or embedding.
- [ ] Do not implement anonymous public library access.
- [ ] Do not create public self-service registration.
- [ ] Do not perform broad UI redesign beyond the frontend de-Firebase rewiring needed for Phase 6.

## Security Requirements

- [ ] Backend JWT cookie is the only session trust source for frontend requests.
- [ ] Cookies must be sent with `credentials: "include"`.
- [ ] `localStorage` and `sessionStorage` must not store auth tokens or durable session user objects.
- [ ] Frontend must not send `Authorization: Bearer` after the removal gate.
- [ ] Frontend must not send `user_id`, `creator_id`, `tenant_id`, or `X-Tenant-ID` as identity authority.
- [ ] Admin permissions must be enforced by backend responses, not frontend button visibility.
- [ ] Private APIs and authenticated public library remain login-required.
- [ ] Cookie/CORS behavior must not use wildcard credentialed origins in production.
- [ ] Any CSRF mitigation required by backend cookie strategy must be wired consistently before write requests are accepted.
- [ ] Unsafe cookie-authenticated methods must be protected at minimum by Origin/Referer checks.
- [ ] If `SameSite=None` is used, stronger CSRF protection such as a double-submit token is required.
- [ ] CSRF/Origin/Referer tests must cover both allowed and rejected cookie-authenticated unsafe requests.

## Bearer/localStorage Compatibility Removal Gate

This gate blocks Phase 6 closeout.

- [ ] `/api/users/login` establishes the browser session without requiring frontend token persistence.
- [ ] `/api/users/me` restores the current user from the cookie on page refresh.
- [ ] `/api/users/refresh` renews the 1h access cookie using the 30d refresh cookie.
- [ ] `/api/users/logout` clears the server session cookies and revokes or expires the refresh session as appropriate.
- [ ] `frontend/src/lib/api.js` no longer reads `access_token`.
- [ ] `frontend/src/lib/api.js` no longer adds `Authorization: Bearer`.
- [ ] `AuthContext` no longer writes `access_token` or session user objects to `localStorage`.
- [ ] A repository scan confirms no active frontend auth-token storage remains.

## Tests And Verification Checklist

- [ ] `npm run lint` from `frontend/`.
- [ ] `npm test` from `frontend/`.
- [ ] `npm run build` from `frontend/`.
- [ ] Focused auth UI tests cover login, refresh restore, logout, 401/403 handling, and disabled-user login failure.
- [ ] Backend auth/session tests cover login cookies, `/api/users/me` cookie auth, `/api/users/refresh`, logout cookie clearing/session expiry, disabled-user protected access, and disabled-user refresh rejection.
- [ ] Backend CSRF/Origin tests cover allowed same-origin unsafe request, missing/invalid Origin/Referer rejection where policy requires, disallowed Origin rejection, safe methods not incorrectly blocked, and SameSite=None stronger-token behavior if applicable.
- [ ] Focused REST UI tests cover owner frameworks, public library, publish/unpublish, admin users, and artefacts.
- [ ] Forbidden Firebase scan passes.
- [ ] Forbidden bearer/localStorage auth scan passes.
- [ ] Forbidden frontend identity propagation scan passes.
- [ ] Backend auth/session tests are run when Round 1 verifies or repairs cookie-session behavior.

## Reviewer Handoff Criteria

- [ ] Phase 6 implementation report lists every frontend file changed, removed, or isolated.
- [ ] Phase 6 verification records exact commands and outputs.
- [ ] The reviewer receives static scan evidence for Firebase removal, bearer/localStorage removal, and identity propagation removal.
- [ ] The reviewer receives frontend lint/test/build output.
- [ ] The reviewer receives Phase 5 accepted-closeout evidence.
- [ ] The reviewer receives backend auth/session and CSRF/Origin test evidence from Round 1.
- [ ] Any Phase 7 residue intentionally left behind is listed as a deferral, not hidden as Phase 6 completion.
- [ ] Phase 6 is not marked complete until reviewer acceptance.
