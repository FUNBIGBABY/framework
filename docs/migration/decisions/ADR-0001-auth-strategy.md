# ADR-0001: Auth Strategy

## Status

Accepted and implemented

## Context

The legacy project mixed Firebase Auth, backend-local JWT, and frontend-provided `user_id` values in request body, query, or form data. This created a severe identity trust-chain problem because private backend actions could trust user identity supplied by the client instead of deriving identity from a verified token.

## Decision

The new project adopts option A: self-hosted backend JWT, allowlist, and no public registration.

## Consequences

- Frontend Firebase Auth was removed from the active frontend route in Phase 6.
- All private backend endpoints must derive `user_id` from JWT.
- Browser auth uses a 1h access cookie and a 30d refresh cookie. Both are `httpOnly`; the implementation sets `Secure` when `ENV` / `APP_ENV` declares production or `AUTH_COOKIE_SECURE` is truthy, and `SameSite=Lax` is the default.
- The canonical auth route family is `/api/users/login`, `/api/users/me`, `/api/users/refresh`, and `/api/users/logout`; no parallel `/api/auth/*` contract is used.
- The frontend stores no auth token in `localStorage` or `sessionStorage` and sends private requests with credentials included.
- Protected routes authenticate from the access cookie only and reject `Authorization: Bearer` as a protected-route credential.
- Cookie-authenticated unsafe methods are protected by the configured Origin/Referer CSRF policy.
- Firebase ID Token is not the main route for the new project.
- Phase 1 established Argon2id, the allowlist/registration boundary, and the backend-trusted `user_id` contract. Phase 6 completed the cookie-session, refresh/logout, frontend token removal, and Bearer-removal work.
