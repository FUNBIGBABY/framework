# Phase 01 Report - Auth Baseline

## Scope

This Phase only implements the authentication and permission baseline:

- Argon2id password hashing.
- Legacy SHA-256+salt password verification compatibility.
- Login-time password hash rehashing.
- JWT as the single trusted source for backend `user_id`.
- Public registration disabled by default.
- Email allowlist enforcement for the registration endpoint.
- Administrator seeding through a script.

This Phase does not implement DeepSeekProvider, Postgres, pgvector, Agent, RAG, LLMWiki, large frontend Firebase removal, or broad frontend rewrites.

## Files Changed

- `.env.example`
- `backend_py/requirements.txt`
- `backend_py/app/auth.py`
- `backend_py/app/api/users.py`
- `backend_py/app/api/frameworks.py`
- `backend_py/scripts/seed_admin.py`
- `docs/migration/phases/phase-01-auth-baseline/checklist.md`
- `docs/migration/phases/phase-01-auth-baseline/phase-report.md`
- `docs/migration/phases/phase-01-auth-baseline/verification.md`

## Auth Changes

- `backend_py/app/auth.py` now uses `argon2-cffi` `PasswordHasher(type=Type.ID)`.
- New password hashes start with `$argon2id$`.
- `verify_password()` remains a boolean compatibility wrapper.
- `verify_password_with_rehash()` returns `(valid, needs_rehash)`.
- Legacy `salt$sha256hash` values remain verifiable.
- Legacy hash success returns `needs_rehash=True`.
- Argon2id verification failures return `False` without exposing password or full hash material in logs.
- `get_current_user_id()` remains the JWT subject dependency.
- `get_current_user()` returns the database `User` object and returns `404` when the JWT subject no longer maps to a user.

## Registration Policy

- `ENABLE_PUBLIC_REGISTER` defaults to `false`.
- `/api/users/register` returns `403` unless `ENABLE_PUBLIC_REGISTER=true` and the requested email is present in `ALLOWED_EMAILS`.
- This Phase does not allow first-user self-registration as super admin.
- Administrator creation is handled by `backend_py/scripts/seed_admin.py`.
- The seed script reads `SUPER_ADMIN_EMAIL` and `SUPER_ADMIN_PASSWORD`, fails fast when either is missing, and creates the user with an Argon2id password hash.
- The current `User` model has no `is_admin` field. Until the database migration Phase adds a formal admin field, `SUPER_ADMIN_EMAIL` is the documented admin identity boundary.

## User ID Trust Boundary

The following endpoints no longer trust frontend-provided user identity:

- `POST /api/frameworks/generate-from-text`
  - Removed `user_id` from `TextGenerateRequest`.
  - Added `user_id: str = Depends(get_current_user_id)`.
  - If legacy clients still send a `user_id` JSON field, Pydantic ignores it and JWT remains authoritative.
- `POST /api/frameworks/generate-from-files`
  - Replaced `user_id: str = Form(None)` with `Depends(get_current_user_id)`.
  - Legacy multipart `user_id` fields are ignored.
- `GET /api/frameworks/my-frameworks`
  - Replaced `user_id: str = Query(None)` with `Depends(get_current_user_id)`.
- `POST /api/frameworks/log-event`
  - Keeps the old request schema field for compatibility, but ignores it and writes the JWT `user_id` into the event payload.

Existing private framework detail/update/delete routes already used `Depends(get_current_user_id)` and were left intact.

## Verification Summary

See `verification.md` for command output.

Summary:

- Python syntax check passed for the required Phase 1 backend files.
- `user_id` Body / Query / Form / Path grep returned no matches.
- `request.user_id` grep returned no matches.
- Argon2id dependency and `PasswordHasher` usage are present.
- The `sha256(` grep still finds the intentional legacy verifier only.
- Secret scan returned no matches.
- Legacy Cloud LLM guardrail scan returned no matches in the checked deploy files.
- Runtime password helper smoke test passed for Argon2id valid/invalid and legacy hash migration behavior.

## Known Deferrals

- httpOnly cookie and refresh token flow are not implemented in this Phase and must not be counted as complete. The backend still returns a 7d access token for `Authorization: Bearer` compatibility; the frontend stores it in `localStorage` until the Phase 6 auth rewrite or a dedicated cookie-auth pass.
- Frontend Firebase Auth removal remains deferred to Phase 6.
- DeepSeekProvider remains deferred to Phase 3.
- Postgres, Alembic, and pgvector remain deferred to Phase 4.
- Full Provider abstraction and legacy Vector Store cleanup remain deferred to Phase 2+.
- Broader auth hardening for legacy endpoints that do not accept `user_id` directly, such as export/regenerate/AI ops/vector sync paths, was deferred at Phase 1 close and then addressed in Phase 01.1.

## Handoff To Phase 2

Phase 2 can begin Provider abstraction work. The key auth baseline is now available: backend routes can depend on `get_current_user_id()` or `get_current_user()` and treat JWT as the only trusted source of user identity.
