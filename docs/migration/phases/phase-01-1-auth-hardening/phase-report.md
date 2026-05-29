# Phase 01.1 Report - Auth Hardening

## Scope

This small hardening pass closes the review gaps found after Phase 1. It stays within the auth boundary and does not start Phase 2 Provider abstraction, DeepSeekProvider, Postgres, pgvector, Agent, RAG, LLMWiki, or frontend Firebase removal.

## Files Changed

- `.env.example`
- `backend_py/app/api/frameworks.py`
- `backend_py/app/api/users.py`
- `backend_py/app/models.py`
- `backend_py/scripts/seed_admin.py`
- `backend_py/tests/test_auth_hardening.py`
- `docs/migration/phases/phase-01-1-auth-hardening/checklist.md`
- `docs/migration/phases/phase-01-1-auth-hardening/phase-report.md`
- `docs/migration/phases/phase-01-1-auth-hardening/verification.md`

## Auth Hardening Changes

- Added `Depends(get_current_user_id)` to these high-cost or write-like framework endpoints:
  - `POST /api/frameworks/export-markdown`
  - `POST /api/frameworks/export-docx`
  - `POST /api/frameworks/regenerate`
  - `POST /api/frameworks/ai-merge`
  - `POST /api/frameworks/ai-fill`
  - `POST /api/frameworks/sync-library`
  - `POST /api/frameworks/push-framework`
- Added `Depends(get_current_user)` to:
  - `GET /api/users/check-email/{email}`
  - `GET /api/users/check-username/{username}`
- These availability endpoints no longer allow anonymous account enumeration.

## Admin Seed Behavior

`backend_py/scripts/seed_admin.py` now handles an existing admin email as follows:

- If `SUPER_ADMIN_PASSWORD` matches and the stored hash needs rehashing, it upgrades the hash.
- If `SUPER_ADMIN_PASSWORD` matches and no rehash is needed, it exits successfully.
- If `SUPER_ADMIN_PASSWORD` does not match, it fails fast by default.
- If `SEED_ADMIN_RESET_PASSWORD=true`, it resets the existing admin password to `SUPER_ADMIN_PASSWORD`.

## Documentation Cleanup

- `backend_py/app/models.py` now describes `password_hash` as an Argon2id password hash instead of bcrypt.
- `backend_py/app/api/frameworks.py` no longer describes `ai_merge_frameworks` as unauthenticated. The docstring now states that a valid JWT is required before merge logic can run.
- Removed an obsolete local implementation note near the AI fill endpoint.

## Tests Added

- Added `backend_py/tests/test_auth_hardening.py`.
- The test builds a minimal FastAPI app with the existing `frameworks` and `users` routers and calls protected endpoints without an `Authorization` header.
- It verifies the following routes return `401` or `403` before business logic can run:
  - `POST /api/frameworks/export-markdown`
  - `POST /api/frameworks/export-docx`
  - `POST /api/frameworks/regenerate`
  - `POST /api/frameworks/ai-merge`
  - `POST /api/frameworks/ai-fill`
  - `POST /api/frameworks/sync-library`
  - `POST /api/frameworks/push-framework`
  - `GET /api/users/check-email/{email}`
  - `GET /api/users/check-username/{username}`

## Frontend Compatibility Debt

- `frontend/src/lib/api.js` still contains legacy Firebase-era code that reads `auth.currentUser.uid` and sends `user_id` to backend endpoints.
- This pass intentionally does not rewrite frontend Firebase auth or API calls.
- The backend now ignores or rejects frontend-provided `user_id` and uses JWT dependencies instead.
- Phase 6 must remove the frontend Firebase `user_id` plumbing and switch those calls fully to the backend JWT/auth flow.

## Known Deferrals

- httpOnly cookie / refresh token remains deferred.
- Legacy OpenAI Vector Store and old LLM code paths remain deferred to later Provider / DeepSeek phases.
- Full route ownership checks for arbitrary framework payloads are not solved here; this pass only prevents anonymous invocation.
- Frontend Firebase Auth removal and stale frontend `user_id` request parameters remain deferred to Phase 6.

## Handoff

Phase 2 can proceed after this hardening pass. The auth boundary is stricter than Phase 1: high-cost and legacy sync routes now require a JWT before they can run.
