# Phase 06 Verification - Frontend de-Firebase

Planning status: verification plan only. No Phase 6 implementation has been verified yet, and Phase 6 is not complete.

## Verification Principles

- Record exact commands and outputs after each implementation round.
- Keep evidence scoped to frontend de-Firebase work.
- Do not use this document as code review.
- Do not mark Phase 6 complete until Round 6 passes and a reviewer accepts it.
- Round 1 owns the narrow backend cookie-session repair if support is absent or incomplete. Record backend commands/results separately and do not preserve Bearer/localStorage as the Phase 6 path.
- Phase 6 uses only the `/api/users/*` auth route family: `POST /api/users/login`, `GET /api/users/me`, `POST /api/users/refresh`, and `POST /api/users/logout`.
- Before Phase 6 implementation is merged, verification must record that Phase 5 final review accepted the closeout, the staged package was committed and pushed, and Phase 6 planning may proceed.

## Round 0 Verification - Canonical Doc Alignment

Planned commands:

```powershell
rg -n "firebase|Firebase|from ['\"]firebase|../lib/firebase|./firebase" frontend/src frontend/package.json
rg -n "localStorage|Authorization|Bearer|access_token|getAuthToken|X-Tenant-ID|user_id|tenant_id" frontend/src
rg -n "valorie|tenant|invite|migration|MigrationTool|migrate-data" frontend/src
rg -n "/api/auth|api/auth" MIGRATION_PHASES.md docs/migration/phases/phase-06-frontend-defirebase frontend/src backend_py/app
```

Expected evidence:

- Firebase-importing files are inventoried.
- Bearer/localStorage compatibility paths are inventoried.
- Phase 7 residue is listed separately from Phase 6 Firebase dependency removal.
- Backend cookie-session blocker, if any, is recorded before Round 1 proceeds.
- No Phase 6 plan or active frontend/backend contract introduces `/api/auth/*` aliases.
- Phase 5 accepted-closeout evidence is confirmed before merge.

Current result: not run for implementation.

## Round 1 Verification - Cookie Session + AuthContext

Planned commands:

```powershell
rg -n "onAuthStateChanged|signInWithEmailAndPassword|firebase/auth|firebase/firestore|../lib/firebase|./firebase" frontend/src/contexts frontend/src/components/Login.jsx frontend/src/components/PrivateRoute.jsx frontend/src/lib/api.js
rg -n "localStorage\\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken" frontend/src/contexts frontend/src/lib
rg -n "credentials:\\s*['\"]include['\"]" frontend/src
rg -n "refresh|set_cookie|delete_cookie|httponly|samesite|secure|Origin|Referer|csrf|Bearer|Authorization" backend_py/app/auth.py backend_py/app/api/users.py backend_py/tests
```

Planned behavior checks:

- Login succeeds through `POST /api/users/login`.
- Login sets a 1h access token cookie and a 30d refresh token cookie.
- Auth cookies are httpOnly, Secure in production, and SameSite=Lax or stricter unless a documented local-dev exception is required.
- `/api/users/me` restores the user through cookie auth.
- Expired access uses `POST /api/users/refresh` to renew the access cookie.
- `/api/users/logout` clears cookies and revokes or expires the refresh session as appropriate.
- Backend auth dependencies read the access token from the cookie.
- Unsafe cookie-authenticated methods have at least Origin/Referer checks.
- Allowed same-origin unsafe requests pass.
- Missing or invalid Origin/Referer rejects where policy requires it.
- Disallowed Origin rejects.
- Safe methods are not incorrectly blocked by unsafe-method CSRF policy.
- If SameSite=None is used, stronger CSRF protection such as a double-submit token is present.
- If SameSite=None is used, stronger CSRF protection is tested for success and failure.
- Disabled users cannot access protected routes with already-issued cookies.
- Disabled users cannot refresh with already-issued cookies.
- 401/403 clears in-memory user state and routes to `/login`.
- Disabled-user login/current-user rejection is handled from backend responses.
- Frontend restore flow has no localStorage token fallback.

Expected evidence:

- AuthContext has no active Firebase Auth or Firestore imports.
- `access_token` is not stored in `localStorage`.
- Shared API client includes cookies.
- Login sets cookie session.
- `/api/users/me` works with cookie auth.
- `/api/users/refresh` renews access cookie.
- Logout clears cookies/session.
- Disabled user cannot refresh or access protected routes.
- CSRF/Origin/Referer backend tests cover allowed same-origin unsafe request, missing/invalid Origin/Referer rejection where policy requires, disallowed Origin rejection, safe methods not incorrectly blocked, and SameSite=None stronger-token behavior if applicable.
- Only `/api/users/*` auth endpoints are used for the Phase 6 auth contract.

Suggested backend auth/session tests:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_admin_users.py -q
```

If Round 1 adds a dedicated cookie-session test module, include it in this focused command and record the exact result.

Required CSRF/Origin backend test matrix:

- allowed same-origin unsafe request passes.
- missing Origin/Referer rejects where the policy requires one.
- invalid Origin/Referer rejects.
- disallowed Origin rejects.
- safe methods are not incorrectly blocked by unsafe-method protection.
- if `SameSite=None` is used, stronger CSRF protection such as double-submit token is tested for both success and failure.

Current result: not run for implementation.

## Round 2 Verification - Core Framework REST

Planned commands:

```powershell
rg -n "firebase/firestore|../lib/firebase|./firebase|getFirebaseUserId|X-Tenant-ID|tenant_id|user_id|creator_id" frontend/src/lib/api.js frontend/src/components/YourFrameworks.jsx frontend/src/components/FrameworkCard.jsx frontend/src/components/FrameworkEditor.jsx frontend/src/components/CreateFramework.jsx frontend/src/components/AIMergeMode.jsx frontend/src/components/ManualMergeMode.jsx frontend/src/components/UpdateFrameworksButton.jsx
```

Planned behavior checks:

- Owner can list frameworks.
- Owner can load framework detail.
- Owner can update and delete a framework.
- Generation flows work and request payloads do not contain frontend identity fields.
- Deferred vector-sync/indexing UI does not claim success for Phase 9-deferred behavior.

Current result: not run for implementation.

## Round 3 Verification - Library + Publish/Unpublish REST

Planned commands:

```powershell
rg -n "onSnapshot|collection\\(|query\\(|where\\(|firebase/firestore|../lib/firebase|./firebase" frontend/src/components/Library.jsx frontend/src/components/PublishModal.jsx frontend/src/components/FrameworkCard.jsx
```

Planned behavior checks:

- Authenticated user can load `/api/frameworks/public`.
- Unauthenticated user cannot see public-library data.
- Owner can publish through `POST /api/frameworks/{framework_id}/publish`.
- Owner can unpublish through `POST /api/frameworks/{framework_id}/unpublish`.
- Library renders backend response fields without Firestore timestamp assumptions.

Current result: not run for implementation.

## Round 4 Verification - Admin Users REST

Planned commands:

```powershell
rg -n "getAllUsers|blockUser|unblockUser|getWhitelistDomains|addWhitelistDomain|removeWhitelistDomain|isSuperAdmin|firebase/firestore|../lib/firebase|./firebase" frontend/src/components/AdminPanel.jsx frontend/src/lib/api.js
```

Planned behavior checks:

- Super-admin can list backend users.
- Super-admin can create a user.
- Super-admin can disable and enable a user.
- Non-admin receives backend 403.
- Admin UI does not expose or submit `password_hash`.

Current result: not run for implementation.

## Round 5 Verification - Artefact Subresource Wiring

Planned commands:

```powershell
rg -n "firebase/firestore|../lib/firebase|./firebase|framework_id|user_id|creator_id" frontend/src/components/FrameworkEditor.jsx frontend/src/components/ArtefactEditor.jsx frontend/src/lib/api.js
```

Planned behavior checks:

- Owner can list artefacts for a framework.
- Owner can create, update, and delete an artefact.
- Request bodies do not include `framework_id`, `user_id`, or `creator_id`.
- Cross-user rejection is handled through backend responses.

Current result: not run for implementation.

## Round 6 Verification - Firebase SDK Removal + Closeout

Required static scans:

```powershell
rg -n "from ['\"]firebase|firebase/" frontend/src
rg -n "frontend/src/lib/firebase|../lib/firebase|./firebase" frontend/src
rg -n "VITE_FIREBASE|FIREBASE_" frontend
rg -n "\"firebase\"|node_modules/firebase" frontend/package.json frontend/package-lock.json
rg -n "localStorage\\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken" frontend/src
rg -n "user_id|creator_id|tenant_id|X-Tenant-ID|getFirebaseUserId" frontend/src
rg -n "Authorization.*Bearer|localStorage\\.(getItem|setItem).*access_token" frontend/src
```

Required frontend commands:

```powershell
cd frontend
npm run lint
npm test
npm run build
```

Expected evidence:

- No active frontend Firebase SDK imports.
- No Firebase package dependency in `package.json` or lockfile.
- No active Firebase env references.
- No bearer/localStorage auth compatibility.
- No frontend-supplied identity authority.
- Backend cookie-session contract has been verified, including refresh and disabled-user rejection.
- CSRF/Origin/Referer positive and negative backend tests have passed.
- Phase 5 accepted-closeout evidence has been confirmed before merge.
- Build output contains no Firebase chunk.

Current result: not run for implementation.

## Browser Smoke Checklist

- [ ] Login with a backend-created user.
- [ ] Confirm login sets access and refresh cookies without storing frontend tokens.
- [ ] Refresh page and remain logged in through cookie session.
- [ ] Confirm expired access is renewed through `/api/users/refresh`.
- [ ] Logout and confirm private routes require login.
- [ ] Confirm logout clears cookies/session.
- [ ] Confirm disabled user cannot refresh or access protected routes with already-issued cookies.
- [ ] Load owner framework list.
- [ ] Create or generate a framework.
- [ ] Open and save a framework.
- [ ] Load Library as authenticated user.
- [ ] Publish and unpublish an owned framework.
- [ ] Access AdminPanel as super-admin.
- [ ] Confirm non-admin admin access fails.
- [ ] List/create/update/delete artefacts.
- [ ] Confirm app has no `firebase not initialized` runtime error.

## Reviewer Handoff Evidence

The final Phase 6 handoff should include:

- Changed/removed/isolated frontend file list.
- Exact static scan commands and outputs.
- Exact frontend lint/test/build commands and outputs.
- Browser smoke notes.
- Confirmation that bearer/localStorage compatibility is removed.
- Confirmation that backend cookie-session contract is present.
- Confirmation that only `/api/users/*` auth endpoints are used.
- Confirmation that CSRF/Origin/Referer tests passed.
- Confirmation that Phase 5 accepted-closeout evidence was checked before merge.
- Confirmation that Firebase SDK dependency is removed.
- Confirmation that Phase 7 semantic cleanup was not folded into Phase 6.
- Open risks and deferrals.

## Known Planning Risks

- Cookie-session backend readiness remains the primary Round 1 risk, but it is not a stop reason for preserving Bearer/localStorage. Phase 6 Round 1 owns the narrow backend session repair if cookie support is absent or incomplete.
- CSRF/cookie-auth unsafe-method protection must be made explicit during Round 1; SameSite=None requires stronger protection such as a double-submit token.
- Phase 5 closeout documentation has been corrected to record accepted final review, committed/pushed package, and Phase 6 planning may proceed; Phase 6 should not reopen Phase 5 implementation.
- Some Firebase-importing files are also tenant/invite/migration residue. Phase 6 may remove or isolate them only to uninstall Firebase; broader semantic cleanup remains Phase 7.
- Admin UI may currently expose whitelist-domain concepts that have no Phase 5 backend endpoint. Round 4 should remove or isolate that UI instead of inventing a new backend domain-management feature.
- Artefact UI may still be coupled to legacy `frameworks.artefacts_json`; Round 5 must avoid claiming historical backfill unless a later explicit phase owns it.
