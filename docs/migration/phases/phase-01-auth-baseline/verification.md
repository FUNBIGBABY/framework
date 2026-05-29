# Phase 01 Verification - Auth Baseline

## Syntax Check

Command:

```powershell
python -m py_compile backend_py/app/auth.py backend_py/app/api/users.py backend_py/app/api/frameworks.py
```

Result: passed with exit code `0`.

## Frontend user_id Trust Boundary

Command:

```powershell
rg -n "user_id\s*:\s*str\s*=\s*(Body|Query|Form|Path)\(" backend_py/app
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

Command:

```powershell
rg -n "request\.user_id" backend_py/app
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

## Password Hashing

Command:

```powershell
rg -n "your-secret-key|sha256\(" backend_py/app/auth.py
```

Result:

```text
91:    """Verify the old salt$sha256(salt + password) format."""
96:        pwd_hash = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
```

Interpretation: no hardcoded JWT placeholder remains. The only `sha256(` hit is the intentional legacy compatibility verifier.

Command:

```powershell
rg -n "argon2|PasswordHasher" backend_py/app/auth.py backend_py/requirements.txt
```

Result:

```text
backend_py/requirements.txt:14:argon2-cffi>=23.1.0
backend_py/app/auth.py:15:from argon2 import PasswordHasher
backend_py/app/auth.py:16:from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
backend_py/app/auth.py:17:from argon2.low_level import Type
backend_py/app/auth.py:41:password_hasher = PasswordHasher(type=Type.ID)
backend_py/app/auth.py:42:ARGON2ID_PREFIX = "$argon2id$"
```

Runtime smoke command:

```powershell
$env:JWT_SECRET_KEY='phase1-test-secret-at-least-32-chars'; python -c "import hashlib, secrets, sys; sys.path.insert(0, 'backend_py'); from app.auth import hash_password, verify_password_with_rehash; h=hash_password('secret-pass'); salt=secrets.token_hex(16); legacy=salt+'$'+hashlib.sha256((salt+'secret-pass').encode()).hexdigest(); print('ARGON2_PREFIX=' + str(h.startswith('$argon2id$'))); print('ARGON2_VALID=' + str(verify_password_with_rehash('secret-pass', h))); print('ARGON2_INVALID=' + str(verify_password_with_rehash('wrong', h))); print('LEGACY_VALID=' + str(verify_password_with_rehash('secret-pass', legacy)))"
```

Result:

```text
ARGON2_PREFIX=True
ARGON2_VALID=(True, False)
ARGON2_INVALID=(False, False)
LEGACY_VALID=(True, True)
```

Note: `argon2-cffi` and existing project dependency `python-jose[cryptography]` were installed into the local Python environment to run this runtime smoke test. They are both now represented by `backend_py/requirements.txt` or pre-existing requirements.

## Registration and Admin Seed

Command:

```powershell
rg -n "ENABLE_PUBLIC_REGISTER|ALLOWED_EMAILS|SUPER_ADMIN_PASSWORD|SUPER_ADMIN_EMAIL" .env.example backend_py/app/api/users.py backend_py/scripts/seed_admin.py
```

Result:

```text
backend_py/scripts/seed_admin.py:5:- SUPER_ADMIN_EMAIL
backend_py/scripts/seed_admin.py:6:- SUPER_ADMIN_PASSWORD
backend_py/scripts/seed_admin.py:10:the configured SUPER_ADMIN_EMAIL is the admin identity boundary.
backend_py/scripts/seed_admin.py:41:    email = _required_env("SUPER_ADMIN_EMAIL").lower()
backend_py/scripts/seed_admin.py:42:    password = _required_env("SUPER_ADMIN_PASSWORD")
.env.example:23:SUPER_ADMIN_EMAIL=
.env.example:24:SUPER_ADMIN_PASSWORD=
.env.example:25:ALLOWED_EMAILS=
.env.example:26:ENABLE_PUBLIC_REGISTER=false
backend_py/app/api/users.py:81:    return os.getenv("ENABLE_PUBLIC_REGISTER", "false").strip().lower() == "true"
backend_py/app/api/users.py:85:    raw = os.getenv("ALLOWED_EMAILS", "")
```

Registration policy result:

- `ENABLE_PUBLIC_REGISTER` defaults to `false`.
- `ALLOWED_EMAILS` is required even when public registration is explicitly enabled.
- First-user self-registration was not implemented.
- Admin creation is script-only.

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

The old deploy env guardrail remains intact. `ENABLE_LEGACY_LLM=false` is still present in `.env.example`, but it is not matched by the legacy deploy env grep pattern above.

## Generated Cache Cleanup

Command:

```powershell
Get-ChildItem -Directory -Recurse -Force -Filter '__pycache__' | Select-Object -ExpandProperty FullName
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
 M backend_py/app/auth.py
 M backend_py/requirements.txt
?? backend_py/scripts/
?? docs/migration/phases/phase-01-auth-baseline/
```
