# ADR-0002: Historical Ownerless Material Disposition

## Status

Owner-approved on 2026-07-15; Phase 7 still pending.

## Decision owners

Project Owner, acting as Security Owner and Backend Owner

## Approval source

Explicit Project Owner confirmation to the Project Steward on 2026-07-15.

## Context

The repository migration defines a nullable Materials `owner_id` and an intended `ON DELETE SET NULL` foreign-key action; live PostgreSQL proof of that action remains a Phase 7 blocker. Historical Material rows may have `owner_id IS NULL`. The reviewed current application behavior creates new rows with authenticated ownership and uses owner-filtered, non-enumerating retrieval: a row outside the authenticated user's ownership scope is not exposed through the application retrieval path. Historical ownerless rows consequently remain quarantined from authenticated listing and retrieval.

Phase 7 needed an explicit joint Security Owner and Backend Owner disposition for those historical ownerless rows. The 2026-07-13 review event `MR-2EC4192-20260713-01` recorded that disposition evidence as absent while also recording that the quarantine was not an active IDOR. This ADR records the later owner decision without rewriting that historical finding.

## Decision

- For every historical Material row whose `owner_id IS NULL`, quarantine is the final disposition for this migration / Phase 7 scope.
- Do not automatically backfill, infer, fabricate, or arbitrarily assign an owner.
- Do not expose, list, retrieve, or unquarantine these rows through authenticated application paths.
- This decision requires no database mutation or deletion.
- A future ownership mapping is allowed only when authoritative provenance exists and a separately authorized, independently reviewed migration preserves that evidence.
- Future deletion requires separate explicit authorization.
- This owner decision is not a reviewer verdict, does not accept Phase 7, and does not open Phase 8.

## Consequences and future-change controls

- The owner-disposition evidence previously absent at the 2026-07-13 review now exists for evaluation by the next named Phase 7 Reviewer.
- Historical ownerless rows remain quarantined. Authenticated application paths must not expose, list, retrieve, or unquarantine them.
- No ownership value may be inferred from unrelated fields, fabricated, or assigned merely to make a row retrievable.
- Any future ownership mapping requires authoritative provenance and a separately authorized, independently reviewed migration that preserves the provenance evidence.
- Any future deletion requires separate explicit authorization.
- This decision neither amends nor replaces the historical `MR-2EC4192-20260713-01` finding.

## Governance and execution scope

This is a docs-only owner-decision record. No rows were enumerated, modified, mapped, deleted, or unquarantined while creating it. No database, runtime, migration, Docker, browser, or external-system action occurred.

This record is not a review event or reviewer verdict and does not create an `accepted_commit`. Phase 7 remains `pending` until a named Reviewer evaluates the candidate. Live PostgreSQL `0005` upgrade/current, FK/index, actual `ON DELETE SET NULL`, and authenticated 404 evidence from Database Migration Owner remain a Phase 7 blocker. A reviewed Node-compatible builder from Container Runtime Owner also remains a Phase 7 blocker.

Phase 8 remains `pending` / `closed` and is not opened by this decision.
