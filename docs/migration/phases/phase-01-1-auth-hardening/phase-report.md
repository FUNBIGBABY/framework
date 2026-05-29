# Phase 01.1 Report - Auth Hardening

## Scope

This small hardening pass closes the review gaps found after Phase 1. It stays within the auth boundary and does not start Phase 2 Provider abstraction, DeepSeekProvider, Postgres, pgvector, Agent, RAG, LLMWiki, or frontend Firebase removal.

## Files Changed

- `.env.example`
- `backend_py/app/api/frameworks.py`
- `backend_py/app/api/users.py`
- `backend_py/app/models.py`
- `backend_py/scripts/seed_admin.py`
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

## Known Deferrals

- httpOnly cookie / refresh token remains deferred.
- Legacy OpenAI Vector Store and old LLM code paths remain deferred to later Provider / DeepSeek phases.
- Full route ownership checks for arbitrary framework payloads are not solved here; this pass only prevents anonymous invocation.

## Handoff

Phase 2 can proceed after this hardening pass. The auth boundary is stricter than Phase 1: high-cost and legacy sync routes now require a JWT before they can run.
