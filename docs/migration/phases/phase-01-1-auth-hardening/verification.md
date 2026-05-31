# Phase 01.1 Verification - Auth Hardening

## Syntax Check

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m py_compile main.py app\api\materials.py app\api\users.py app\auth.py
```

Result: passed with exit code `0`.

## Dotenv Load Order Check

Command:

```powershell
rg -n "load_dotenv|BASE_DIR|from app\.api|JWT_SECRET_KEY" backend_py\main.py backend_py\app\auth.py
```

Result:

```text
backend_py\main.py:6:from dotenv import load_dotenv
backend_py\main.py:9:# JWT_SECRET_KEY at import time.
backend_py\main.py:10:BASE_DIR = Path(__file__).resolve().parent
backend_py\main.py:11:load_dotenv(BASE_DIR.parent / ".env")
backend_py\main.py:12:load_dotenv(BASE_DIR / ".env")
backend_py\main.py:20:from app.api.materials import router as materials_router
backend_py\main.py:21:from app.api.frameworks import router as frameworks_router
backend_py\main.py:22:from app.api.users import router as users_router
backend_py\main.py:23:from app.api.frameworks import sync_library, SyncLibraryRequest
backend_py\app\auth.py:30:SECRET_KEY = os.getenv("JWT_SECRET_KEY")
```

Interpretation: dotenv is loaded before `main.py` imports routers that can import `app.auth`.

## Materials JWT Check

Command:

```powershell
rg -n "get_current_user_id|upload_file|get_material|ingest_text|/ping" backend_py\app\api\materials.py
```

Result:

```text
10:from ..auth import get_current_user_id
27:@router.get("/ping")
59:async def upload_file(
61:    _current_user_id: str = Depends(get_current_user_id),
108:def get_material(
110:    _current_user_id: str = Depends(get_current_user_id),
128:def ingest_text(
130:    _current_user_id: str = Depends(get_current_user_id),
```

Interpretation: non-ping materials endpoints require JWT; `/materials/ping` remains public.

## Stale Auth Docstring Scan

Command:

```powershell
rg -n -i "no auth|no authentication|required authentication|temporary version|test results directly|Add this code" backend_py/app/api/frameworks.py
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

## High-Cost / Write Endpoint JWT Check

Command:

```powershell
rg -n "^(async def export_markdown_from_data|async def export_docx_from_data|async def regenerate_framework|async def ai_merge_frameworks|async def ai_fill_sections|def sync_library|def push_framework)" backend_py/app/api/frameworks.py
```

Result:

```text
1963:async def export_markdown_from_data(
2010:async def export_docx_from_data(
2057:async def regenerate_framework(
2291:async def ai_merge_frameworks(
2516:async def ai_fill_sections(
2671:def sync_library(
2823:def push_framework(
```

Command:

```powershell
rg -n "current_user_id: str = Depends\(get_current_user_id\)" backend_py/app/api/frameworks.py
```

Result:

```text
1964:    framework_data: dict, current_user_id: str = Depends(get_current_user_id)
2011:    framework_data: dict, current_user_id: str = Depends(get_current_user_id)
2058:    request: RegenerateRequest, current_user_id: str = Depends(get_current_user_id)
2292:    request: AIMergeRequest, current_user_id: str = Depends(get_current_user_id)
2517:    request: AIFillRequest, current_user_id: str = Depends(get_current_user_id)
2673:    current_user_id: str = Depends(get_current_user_id),
2824:    req: PushFrameworkRequest, current_user_id: str = Depends(get_current_user_id)
```

## Account Enumeration Endpoint JWT Check

Command:

```powershell
rg -n "check_email_availability|check_username_availability|current_user: User = Depends\(get_current_user\)" backend_py/app/api/users.py
```

Result:

```text
228:def get_current_user_info(current_user: User = Depends(get_current_user)):
241:def check_email_availability(
243:    current_user: User = Depends(get_current_user),
260:def check_username_availability(
262:    current_user: User = Depends(get_current_user),
```

## Frontend user_id Trust Boundary

Command:

```powershell
rg -n "user_id\s*:\s*str\s*=\s*(Body|Query|Form|Path)\(|request\.user_id" backend_py/app
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

## Seed Admin Behavior

Command:

```powershell
rg -n "bcrypt|SEED_ADMIN_RESET_PASSWORD|Admin user already exists" backend_py/app/models.py backend_py/scripts/seed_admin.py .env.example
```

Result:

```text
backend_py/scripts/seed_admin.py:8:- SEED_ADMIN_RESET_PASSWORD=true to reset an existing admin password
backend_py/scripts/seed_admin.py:63:                    print(f"Admin user already exists and password verified: {email}")
backend_py/scripts/seed_admin.py:66:            if not _env_enabled("SEED_ADMIN_RESET_PASSWORD"):
backend_py/scripts/seed_admin.py:68:                    "Admin user already exists but SUPER_ADMIN_PASSWORD does not match. "
backend_py/scripts/seed_admin.py:69:                    "Set SEED_ADMIN_RESET_PASSWORD=true to reset it."
.env.example:25:SEED_ADMIN_RESET_PASSWORD=false
```

Interpretation: no `bcrypt` match remains in the checked files. `SEED_ADMIN_RESET_PASSWORD=false` is documented in `.env.example`.

## Secret Scan

Command:

```powershell
rg -n --hidden -S "AIza[0-9A-Za-z_-]{20,}|huangboyuan|hby199|sk-[A-Za-z0-9_-]{20,}|-----BEGIN|private_key" . -g "!node_modules" -g "!frontend/node_modules" -g "!docs/migration/**" -g "!project-tree.txt" -g "!**/__pycache__/**"
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

## Legacy Cloud LLM Guardrail

Command:

```powershell
rg -n "34\.87\.13\.228|LOCAL_LLM|LLM_TYPE|OPENAI_API_KEY|OPENAI_VECTOR_STORE" docker-compose.yml docker-entrypoint.sh .env.example
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

## Pytest

Targeted auth hardening test command:

```powershell
cd backend_py
python -m pytest tests/test_auth_hardening.py -q
```

Result:

```text
tests\test_auth_hardening.py .............                               [100%]
13 passed, 3 warnings in 3.99s
```

Full backend test command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
55 passed, 3 warnings in 5.15s
```

Warnings are existing Pydantic v2 deprecation warnings in `backend_py/app/api/users.py`; they are unrelated to this auth hardening patch.

## Frontend Compatibility Debt Check

Command:

```powershell
rg -n "user_id|currentUser|Firebase|firebase" frontend/src/lib/api.js
```

Result:

```text
4:import { auth } from './firebase'
84: * Get Firebase User ID
86:function getFirebaseUserId() {
87:  const user = auth.currentUser
168:  const userId = getFirebaseUserId()
174:  if (userId) payload.user_id = userId
207:  const userId = getFirebaseUserId()
209:  if (userId) formData.append('user_id', userId)
252:  const userId = getFirebaseUserId()
254:  if (userId) formData.append('user_id', userId)
289:  const userId = getFirebaseUserId()
293:  if (userId) params.set('user_id', userId)
306:  const userId = getFirebaseUserId()
310:  if (userId) params.set('user_id', userId)
```

Interpretation: frontend Firebase `user_id` compatibility code still exists and is deferred to Phase 6, but the list APIs only append `user_id` when a Firebase user exists. Backend-JWT-only sessions are no longer blocked by an empty `auth.currentUser`.

## Frontend Backend-JWT Login Bridge

Command:

```powershell
rg -n "loginWithBackend|access_token|backend-jwt|firebase-compat|Firebase login compatibility" frontend\src\contexts\AuthContext.jsx frontend\src\components\Login.jsx frontend\src\lib\api.js
```

Result:

```text
frontend\src\lib\api.js:56:  return localStorage.getItem('access_token')
frontend\src\lib\api.js:107:        localStorage.removeItem('access_token')
frontend\src\lib\api.js:133:export async function loginWithBackend(email, password) {
frontend\src\contexts\AuthContext.jsx:16:import { loginWithBackend } from '../lib/api'
frontend\src\contexts\AuthContext.jsx:33:    authProvider: 'backend-jwt',
frontend\src\contexts\AuthContext.jsx:38:  const token = localStorage.getItem('access_token')
frontend\src\contexts\AuthContext.jsx:54:  localStorage.setItem('access_token', authData.access_token)
frontend\src\contexts\AuthContext.jsx:61:  localStorage.removeItem('access_token')
frontend\src\contexts\AuthContext.jsx:82:    authProvider: 'backend-jwt+firebase-compat',
frontend\src\contexts\AuthContext.jsx:175:      const backendAuth = await loginWithBackend(email, password)
frontend\src\contexts\AuthContext.jsx:227:          'Firebase login compatibility skipped; backend JWT login succeeded.',
```

Interpretation: frontend login now gets the backend JWT first. Firebase is retained only for Phase 6 compatibility metadata.

## Frontend Tests

Command:

```powershell
cd frontend
npm test -- --configLoader runner
```

Result:

```text
Test Files  1 passed (1)
Tests  13 passed (13)
```

Note: Vitest printed the existing stale `baseline-browser-mapping` warning.

## Frontend Build

Command:

```powershell
cd frontend
npm run build -- --configLoader runner
```

Result: build passed. Vite printed existing stale browser-data warnings and a chunk-size warning.

## Latest Review Fix Verification - 2026-05-31

Backend targeted test command requested by the reviewer:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_deepseek_provider.py tests\test_provider_abstractions.py -q
```

Result:

```text
37 passed, 3 warnings in 4.26s
```

Warnings are the existing Pydantic v2 deprecation warnings in `backend_py/app/api/users.py`.

Frontend test command:

```powershell
cd frontend
npm test -- --configLoader runner
```

Result:

```text
Test Files  1 passed (1)
Tests       13 passed (13)
```

Note: Vitest printed the existing stale `baseline-browser-mapping` warning.

Frontend build command:

```powershell
cd frontend
npm run build -- --configLoader runner
```

Result: build passed in 12.90s. Vite printed the existing stale `baseline-browser-mapping`, stale `caniuse-lite`, and chunk-size warnings.

Token storage compatibility scan:

```powershell
rg -n 'localStorage\.getItem\([''"]token[''"]\)|localStorage\.setItem\([''"]token[''"]\)' frontend/src
```

Result: no matches. `rg` exited `1`, which means no code still reads or writes `localStorage.token`.

Protected frontend framework API scan:

```powershell
rg -n "fetch\(|API_ENDPOINTS\.|/api/frameworks" frontend/src
```

Result: protected framework calls are routed through `apiRequest()` or `apiFetch()`. Direct component calls to `EXPORT_DOCX`, `REGENERATE`, `AI_MERGE`, `AI_FILL`, and `PUSH_FRAMEWORK` now use `apiFetch(API_ENDPOINTS.*)`. Remaining raw `fetch()` calls are the `apiFetch()` implementation itself, backend login, and the public health check.

Signup exposure scan:

```powershell
rg -n 'navigate\(''/signup''\)|to="/signup"|path="/signup"|createUserWithEmailAndPassword' frontend/src
```

Result: no matches. `rg` exited `1`, which means there is no active signup route/link/navigation and no Firebase public signup creation call.

Backend-JWT-only framework list compatibility scan:

```powershell
rg -n "user_id|currentUser|Firebase|firebase" frontend/src/lib/api.js
```

Result:

```text
4:import { auth } from './firebase'
84: * Get Firebase User ID
86:function getFirebaseUserId() {
87:  const user = auth.currentUser
168:  const userId = getFirebaseUserId()
174:  if (userId) payload.user_id = userId
207:  const userId = getFirebaseUserId()
209:  if (userId) formData.append('user_id', userId)
252:  const userId = getFirebaseUserId()
254:  if (userId) formData.append('user_id', userId)
289:  const userId = getFirebaseUserId()
293:  if (userId) params.set('user_id', userId)
306:  const userId = getFirebaseUserId()
310:  if (userId) params.set('user_id', userId)
```

Interpretation: Firebase `user_id` remains as optional compatibility plumbing only. `getMyFrameworks()` and `getMyFrameworksByFamily()` no longer return early when `auth.currentUser` is absent.

Backend trust-boundary scan:

```powershell
rg -n "user_id\s*:\s*str\s*=\s*(Body|Query|Form|Path)\(|request\.user_id" backend_py/app
```

Result: no matches. `rg` exited `1`.

OpenAI/direct legacy LLM scan:

```powershell
rg -n "from openai import OpenAI|openai\.OpenAI\(|client\.chat|call_openai_framework|llm_global|resolve_api_settings|gpt-4o" backend_py/app/api frontend/src
```

Result: no matches. `rg` exited `1`.

README legacy-entry scan:

```powershell
rg -n "PROJECT_AUDIT_AND_MIGRATION_PLAN.md|Project-Startup-and-Operation-Flow.md" docs MIGRATION_PHASES.md README.md
```

Result: matches remain only in the canonical migration plan, historical Phase 0 records, reviewer skill scan instructions, and this verification record. Root `README.md` no longer points to either legacy document.

## Generated Cache Cleanup

Command:

```powershell
$root=(Resolve-Path .).Path; $targets=@('backend_py\htmlcov','backend_py\.coverage','backend_py\.pytest_cache'); foreach ($rel in $targets) { $path=Join-Path $root $rel; if (Test-Path -LiteralPath $path) { $resolved=(Resolve-Path -LiteralPath $path).Path; if (-not $resolved.StartsWith($root)) { throw "Refusing to delete outside workspace: $resolved" }; Remove-Item -LiteralPath $resolved -Recurse -Force } }
```

Result: removed generated coverage and pytest-cache outputs created by the targeted backend test run. Python `__pycache__` folders under the local virtual environments and ignored app/test import caches may still exist; they are not tracked phase outputs.

## Git Status Before Commit

Command:

```powershell
git status --short
```

Result:

```text
 M MIGRATION_PHASES.md
 D PROJECT_AUDIT_AND_MIGRATION_PLAN.md
 M README.md
 M backend_py/.env.example
 M backend_py/app/api/frameworks_shared.py
 M backend_py/app/api/generation.py
 M backend_py/app/api/materials.py
 M backend_py/diagnose_env.py
 M backend_py/main.py
 M backend_py/tests/test_auth_hardening.py
 M backend_py/tests/test_provider_abstractions.py
 M docker-compose.yml
 M docs/migration/README.md
 M docs/migration/phases/phase-01-1-auth-hardening/checklist.md
 M docs/migration/phases/phase-01-1-auth-hardening/phase-report.md
 M docs/migration/phases/phase-01-1-auth-hardening/verification.md
 M docs/migration/phases/phase-01-auth-baseline/checklist.md
 M docs/migration/phases/phase-01-auth-baseline/phase-report.md
 M docs/migration/phases/phase-02-provider-abstraction/checklist.md
 M docs/migration/phases/phase-02-provider-abstraction/phase-report.md
 M docs/migration/phases/phase-02-provider-abstraction/verification.md
 M frontend/src/App.jsx
 M frontend/src/components/AIMergeMode.jsx
 M frontend/src/components/ArtefactEditor.jsx
 M frontend/src/components/CreateFramework.jsx
 M frontend/src/components/FrameworkCard.jsx
 M frontend/src/components/FrameworkEditor.jsx
 M frontend/src/components/LandingPage.jsx
 M frontend/src/components/Login.jsx
 M frontend/src/components/Navbar.jsx
 M frontend/src/components/PublishModal.jsx
 M frontend/src/components/Signup.jsx
 M frontend/src/contexts/AuthContext.jsx
 M frontend/src/lib/api.js
 M frontend/src/lib/firebase.js
?? docs/CN_DEPLOY.md
?? docs/migration/phases/phase-03-deepseek-v4/
?? docs/skills/
```

Interpretation: the worktree includes prior Phase 1-3 migration changes plus the latest review-fix edits. No generated coverage directory, `.coverage`, or `.pytest_cache` file is present in `git status`.
