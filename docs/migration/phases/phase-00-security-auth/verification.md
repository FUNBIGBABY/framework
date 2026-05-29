# Phase 00 Verification - Security & Auth Decision

## Firebase Admin SDK JSON

Command:

```powershell
if (Test-Path 'backend_py/framework-builder-55896-firebase-adminsdk-fbsvc-b99f494a12.json') { 'EXISTS' } else { 'MISSING' }
```

Result: `MISSING`.

The private key file was removed from the working tree. This does not revoke the leaked key. A human still needs to ask the customer to Disable and Delete the corresponding service account key in the GCP console.

## JWT Secret

Commands:

```powershell
rg -n 'your-secret-key-change-this' backend_py/app/auth.py
rg -n 'JWT_SECRET_KEY|your-secret-key-change-this' backend_py/app/auth.py
$env:JWT_SECRET_KEY = ''; python -c "import sys; sys.path.insert(0, 'backend_py'); import app.auth"
```

Results:

- Hardcoded placeholder search returned no matches.
- `backend_py/app/auth.py` now reads `JWT_SECRET_KEY`.
- Missing `JWT_SECRET_KEY` raises `RuntimeError: JWT_SECRET_KEY environment variable is required` before backend auth can load.

## LLM API Key Fallbacks

Commands:

```powershell
rg -n 'LOCAL_LLM_API_KEY.*sk-' backend_py/llm_local.py backend_py/test_cloud_llm.py
```

Result: no matches.

Strict redacted secret scan:

```powershell
$pattern = 'sk-[A-Za-z0-9_-]{20,}|-----BEGIN (RSA )?PRIVATE KEY|private_key'
Get-ChildItem -Recurse -File -Force |
  Where-Object { $_.FullName -notmatch '\\docs\\migration\\' -and $_.FullName -notmatch '\\.git\\' -and $_.FullName -notmatch '\\node_modules\\' } |
  Select-String -Pattern $pattern -AllMatches
```

Result after removing source fallbacks and stale compiled caches: `NO_MATCHES`.

## Customer Hardcode Findings

Command:

```powershell
$pattern = 'framework-builder-55896|34\.87\.13\.228|valorie\.ai|webmaster@valorie\.ai|UNSW|ad\.unsw\.edu\.au|OPENAI_VECTOR_STORE|VITE_FIREBASE'
Get-ChildItem -Recurse -File -Force |
  Where-Object { $_.FullName -notmatch '\\docs\\migration\\' -and $_.FullName -notmatch '\\.git\\' -and $_.FullName -notmatch '\\node_modules\\' -and $_.FullName -notmatch '\\__pycache__\\' } |
  Select-String -Pattern $pattern -AllMatches
```

Result: legacy customer-specific matches remain and are intentionally deferred to later Phases.

- `framework-builder-55896`: `firebaseDoc.md`, `backend_py/test_firebase.py`.
- `34.87.13.228`: `docker-compose.yml`, `backend_py/diagnose_env.py`, `backend_py/app/api/frameworks.py`.
- `valorie.ai`: `deploy.sh`, `nginx-valorie.conf`, `backend_py/app/api/frameworks.py`, multiple frontend files under `frontend/src`.
- `webmaster@valorie.ai`: `frontend/src/lib/firebase.js`.
- `ad.unsw.edu.au`: `frontend/src/components/AdminPanel.jsx`, `frontend/src/lib/firebase.js`.
- Exact uppercase `UNSW`: no non-generated source hit in this scan.
- `VITE_FIREBASE`: `docker-compose.yml`, `Dockerfile`, `Project-Startup-and-Operation-Flow.md`, `backend_py/main.py`, `backend_py/app/api/frameworks.py`, backend test scripts, `frontend/src/lib/firebase.js`.
- `OPENAI_VECTOR_STORE`: `docker-compose.yml`, `backend_py/main.py`, `backend_py/README-DIFF.md`, backend test scripts, `backend_py/app/api/frameworks.py`.

## Gitignore

Command:

```powershell
rg -n '^\.env\*|^!\.env\.example|firebase-adminsdk|\*\.pem|\*\.key|__pycache__|\*\.py\[cod\]' .gitignore
```

Result:

- `.env*`
- `!.env.example`
- `*-firebase-adminsdk*.json`
- `*.pem`
- `*.key`
- `__pycache__/`
- `*.py[cod]`

## Env Example

Commands:

```powershell
Get-Content -Raw '.env.example'
Select-String -Path '.env.example' -Pattern 'sk-[A-Za-z0-9_-]{20,}|-----BEGIN|private_key|AIza[0-9A-Za-z_-]{20,}'
```

Result:

- `.env.example` exists.
- Required Phase 0 env names are present.
- Legacy `LLM_TYPE` / `LOCAL_LLM_*` placeholders are present with empty secret values until Phase 3 replaces that path.
- Secret-like scan returned `NO_MATCHES`.

## Syntax Check

Command:

```powershell
python -m py_compile backend_py/app/auth.py backend_py/llm_local.py backend_py/test_cloud_llm.py backend_py/test_vec_base.py
```

Result: passed with exit code `0`.

Generated `.pyc` artifacts from this syntax check were removed afterwards. The strict redacted secret scan was rerun and returned `NO_MATCHES`.

## Git History

Command:

```powershell
if (Test-Path '.git') { 'GIT_PRESENT' } else { 'NO_GIT_DIRECTORY' }
```

Result: `NO_GIT_DIRECTORY`.

This working directory currently has no `.git` metadata, so Phase 0 could not inspect or rewrite commit history here. If this tree was ever pushed to a remote, the remote history still needs separate cleanup. If this is a new fork or new repo, initialize from this cleaned working tree.

## Post-Verification Fixes

Main directory decision:

```powershell
C:\Users\micha\Desktop\Valorie.ai\valorie-expert-studio-main
```

Planning documents migrated into the main project root:

```powershell
Test-Path 'PROJECT_AUDIT_AND_MIGRATION_PLAN.md'
Test-Path 'MIGRATION_PHASES.md'
```

Result: both files exist in the main project root.

Additional redaction performed:

- `firebaseDoc.md`: replaced legacy Firebase config values with placeholders.
- `backend_py/test_firebase.py`: replaced the example command containing a real-looking Firebase Web API key, email, and password with placeholders.

Cache cleanup performed:

```powershell
Get-ChildItem -Directory -Recurse -Force -Filter '__pycache__'
Remove-Item -LiteralPath <verified-workspace-path> -Recurse -Force
```

Result: all `__pycache__` directories under the main project were removed after verifying their resolved paths were inside the workspace.

Final secret scan command:

```powershell
rg -n --hidden -S 'AIza[0-9A-Za-z_-]{20,}|huangboyuan|hby199|sk-[A-Za-z0-9_-]{20,}|-----BEGIN|private_key' . -g '!node_modules' -g '!frontend/node_modules' -g '!docs/migration/**' -g '!project-tree.txt' -g '!**/__pycache__/**'
```

Result: `NO_MATCHES`.

## Phase 0.1 Legacy Cloud LLM Guardrail

Commands:

```powershell
rg -n '34\.87\.13\.228|LOCAL_LLM|LLM_TYPE|OPENAI_API_KEY|OPENAI_VECTOR_STORE' docker-compose.yml docker-entrypoint.sh .env.example
```

Result: no legacy Cloud LLM / OpenAI Vector Store deployment env remains in `docker-compose.yml` or `docker-entrypoint.sh`; `.env.example` keeps only `ENABLE_LEGACY_LLM=false` as an explicit guardrail.

Command:

```powershell
python -c "import sys; sys.path.insert(0, 'backend_py'); from llm_local import LLMClient; LLMClient()"
```

Result:

```text
RuntimeError: Legacy llm_local/Ollama/GCP LLM path is disabled. Use the DeepSeek provider after Phase 3 migration.
```

This confirms the old `llm_local` path cannot run accidentally before Phase 3 replaces it with `LLMProvider`.
