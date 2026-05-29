# Phase 00 Report - Security & Auth Decision

## Scope

This Phase only handles P0 security and the Auth strategy decision. It does not enter Phase 1.

No password hash migration, refresh token flow, JWT cookie migration, frontend `user_id` permission rewrite, DeepSeekProvider, Postgres, pgvector, Agent, RAG, or LLMWiki implementation was started.

## Files Changed

- `.gitignore`
- `.env.example`
- `backend_py/app/auth.py`
- `backend_py/llm_local.py`
- `backend_py/test_cloud_llm.py`
- `backend_py/test_vec_base.py`
- `backend_py/test_firebase.py`
- `firebaseDoc.md`
- `PROJECT_AUDIT_AND_MIGRATION_PLAN.md`
- `MIGRATION_PHASES.md`
- `docs/PERSONAL_USE_BOUNDARY.md`
- `docs/migration/README.md`
- `docs/migration/decisions/ADR-0001-auth-strategy.md`
- `docs/migration/phases/phase-00-security-auth/checklist.md`
- `docs/migration/phases/phase-00-security-auth/verification.md`
- `docs/migration/phases/phase-00-security-auth/phase-report.md`

Deleted:

- `backend_py/framework-builder-55896-firebase-adminsdk-fbsvc-b99f494a12.json`
- `backend_py/__pycache__/llm_local.cpython-312.pyc`
- `backend_py/__pycache__/test_cloud_llm.cpython-312.pyc`
- `backend_py/__pycache__/test_vec_base.cpython-312.pyc`
- `backend_py/app/__pycache__/auth.cpython-312.pyc`

## Secrets Removed

- Removed the Firebase/GCP service account JSON private key file from the working tree.
- Removed the hardcoded JWT signing secret fallback from `backend_py/app/auth.py`.
- Removed the hardcoded cloud LLM API key fallback from `backend_py/llm_local.py`.
- Removed the same cloud LLM API key fallback from `backend_py/test_cloud_llm.py`.
- Removed a command comment containing a real-looking API key from `backend_py/test_vec_base.py`.
- Redacted the legacy Firebase Web API key and example test account/password from `firebaseDoc.md` and `backend_py/test_firebase.py`.
- Removed stale compiled `.pyc` / `__pycache__` artifacts after verification.

No private key or API key values are reproduced in this report.

## Env Added

- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `LLM_PROVIDER`
- `DEEPSEEK_BASE_URL`
- `DEEPSEEK_API_KEY`
- `DEEPSEEK_MODEL_DEFAULT`
- `DEEPSEEK_MODEL_REASONING`
- `DEEPSEEK_THINKING_MODE`
- `LLM_TYPE`
- `LOCAL_LLM_URL`
- `LOCAL_LLM_MODEL`
- `LOCAL_LLM_API_KEY`
- `EMBEDDING_PROVIDER`
- `EMBEDDING_MODEL`
- `EMBEDDING_DIM`
- `OBJECT_STORE_PROVIDER`
- `APP_BASE_DOMAIN`
- `APP_NAME`
- `SUPER_ADMIN_EMAIL`
- `ALLOWED_EMAILS`
- `ENABLE_PUBLIC_REGISTER`

## Customer Legacy Findings

The following customer-specific hardcodes still exist and are deferred to later Phases. These are not fully refactored in Phase 0.

- `framework-builder-55896`: `firebaseDoc.md`, `backend_py/test_firebase.py`.
- `34.87.13.228`: `docker-compose.yml`, `backend_py/diagnose_env.py`, `backend_py/app/api/frameworks.py`.
- `valorie.ai`: `deploy.sh`, `nginx-valorie.conf`, `backend_py/app/api/frameworks.py`, multiple frontend files under `frontend/src`.
- `webmaster@valorie.ai`: `frontend/src/lib/firebase.js`.
- `ad.unsw.edu.au`: `frontend/src/components/AdminPanel.jsx`, `frontend/src/lib/firebase.js`.
- `UNSW`: no exact uppercase source hit in the Phase 0 scan; the UNSW domain hits above remain.
- `VITE_FIREBASE`: `docker-compose.yml`, `Dockerfile`, `Project-Startup-and-Operation-Flow.md`, `backend_py/main.py`, `backend_py/app/api/frameworks.py`, backend test scripts, `frontend/src/lib/firebase.js`.
- `OPENAI_VECTOR_STORE`: `docker-compose.yml`, `backend_py/main.py`, `backend_py/README-DIFF.md`, backend test scripts, `backend_py/app/api/frameworks.py`.

Recommended later ownership:

- Phase 3: remove legacy GCP LLM endpoint assumptions while switching to DeepSeek.
- Phase 5-7: remove Firebase, Firestore, customer domain, deploy, and frontend legacy paths.
- Phase 4/9: replace OpenAI Vector Store with Postgres + pgvector as the core path.

## Decisions

- Auth strategy is locked to option A: self-hosted backend JWT, allowlist, and no public registration.
- Firebase Auth and Firebase ID Token are not part of the new project route.
- OpenAI Vector Store is not a core path and should later be replaced by pgvector.
- DeepSeek V4 is the default LLM direction, but Phase 0 does not implement `DeepSeekProvider`.
- The project boundary is personal use only unless a later compliance review changes that.

## Manual Actions Required

- A human must notify the customer to Disable and Delete the exposed service account key in the GCP console. Deleting the JSON from this repository does not revoke the key.
- Decide whether git history must be rebuilt. If this is a new fork or new repository, initialize from the cleaned working tree. If any previous repository or remote already contains the leaked file, deleting it now is not enough.
- If the file was pushed to any remote, clean git history separately before using or sharing that remote.
- Current working directory check returned `NO_GIT_DIRECTORY`, so Phase 0 could not inspect or rewrite local commit history here.

## Post-Verification Fixes

- Main working directory is now `C:\Users\micha\Desktop\Valorie.ai\valorie-expert-studio-main`.
- The two master planning documents were migrated from `C:\Users\micha\Desktop\newvalorie\valorie-expert-studio-main` into the main project root:
  - `PROJECT_AUDIT_AND_MIGRATION_PLAN.md`
  - `MIGRATION_PHASES.md`
- `firebaseDoc.md` now uses placeholder Firebase config values instead of the legacy customer Web API key/project values.
- `backend_py/test_firebase.py` now uses placeholder CLI example values instead of a real-looking API key/email/password.
- All `__pycache__` directories under the main project were removed.
- The same Firebase/GCP service account JSON private key file was also removed from the deprecated `C:\Users\micha\Desktop\newvalorie\valorie-expert-studio-main` tree to reduce accidental reuse risk.

## Verification Summary

- Firebase admin SDK JSON file check: `MISSING`.
- Hardcoded JWT placeholder search: no matches.
- Missing `JWT_SECRET_KEY` import check: raises `RuntimeError`.
- `LOCAL_LLM_API_KEY` fallback search in `llm_local.py` and `test_cloud_llm.py`: no matches.
- Strict redacted secret scan for long `sk-` values, Firebase Web API keys, private key blocks, `private_key`, and the prior test credential strings: `NO_MATCHES`.
- Planning document presence check in the main project root: passed.
- `__pycache__` / `.pyc` scan after cleanup: no matches.
- `.gitignore` contains `.env*`, `!.env.example`, `*-firebase-adminsdk*.json`, `*.pem`, `*.key`, `__pycache__/`, and `*.py[cod]`.
- `.env.example` exists and contains placeholders only.
- Python syntax check passed for changed backend files.
- Customer legacy hardcodes remain and are listed above for later Phases.

## Handoff To Phase 1

Phase 1 can begin:

- Argon2id password hashing.
- JWT as the single identity trust source.
- Blocking frontend-provided `user_id`.
- Allowlist registration.
- Refresh token and cookie strategy.
