# Phase 06 Verification - Frontend de-Firebase

Round 0/1/2 implementation status: Round 0 inventory, Round 1 cookie-session/AuthContext foundation, Round 0/1 reviewer repairs, Round 2 core framework REST wiring, and Round 2 review repairs have static scan, lint, unit-test, and build verification. No Round 2 browser smoke test has been run. Phase 6 is not complete; Rounds 3-6 remain open.

## Verification Principles

- Record exact commands and outputs after each implementation round.
- Keep evidence scoped to frontend de-Firebase work.
- Do not use this document as code review.
- Do not mark Phase 6 complete until Round 6 passes and a reviewer accepts it.
- Round 1 owns the narrow backend cookie-session repair if support is absent or incomplete. Record backend commands/results separately and do not preserve Bearer/localStorage as the Phase 6 path.
- Phase 6 uses only the `/api/users/*` auth route family: `POST /api/users/login`, `GET /api/users/me`, `POST /api/users/refresh`, and `POST /api/users/logout`.
- Before Phase 6 implementation is merged, verification must record that Phase 5 final review accepted the closeout, the staged package was committed and pushed, and Phase 6 planning may proceed.

## Round 0/1 Verification Results

### Phase 5 Acceptance Gate

Phase 5 `checklist.md`, `phase-report.md`, and `verification.md` were read before implementation. They record that Phase 5 final review accepted closeout, the staged Phase 5 package was committed and pushed, and Phase 6 may proceed. Phase 6 Round 0/1 did not reopen Phase 5 implementation.

### Round 0 Firebase Inventory Scan

Command:

```powershell
rg -l 'from [''\"'']firebase|firebase/|\.\./lib/firebase|\./firebase' frontend/src
```

Result:

```text
frontend/src\utils\cleanupData.js
frontend/src\migrate-data.js
frontend/src\utils\updateFrameworkTenants.js
frontend/src\components\CreateFramework.jsx
frontend/src\components\AdminPanel.jsx
frontend/src\components\FrameworkCard.jsx
frontend/src\components\FrameworkEditor.jsx
frontend/src\components\InviteAccept.jsx
frontend/src\components\Library.jsx
frontend/src\lib\firebase.js
frontend/src\components\PublishModal.jsx
frontend/src\components\TenantCreationModal.jsx
frontend/src\components\TenantSettings.jsx
frontend/src\components\UpdateFrameworksButton.jsx
frontend/src\components\YourFrameworks.jsx
frontend/src\components\YourOrganization.jsx
```

Classification:

- Rewrite in Round 2: `CreateFramework.jsx`, `FrameworkCard.jsx`, `FrameworkEditor.jsx`, `UpdateFrameworksButton.jsx`, `YourFrameworks.jsx`.
- Rewrite in Round 3: `Library.jsx`, `PublishModal.jsx`.
- Rewrite in Round 4: `AdminPanel.jsx`.
- Rewrite in Round 5: `FrameworkEditor.jsx` artefact child-resource behavior.
- Remove or isolate in Round 6 after active imports are gone: `frontend/src/lib/firebase.js`.
- Phase 7 residue, to remove or isolate only as needed for SDK uninstall: `migrate-data.js`, `utils/cleanupData.js`, `utils/updateFrameworkTenants.js`, `InviteAccept.jsx`, `TenantCreationModal.jsx`, `TenantSettings.jsx`, `YourOrganization.jsx`.

### Round 0 Firebase Package Scan

Command:

```powershell
rg -n '"firebase"|node_modules/firebase' frontend\package.json frontend\package-lock.json
```

Result: matches remain in `frontend/package.json` and `frontend/package-lock.json`, including `frontend/package.json:31: "firebase": "^12.4.0"` and `frontend/package-lock.json` entries for `firebase` / `@firebase/*`. This is expected and deferred to Round 6. Firebase was not uninstalled in Round 1.

### Round 0 Phase 7 Residue Scan

Command:

```powershell
rg -n 'valorie|Valorie|tenant|Tenant|invite|Invite|migration|MigrationTool|migrate-data' frontend\src\App.jsx frontend\src\components frontend\src\utils frontend\src\migrate-data.js frontend\src\lib\firebase.js
```

Result: numerous matches remain in `App.jsx`, `frontend/src/lib/firebase.js`, `frontend/src/migrate-data.js`, tenant/invite components, and tenant cleanup utilities. These are recorded as Phase 7 residue unless Round 6 must isolate them to remove the Firebase SDK.

### Round 0 Auth Route Alias Scan

Command:

```powershell
rg -n '/api/auth|api/auth' MIGRATION_PHASES.md docs\migration\phases\phase-06-frontend-defirebase frontend\src backend_py\app
```

Result: matches are documentation references only; no active frontend source or backend app route introduces `/api/auth/*` aliases.

### Backend Syntax Check

Command:

```powershell
backend_py\.venv\Scripts\python.exe -m py_compile backend_py\app\auth.py backend_py\app\api\users.py backend_py\app\models.py backend_py\main.py backend_py\alembic\versions\0004_phase6_refresh_session_version.py backend_py\tests\test_cookie_sessions.py
```

Result: passed with exit code `0` and no output.

### Focused Backend Auth/Cookie Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_cookie_sessions.py tests\test_auth_hardening.py tests\test_admin_users.py -q
```

Result:

```text
40 passed, 93 warnings in 10.73s
```

Coverage includes login cookies, `/api/users/me` cookie auth without bearer, `/api/users/refresh`, logout cookie clearing and refresh-version revocation, disabled-user access/refresh rejection, SameSite=None configuration clamped to Lax, the Origin/Referer unsafe-method matrix, refresh-token rejection on protected endpoints through access-cookie and temporary Bearer paths, access-token acceptance on protected endpoints, and refresh endpoint rejection of access tokens.

### Full Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
117 passed, 199 warnings in 12.57s
```

Warnings are existing Pydantic v2 deprecations and `datetime.utcnow()` deprecations, plus the same timestamp warnings in the new cookie-session paths.

### Alembic History

Command:

```powershell
cd backend_py
.\.venv\Scripts\alembic.exe -c alembic.ini history --verbose
```

Result: passed with exit code `0`. Head is `0004_phase6_refresh_session_version`, parent `0003_phase5_admin_user_disabled`.

### Alembic Offline SQL

Command:

```powershell
cd backend_py
$env:DATABASE_URL='postgresql+psycopg://test:test@localhost:5432/test'; .\.venv\Scripts\alembic.exe -c alembic.ini upgrade head --sql
```

Result: passed with exit code `0`. Offline SQL includes:

```sql
ALTER TABLE users ADD COLUMN refresh_token_version INTEGER DEFAULT '0' NOT NULL;
```

### Round 1 Active Auth Firebase Scan

Command:

```powershell
rg -n 'onAuthStateChanged|signInWithEmailAndPassword|firebase/auth|firebase/firestore|\.\./lib/firebase|\./firebase' frontend\src\contexts frontend\src\components\Login.jsx frontend\src\components\PrivateRoute.jsx frontend\src\components\Navbar.jsx frontend\src\lib\api.js
```

Result: no matches. `rg` exited `1`.

### Round 1 Bearer/localStorage and Identity Scan

Command:

```powershell
rg -n 'localStorage\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken|access_token|user_id|creator_id|tenant_id|X-Tenant-ID|getFirebaseUserId' frontend\src
```

Result: no matches. `rg` exited `1`.

### Round 1 Credentials Scan

Command:

```powershell
rg -n "credentials: 'include'|refreshSessionForRetry|skipAuthRefresh|AUTH_REFRESH_SKIP_PATHS" frontend\src\lib\api.js frontend\src\lib\api.test.js
```

Result:

```text
frontend\src\lib\api.test.js:34:      credentials: 'include',
frontend\src\lib\api.test.js:38:      credentials: 'include',
frontend\src\lib\api.js:51:const AUTH_REFRESH_SKIP_PATHS = new Set([
frontend\src\lib\api.js:66:function shouldRefreshAfterResponse(url, response, skipAuthRefresh) {
frontend\src\lib\api.js:67:  if (skipAuthRefresh || response.status !== 401) return false
frontend\src\lib\api.js:68:  return !AUTH_REFRESH_SKIP_PATHS.has(getRequestPath(url))
frontend\src\lib\api.js:71:async function refreshSessionForRetry() {
frontend\src\lib\api.js:74:    credentials: 'include',
frontend\src\lib\api.js:102:    skipAuthRefresh = false,
frontend\src\lib\api.js:108:    credentials: 'include',
frontend\src\lib\api.js:114:  if (shouldRefreshAfterResponse(url, response, skipAuthRefresh)) {
frontend\src\lib\api.js:115:    const refreshed = await refreshSessionForRetry()
frontend\src\lib\api.js:154:    credentials: 'include',
frontend\src\lib\api.js:176:    skipAuthRefresh: true,
frontend\src\lib\api.js:337:      credentials: 'include',
```

### Backend Cookie/CSRF Implementation Scan

Command:

```powershell
rg -n 'set_cookie|delete_cookie|httponly|samesite|secure|Origin|Referer|CSRF|Bearer|Authorization|refresh_token_version' backend_py\app\auth.py backend_py\app\api\users.py backend_py\main.py backend_py\tests\test_cookie_sessions.py
```

Result: expected matches in `users.py` cookie helpers, `main.py` `CookieCSRFMiddleware`, and `tests/test_cookie_sessions.py`. `auth.py` still contains temporary bearer compatibility, explicitly documented as a Phase 6 removal gate.

### Backend Access/Refresh Token Type Scan

Command:

```powershell
rg -n "typ.*access|typ.*refresh|Invalid access token|Invalid refresh token|_decode_token_payload" backend_py\app\auth.py backend_py\tests\test_cookie_sessions.py
```

Result:

```text
backend_py\app\auth.py:127:    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "typ": "access"})
backend_py\app\auth.py:141:    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "typ": "refresh"})
backend_py\app\auth.py:145:def _decode_token_payload(token: str) -> dict:
backend_py\app\auth.py:174:    payload = _decode_token_payload(token)
backend_py\app\auth.py:175:    if payload.get("typ") != "access":
backend_py\app\auth.py:178:            detail="Invalid access token",
backend_py\app\auth.py:186:    payload = _decode_token_payload(token)
backend_py\app\auth.py:187:    if payload.get("typ") != "refresh":
backend_py\app\auth.py:190:            detail="Invalid refresh token",
```

### Frontend Lint

Command:

```powershell
cd frontend
npm run lint
```

Result: passed with exit code `0`.

### Frontend Tests

Initial sandboxed command:

```powershell
cd frontend
npm test
```

Initial result: failed before tests ran because Vite/Vitest/esbuild could not read config paths in the sandbox:

```text
Cannot read directory "../../../..": Access is denied.
Could not resolve "C:\Users\micha\Desktop\project\framework\frontend\vitest.config.js"
```

Escalated rerun command:

```powershell
cd frontend
npm test
```

Latest escalated rerun result:

```text
src/lib/api.test.js (4 tests) passed in 6ms
src/App.test.jsx (13 tests) passed in 55ms
2 test files passed
17 tests passed
Duration 2.62s
```

Warning: `baseline-browser-mapping` data is over two months old.

### Frontend Build

Initial sandboxed command:

```powershell
cd frontend
npm run build
```

Initial result: failed before build compilation because Vite/esbuild could not read config paths in the sandbox:

```text
Cannot read directory "../../../..": Access is denied.
Could not resolve "C:\Users\micha\Desktop\project\framework\frontend\vite.config.js"
```

Escalated rerun command:

```powershell
cd frontend
npm run build
```

Latest escalated rerun result:

```text
159 modules transformed.
dist/index.html                 0.47 kB
dist/assets/index-DEdGCMQs.css  42.12 kB
dist/assets/index-CSojT1o_.js   1,483.70 kB
built in 9.51s
```

Warnings: `baseline-browser-mapping` and Browserslist/caniuse data are stale; one chunk is larger than 500 kB after minification. These are not Round 1 blockers.

### Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

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

Current result: implemented and verified above for Round 0.

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

Current result: implemented and verified above for Round 1.

## Round 2 Verification - Core Framework REST

Implemented in Round 2. Review repair passes updated API payload behavior, fixed the no-tenant backend-cookie route gate, suppressed the active tenant-creation modal path, and corrected verification wording. Evidence below distinguishes static scans, unit tests, lint, and build from browser smoke coverage.

### Round 2 Focused Firebase Import Scan

Command:

```powershell
rg -n "firebase/firestore|firebase/|\\.\\./lib/firebase|\\./firebase" frontend/src/lib/api.js frontend/src/components/YourFrameworks.jsx frontend/src/components/FrameworkCard.jsx frontend/src/components/FrameworkEditor.jsx frontend/src/components/CreateFramework.jsx frontend/src/components/AIMergeMode.jsx frontend/src/components/ManualMergeMode.jsx frontend/src/components/UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

This confirms the active Round 2 production files do not import Firestore/Firebase helpers.

### Round 2 Focused Bearer/Token Scan

Command:

```powershell
rg -n "localStorage\\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken|access_token" frontend/src/lib/api.js frontend/src/components/YourFrameworks.jsx frontend/src/components/FrameworkCard.jsx frontend/src/components/FrameworkEditor.jsx frontend/src/components/CreateFramework.jsx frontend/src/components/AIMergeMode.jsx frontend/src/components/ManualMergeMode.jsx frontend/src/components/UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

### Round 2 Focused Identity Field Scan

Command:

```powershell
rg -n "getFirebaseUserId|X-Tenant-ID|tenant_id|user_id|creator_id" frontend/src/lib/api.js frontend/src/components/YourFrameworks.jsx frontend/src/components/FrameworkCard.jsx frontend/src/components/FrameworkEditor.jsx frontend/src/components/CreateFramework.jsx frontend/src/components/AIMergeMode.jsx frontend/src/components/ManualMergeMode.jsx frontend/src/components/UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

This confirms exact frontend identity-field strings were not reintroduced in the active Round 2 production files. `frontend/src/lib/api.test.js` intentionally contains these strings only as negative test assertions.

### Round 2 API Payload Review Repair Tests

Initial sandboxed command:

```powershell
cd frontend
npm test -- src/lib/api.test.js
```

Initial result: failed before tests ran because Vite/Vitest/esbuild could not read config paths in the sandbox:

```text
Cannot read directory "../../../..": Access is denied.
Could not resolve "C:\Users\micha\Desktop\project\framework\frontend\vitest.config.js"
```

Escalated rerun command:

```powershell
cd frontend
npm test -- src/lib/api.test.js
```

Escalated rerun result:

```text
src/lib/api.test.js (9 tests) passed
1 test file passed
9 tests passed
Duration 1.73s
```

Coverage added in this repair: `updateFramework(id, partialData)` omits missing `family`, `confidence`, and `_raw`; `updateFramework(id, { _raw: {} })` omits `_raw`; editor autosave-style payloads do not wipe raw framework data; create/regenerate payloads remain valid; payloads and headers do not include frontend identity fields.

Warning: `baseline-browser-mapping` data is over two months old.

### Round 2 Frontend Lint

Command:

```powershell
cd frontend
npm run lint
```

Result: passed with exit code `0`.

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

### Round 2 Frontend Tests

Initial sandboxed command:

```powershell
cd frontend
npm test
```

Initial result: failed before tests ran because Vite/Vitest/esbuild could not read config paths in the sandbox:

```text
Cannot read directory "../../../..": Access is denied.
Could not resolve "C:\Users\micha\Desktop\project\framework\frontend\vitest.config.js"
```

Escalated rerun command:

```powershell
cd frontend
npm test
```

Escalated rerun result:

```text
src/lib/api.test.js (9 tests) passed
src/App.test.jsx (13 tests) passed
2 test files passed
22 tests passed
Duration 1.94s
```

Warning: `baseline-browser-mapping` data is over two months old.

### Round 2 Frontend Build

Initial sandboxed command:

```powershell
cd frontend
npm run build
```

Initial result: failed before build compilation because Vite/esbuild could not read config paths in the sandbox:

```text
Cannot read directory "../../../..": Access is denied.
Could not resolve "C:\Users\micha\Desktop\project\framework\frontend\vite.config.js"
```

Escalated rerun command:

```powershell
cd frontend
npm run build
```

Escalated rerun result:

```text
158 modules transformed.
dist/index.html                 0.47 kB
dist/assets/index-tNJY5lD5.css  42.01 kB
dist/assets/index-wrMje9Mu.js   1,467.87 kB
built in 9.05s
```

Warnings: `baseline-browser-mapping` and Browserslist/caniuse data are stale; one chunk is larger than 500 kB after minification. These are not Round 2 blockers.

### Round 2 Post-Documentation Source Scan Rerun

Command:

```powershell
rg -n "firebase/firestore|firebase/|\\.\\./lib/firebase|\\./firebase" frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

Command:

```powershell
rg -n "localStorage\\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken|access_token" frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

Command:

```powershell
rg -n "getFirebaseUserId|X-Tenant-ID|tenant_id|user_id|creator_id" frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

### Round 2 Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

### Round 2 Static And Unit-Test Coverage

- Owner framework list/detail/update/delete code paths are wired to backend REST helpers in the active Round 2 source files.
- API payload tests prove update requests are patch-like and do not send absent `family`, absent `confidence`, missing `_raw`, or empty `_raw`.
- API payload tests prove editor autosave-style payloads do not wipe raw framework data.
- API payload tests prove create/regenerate/generation helpers still send valid payloads and do not include frontend identity fields.
- Static scans prove active Round 2 production files do not import Firebase helpers, reintroduce Bearer/localStorage auth-token behavior, or contain exact frontend identity-field strings.
- Deferred vector-sync/indexing UI does not claim success for Phase 9-deferred behavior.

Current result: code wiring is implemented and covered by focused static scans, API payload unit tests, frontend lint, full frontend tests, and production build. No browser smoke test was run in Round 2, so manual/browser owner-flow behavior is not claimed as proven.

Backend tests were not run because Round 2 did not change backend code.

## Round 2 Route-Gate Review Repair Verification

This repair was run on 2026-06-23. It fixes only the remaining Round 2 review findings and does not implement Rounds 3-6.

### Focused Route Tests

Initial sandboxed command:

```powershell
cd frontend
npm test -- src/components/TenantRoute.test.jsx src/components/Login.test.jsx src/App.route.test.jsx
```

Initial result: failed before tests ran because Vite/Vitest/esbuild could not read config paths in the sandbox:

```text
Cannot read directory "../../../..": Access is denied.
Could not resolve "C:\Users\micha\Desktop\project\framework\frontend\vitest.config.js"
```

Escalated rerun command:

```powershell
cd frontend
npm test -- src/components/TenantRoute.test.jsx src/components/Login.test.jsx src/App.route.test.jsx
```

Escalated rerun result:

```text
src/components/TenantRoute.test.jsx (1 test) passed
src/App.route.test.jsx (1 test) passed
src/components/Login.test.jsx (1 test) passed
3 test files passed
3 tests passed
Duration 2.58s
```

Warning: `baseline-browser-mapping` data is over two months old.

Coverage added:

- authenticated backend-cookie user with `tenantId: null` can access the core framework `TenantRoute` shell.
- successful backend-cookie login with no tenant routes to `/personal/frameworks`.
- app root for an authenticated backend-cookie no-tenant user reaches `/personal/frameworks` and does not render `TenantCreationModal`.

### Route-Gate Modal Path Scan

Command:

```powershell
rg -n 'TenantCreationModal|showTenantModal|handleTenantCreated|createTenant|setDoc' frontend\src\App.jsx frontend\src\components\Login.jsx frontend\src\components\TenantRoute.jsx
```

Result: no matches. `rg` exited `1`.

This confirms the normal post-login route shell does not import, mount, or call the Firebase-backed tenant creation path.

### Round 2 Route/Auth/Core Firebase Import Scan

Final command:

```powershell
rg -n "firebase/auth|firebase/firestore|firebase/|\\.\\./lib/firebase|\\./firebase" frontend\src\App.jsx frontend\src\components\TenantRoute.jsx frontend\src\components\Login.jsx frontend\src\contexts\AuthContext.jsx frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

This confirms the active Round 2 route/auth/core production files do not import Firebase Auth, Firestore, or the local Firebase helper.

### Round 2 Route/Auth/Core Bearer Token Scan

Command:

```powershell
rg -n "localStorage\\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken|access_token" frontend\src\App.jsx frontend\src\components\TenantRoute.jsx frontend\src\components\Login.jsx frontend\src\contexts\AuthContext.jsx frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

### Round 2 Route/Auth/Core Identity Field Scan

Command:

```powershell
rg -n "getFirebaseUserId|X-Tenant-ID|tenant_id|user_id|creator_id" frontend\src\App.jsx frontend\src\components\TenantRoute.jsx frontend\src\components\Login.jsx frontend\src\contexts\AuthContext.jsx frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
```

Result: no matches. `rg` exited `1`.

This confirms exact frontend identity-field strings are absent from active Round 2 production files. Test files may contain these exact strings only as intentional negative assertions.

### Route-Gate Repair Frontend Lint

Command:

```powershell
cd frontend
npm run lint
```

Result: passed with exit code `0`.

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

### Route-Gate Repair Frontend Tests

Command:

```powershell
cd frontend
npm test
```

Result:

```text
src/lib/api.test.js (9 tests) passed
src/components/TenantRoute.test.jsx (1 test) passed
src/App.test.jsx (13 tests) passed
src/App.route.test.jsx (1 test) passed
src/components/Login.test.jsx (1 test) passed
5 test files passed
25 tests passed
Duration 3.65s
```

Warning: `baseline-browser-mapping` data is over two months old.

### Route-Gate Repair Frontend Build

Command:

```powershell
cd frontend
npm run build
```

Result:

```text
156 modules transformed.
dist/index.html                 0.47 kB
dist/assets/index-tNJY5lD5.css  42.01 kB
dist/assets/index-_s8JDKqw.js   1,454.33 kB
built in 12.19s
```

Warnings: `baseline-browser-mapping` and Browserslist/caniuse data are stale; one chunk is larger than 500 kB after minification. These are not Round 2 blockers.

### Route-Gate Repair Git Diff Check

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

### Route-Gate Repair Post-Documentation Rerun

After updating this checklist/report/verification package, the relevant source scans were rerun.

Commands:

```powershell
rg -n "firebase/auth|firebase/firestore|firebase/|\\.\\./lib/firebase|\\./firebase" frontend\src\App.jsx frontend\src\components\TenantRoute.jsx frontend\src\components\Login.jsx frontend\src\contexts\AuthContext.jsx frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
rg -n "localStorage\\.(getItem|setItem).*access_token|Authorization.*Bearer|getAuthToken|access_token" frontend\src\App.jsx frontend\src\components\TenantRoute.jsx frontend\src\components\Login.jsx frontend\src\contexts\AuthContext.jsx frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
rg -n "getFirebaseUserId|X-Tenant-ID|tenant_id|user_id|creator_id" frontend\src\App.jsx frontend\src\components\TenantRoute.jsx frontend\src\components\Login.jsx frontend\src\contexts\AuthContext.jsx frontend\src\lib\api.js frontend\src\components\YourFrameworks.jsx frontend\src\components\FrameworkCard.jsx frontend\src\components\FrameworkEditor.jsx frontend\src\components\CreateFramework.jsx frontend\src\components\AIMergeMode.jsx frontend\src\components\ManualMergeMode.jsx frontend\src\components\UpdateFrameworksButton.jsx
rg -n "TenantCreationModal|showTenantModal|handleTenantCreated|createTenant|setDoc" frontend\src\App.jsx frontend\src\components\Login.jsx frontend\src\components\TenantRoute.jsx
```

Result: all four commands returned no matches. `rg` exited `1` for each command.

Command:

```powershell
git diff --check
```

Result: passed with exit code `0` and no output.

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

No Round 2 browser smoke test was run during this repair pass. The checklist remains unchecked until an actual browser/manual smoke session is performed.

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

## Known Remaining Risks

- Round 2 owner framework flows have code wiring, static scans, API payload unit tests, lint, full frontend tests, and build coverage, but no browser/manual smoke test was run.
- Cookie-session backend readiness has been repaired and verified for Round 1, including strict access-vs-refresh token typing. Temporary backend Bearer compatibility remains a Phase 6 closeout blocker until later rounds remove transitional clients/tests from that path.
- CSRF/cookie-auth unsafe-method protection is currently Origin/Referer based and verified for Round 1; SameSite=None remains clamped to Lax. If SameSite=None is later allowed, stronger protection such as a double-submit token must be added and tested.
- Phase 5 closeout documentation has been corrected to record accepted final review, committed/pushed package, and Phase 6 planning may proceed; Phase 6 should not reopen Phase 5 implementation.
- Some Firebase-importing files are also tenant/invite/migration residue. Phase 6 may remove or isolate them only to uninstall Firebase; broader semantic cleanup remains Phase 7.
- Admin UI may currently expose whitelist-domain concepts that have no Phase 5 backend endpoint. Round 4 should remove or isolate that UI instead of inventing a new backend domain-management feature.
- Artefact UI may still be coupled to legacy `frameworks.artefacts_json`; Round 5 must avoid claiming historical backfill unless a later explicit phase owns it.
