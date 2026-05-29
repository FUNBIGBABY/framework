# ADR-0001: Auth Strategy

## Status

Accepted

## Context

The legacy project mixed Firebase Auth, backend-local JWT, and frontend-provided `user_id` values in request body, query, or form data. This created a severe identity trust-chain problem because private backend actions could trust user identity supplied by the client instead of deriving identity from a verified token.

## Decision

The new project adopts option A: self-hosted backend JWT, allowlist, and no public registration.

## Consequences

- Frontend Firebase Auth will be removed in a later Phase.
- All private backend endpoints must derive `user_id` from JWT.
- `localStorage` token storage will later migrate to an httpOnly cookie strategy.
- Firebase ID Token is not the main route for the new project.
- Phase 1 is responsible for Argon2id, allowlist registration, refresh token strategy, and blocking frontend-provided `user_id` permissions.

