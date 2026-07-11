# Migration README

This directory records the migration from the legacy customer project to a personal AI Agent project.

## Authority and review governance

- `MIGRATION_PHASES.md` is the highest canonical migration plan. It controls scope, dependencies, owners, and acceptance gates.
- `docs/migration/REVIEW_LEDGER.md` is the authoritative index for phase/slice review verdicts and acceptance status. It cannot override the canonical plan.
- Phase `checklist.md`, `phase-report.md`, and `verification.md` files remain historical execution evidence.
- A commit title, implementation commit, later status-wording commit, or pushed ref does not prove reviewer acceptance.
- The ledger is append-oriented. Allowed verdicts are `pending`, `rejected`, `accepted`, and `accepted_with_documented_deferral`.
- Missing reviewer, review date, or original verdict artifact must be recorded as `artifact unavailable`; do not infer those fields. Schedule a focused re-review.

Each Phase must have an independent folder. Each Phase folder must contain at least:

- `phase-report.md`
- `checklist.md`
- `verification.md`

When a later AI Agent takes over development, it should read these files first:

1. `MIGRATION_PHASES.md`
2. `docs/PERSONAL_USE_BOUNDARY.md`
3. `docs/migration/README.md`
4. `docs/migration/decisions/*.md`
5. `docs/migration/REVIEW_LEDGER.md`
6. The current Phase `checklist.md`, `phase-report.md`, and `verification.md`

Archived audit notes may exist under `docs/`, but they are reference material only. `MIGRATION_PHASES.md` is the canonical migration plan.

Phase 0 locks the Auth strategy to option A: self-hosted backend JWT, allowlist, and no public registration. Firebase Auth and Firebase ID Token are not part of the new project route.

Current browser auth is implemented as a 1h access cookie plus a 30d refresh cookie. Both are `httpOnly`; the implementation sets `Secure` when the process declares `ENV` / `APP_ENV` as production or when `AUTH_COOKIE_SECURE` is truthy, and `SameSite=Lax` is the default. The canonical route family is `/api/users/login`, `/api/users/me`, `/api/users/refresh`, and `/api/users/logout`. The frontend stores no auth token, and protected routes authenticate from the access cookie only; `Authorization: Bearer` is rejected as a protected-route credential. Cookie-authenticated unsafe methods are guarded by the configured Origin/Referer policy.

User creation for the migration route remains script/admin controlled: use `backend_py/scripts/seed_admin.py` for the current administrator account, and add future users through admin-only backend user management when that exists. Public frontend signup is disabled.

## Evidence and downstream gates

- Phase 0 GCP key Disable/Delete and old reachable-remote cleanup require manual external evidence. A clean current Git tree does not prove either action; the ledger keeps them unresolved until evidence is attached.
- Missing browser smoke is not automatically a blocker. If Docker/Postgres/migrated schema/running services/seeded credentials are unavailable, record `not run`, the exact blocker, owner, and trigger. A named reviewer may use `accepted_with_documented_deferral`.
- Phase 6 retains its historical `accepted_with_documented_deferral` verdict for browser smoke, while its original reviewer identity/date/raw artifact is unavailable and needs focused re-review before the evidence is audit-grade.
- Phase 7 currently remains `pending`; `fa97afd2de0fd9dea66fe86a519f440285717552` is a pushed candidate, not an accepted closeout.
- Phase 8 dependencies are Phases 3, 4, 5, and 7. Phase 8 planning cannot begin until Phase 7 has a named reviewer verdict of `accepted` or `accepted_with_documented_deferral` with explicit owner/trigger. No Phase 8 implementation may begin before its planning package is reviewed.
