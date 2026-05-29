# Phase 01.1 Verification - Auth Hardening

## Syntax Check

Command:

```powershell
python -m py_compile backend_py/app/auth.py backend_py/app/api/users.py backend_py/app/api/frameworks.py backend_py/app/models.py backend_py/scripts/seed_admin.py
```

Result: passed with exit code `0`.

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

Initial command:

```powershell
python -m pytest -q
```

Initial result:

```text
C:\Users\micha\AppData\Local\Programs\Python\Python312\python.exe: No module named pytest
```

Action taken:

```powershell
python -m pip install -r backend_py/requirements.txt
```

Final command:

```powershell
$env:JWT_SECRET_KEY='phase1-test-secret-at-least-32-chars'; python -m pytest -q
```

Final result:

```text
..................                                                       [100%]
18 passed in 2.76s
```

## Generated Cache Cleanup

Command:

```powershell
Get-ChildItem -Force -Directory -Recurse | Where-Object { $_.Name -in @('__pycache__', '.pytest_cache') } | Select-Object -ExpandProperty FullName
Get-ChildItem -Recurse -Force -Filter '*.pyc' | Select-Object -ExpandProperty FullName
```

Result: no matches after cleanup.

## Git Status Before Commit

Command:

```powershell
git status --short
```

Result:

```text
 M .env.example
 M backend_py/app/api/frameworks.py
 M backend_py/app/api/users.py
 M backend_py/app/models.py
 M backend_py/scripts/seed_admin.py
?? docs/migration/phases/phase-01-1-auth-hardening/
```
