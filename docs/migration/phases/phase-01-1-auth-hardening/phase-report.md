# Phase 01.1 Report - Auth Hardening

## Scope

This small hardening pass closes the review gaps found after Phase 1. It stays within the auth boundary and does not start Phase 2 Provider abstraction, DeepSeekProvider, Postgres, pgvector, Agent, RAG, LLMWiki, or frontend Firebase removal.

## Files Changed

- `.env.example`
- `backend_py/app/api/frameworks.py`
- `backend_py/app/api/materials.py`
- `backend_py/app/api/users.py`
- `backend_py/main.py`
- `backend_py/app/models.py`
- `backend_py/scripts/seed_admin.py`
- `backend_py/tests/test_auth_hardening.py`
- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/App.jsx`
- `frontend/src/components/AIMergeMode.jsx`
- `frontend/src/components/ArtefactEditor.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/LandingPage.jsx`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/PublishModal.jsx`
- `frontend/src/components/Signup.jsx`
- `frontend/src/lib/api.js`
- `frontend/src/lib/firebase.js`
- `README.md`
- `docs/migration/README.md`
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
- `backend_py/main.py` now loads root `.env` and `backend_py/.env` before importing routers that import `app.auth`, so `JWT_SECRET_KEY` can come from dotenv before auth module import.
- Added `Depends(get_current_user_id)` to private materials endpoints:
  - `POST /materials/upload-file`
  - `GET /materials/{material_id}`
  - `POST /materials/ingest-text`
- `GET /materials/ping` remains public for health/smoke checks.

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
- It also verifies anonymous materials private endpoints return `401` or `403`, while `GET /materials/ping` remains public.

## Frontend Compatibility Debt

- `frontend/src/contexts/AuthContext.jsx` now calls backend `POST /api/users/login` first and stores the returned `access_token` in `localStorage` for existing Bearer-header API calls.
- Firebase login is retained only as a Phase 6 compatibility layer for Firestore tenant/profile metadata and blocked-user checks. Backend JWT is now the frontend's private API credential.
- If Firebase login fails after backend login succeeds, the session remains authenticated for backend APIs, but Firebase-only tenant/profile features may be absent until Phase 6 removes Firestore dependencies.
- `frontend/src/lib/api.js` now exports `apiFetch()` and shared auth-header helpers that read `localStorage.access_token`, not `localStorage.token`.
- Direct protected framework calls in `AIMergeMode.jsx`, `FrameworkEditor.jsx`, `ArtefactEditor.jsx`, `FrameworkCard.jsx`, and `PublishModal.jsx` now go through `apiFetch()`, so export, regenerate, AI merge/fill, and push-framework requests send `Authorization: Bearer <access_token>`.
- `getMyFrameworks()` and `getMyFrameworksByFamily()` no longer return early when `auth.currentUser` is absent. Legacy Firebase `user_id` query parameters are only appended when a Firebase user exists; backend-JWT-only sessions rely on the backend JWT subject.
- Some legacy Firebase-era code still reads `auth.currentUser.uid` for Firestore compatibility and optional `user_id` compatibility fields. The backend ignores or rejects frontend-provided `user_id` and uses JWT dependencies instead.
- Phase 6 must remove Firebase Auth, Firestore profile reads, and frontend `user_id` plumbing fully.

## Public Registration UI

- `frontend/src/App.jsx` no longer registers a `/signup` route.
- `frontend/src/components/Login.jsx` no longer links to signup.
- `frontend/src/components/LandingPage.jsx` no longer sends CTA buttons to `/signup`.
- `frontend/src/components/Navbar.jsx` no longer treats `/signup` as a public auth page.
- `frontend/src/contexts/AuthContext.jsx` no longer calls Firebase `createUserWithEmailAndPassword`; `signup()` returns a disabled-registration result.
- `frontend/src/components/Signup.jsx` is a disabled-registration informational component only.
- `frontend/src/lib/firebase.js` keeps the old `registerUser` export only as a disabled compatibility stub that throws.
- User creation remains through `backend_py/scripts/seed_admin.py` or future admin-only backend user management. No new public registration flow was added.

## Known Deferrals

- 1h access token + refresh/httpOnly cookie remains deferred and is explicitly a Phase 6 compatibility debt. Current code still uses the 7d Bearer token and `localStorage` compatibility path.
- Legacy OpenAI Vector Store and old LLM code paths remain deferred to later Provider / DeepSeek phases.
- Full route ownership checks for arbitrary framework payloads are not solved here; this pass only prevents anonymous invocation.
- Frontend Firebase Auth removal and remaining optional frontend `user_id` compatibility parameters remain deferred to Phase 6.
- Public signup remains disabled by default. Future user creation belongs to admin-only backend user management, not a public frontend route.

## Handoff

Phase 2 can proceed after this hardening pass. The auth boundary is stricter than Phase 1: high-cost and legacy sync routes now require a JWT before they can run.
