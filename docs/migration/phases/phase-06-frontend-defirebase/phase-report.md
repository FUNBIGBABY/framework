# Phase 06 Initial Report - Frontend de-Firebase

Planning status: initial planning report only. No backend or frontend implementation has happened in Phase 6, and Phase 6 is not complete.

## Status

Phase 6 planning documentation exists and has been amended after reviewer findings. Implementation has not started from this report.

Current Phase 6 status:

- Planning package created: `checklist.md`, `phase-plan.md`, `verification.md`, and this `phase-report.md`.
- Canonical auth route decision recorded: Phase 6 uses only the `/api/users/*` auth route family.
- Round 1 owns narrow backend cookie-session repair if the Phase 1 token strategy debt is still present.
- CSRF/Origin/Referer verification requirements are explicit.
- Phase 5 final review accepted the closeout; Phase 6 planning may proceed.

## Scope

Phase 6 owns frontend de-Firebase work required to remove active frontend Firebase runtime dependency and SDK usage.

Included:

- Narrow backend cookie-session repair if required for Phase 6 cookie auth.
- AuthContext migration to backend cookie session.
- Shared frontend REST client cleanup.
- Core framework REST wiring.
- Library and publish/unpublish REST wiring.
- Admin users REST wiring.
- Artefact subresource REST wiring.
- Firebase SDK package/env removal.
- Isolation or deletion of Firebase-importing frontend residue only when required to uninstall the SDK.

Excluded:

- Phase 7 semantic cleanup of Valorie/domain/tenant/invite/migration residue.
- Tenant, workspace, invite, organization, or sharing redesign.
- Public registration or anonymous API/library access.
- Firebase Auth, Firebase ID token, Firestore, or new Firebase project setup.
- Agent, LLMWiki, Chat UI, MCP, RAG retrieval, pgvector indexing, or embedding.
- Reopening Phase 5 implementation.

## Round Breakdown

Round 0: canonical doc alignment and focused inventory.

Round 1: cookie session strategy, narrow backend session repair if needed, CSRF/Origin protection, and AuthContext foundation.

Round 2: core framework REST wiring.

Round 3: Library plus publish/unpublish REST.

Round 4: Admin users REST.

Round 5: artefact subresource wiring.

Round 6: Firebase SDK removal and closeout.

## Current Planning State

The planning package now states:

- Phase 6 must not preserve 7d Bearer plus `localStorage` as the final path.
- The frontend restore flow uses `/api/users/me` from cookie auth.
- Expired access uses `POST /api/users/refresh`.
- Logout uses `POST /api/users/logout`.
- Temporary Bearer compatibility, if retained during transition, must have a documented removal gate and cannot satisfy Phase 6 closeout.
- Unsafe cookie-authenticated methods require explicit CSRF/Origin/Referer protection and tests.
- Phase 6 implementation can proceed from the accepted Phase 5 REST surfaces without reopening Phase 5 implementation.

## Reviewer Findings Addressed

1. Auth endpoint canonical conflict:

- `MIGRATION_PHASES.md` was updated from `/api/auth/refresh` and `/api/auth/logout` to `/api/users/refresh` and `/api/users/logout`.
- Phase 6 docs now explicitly use `POST /api/users/login`, `GET /api/users/me`, `POST /api/users/refresh`, and `POST /api/users/logout`.
- Phase 6 docs now say not to introduce dual `/api/auth/*` and `/api/users/*` contracts.

2. CSRF/Origin verification gap:

- Round 1 now requires concrete positive and negative backend tests for cookie-authenticated unsafe methods.
- Required cases include allowed same-origin unsafe pass, missing or invalid Origin/Referer rejection where policy requires it, disallowed Origin rejection, safe methods not incorrectly blocked, and SameSite=None stronger-token success/failure if applicable.

3. Missing `phase-report.md`:

- This initial planning report was created.

4. Phase 5 acceptance gate:

- Phase 6 docs now record that Phase 5 final review accepted the closeout, the staged package was committed and pushed, and Phase 6 planning may proceed.
- Phase 6 must not reopen Phase 5 implementation.

## Open Risks

- Phase 5 acceptance documentation has been corrected in the Phase 5 closeout docs; Phase 6 may proceed from the accepted Phase 5 REST surfaces without reopening Phase 5 implementation.
- Round 1 may need backend cookie-session repair before frontend auth migration can proceed.
- CSRF policy details must be concrete enough to test; SameSite=None requires stronger protection such as double-submit token.
- Some Firebase-importing files are also Phase 7 residue. Phase 6 may isolate or delete them only to remove active Firebase dependency.
- Admin UI may expose whitelist-domain concepts without a Phase 5 backend endpoint.
- Artefact UI may still be coupled to legacy `frameworks.artefacts_json`; historical backfill is not Phase 6 scope.

## Completion Note

Phase 6 is not complete. This report records planning state only and does not verify implementation.
