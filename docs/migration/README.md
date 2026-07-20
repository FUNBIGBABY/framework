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
- The `P0: None` finding in review event `MR-2EC4192-20260713-01` applies only to that three-commit review scope; it does not establish that the historical Phase 0 external evidence above is complete.
- Missing browser smoke is not automatically a blocker. If Docker/Postgres/migrated schema/running services/seeded credentials are unavailable, record `not run`, the exact blocker, owner, and trigger. A named reviewer may use `accepted_with_documented_deferral`.
- Governance candidate `c32bb88ce21eabde2141712499713e3c9569b4cd` was rejected. `origin/main@c32bb88ce21eabde2141712499713e3c9569b4cd` records transport state only; its `accepted_commit` is absent. Reviewer identity and review date remain `artifact unavailable`; see `GOV-C32BB88-REJECTION-01` for the supplied findings.
- Named review event `MR-2EC4192-20260713-01` accepted the three-commit corrective remediation as a whole at reviewed/accepted commit `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`. This accepts the corrective code and governance package; it does not make Phase 7 complete or override the separate phase verdicts. The original artifact is preserved at `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`. At the review timestamp, local `main@2ec4192` was three commits ahead of locally tracked `origin/main@c32bb88`; the reviewer did not query the remote or push during the review.
- Phase 3 remains `pending` because the authorized real `DeepSeekProvider.tool_call()` smoke against the official endpoint was not run. LLM Provider Owner owns readiness and Migration Verification Owner owns execution under the artifact's stated key/endpoint/config/candidate triggers.
- Phase 5 is `accepted_with_documented_deferral` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`. Historical embedded-artefact versus child-row reconciliation remains `not run`, and the three legacy sync routes remain authenticated HTTP 501 quarantine shells; Data Reconciliation Owner and Phase 9 RAG Replacement Owner retain the stated conditions and triggers.
- Phase 6 is `accepted_with_documented_deferral` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`. Authenticated browser smoke was not run because the complete live environment is unavailable and the Docker builder remains incompatible. Container Runtime Owner owns the compatible builder and Migration Verification Owner owns browser smoke, triggered by the reviewed Node-compatible builder plus the complete authorized live environment before a release relying on these flows. `27679f8ff832a70a7f69782d8d45a52eab343525` remains a historical implementation candidate, not this review's accepted commit.
- At review event `MR-2EC4192-20260713-01`, Phase 7 was `pending` at reviewed commit `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`, with no `accepted_commit`. The Reviewer recorded three blockers: Security Owner + Backend Owner legacy-owner mapping/disposition approval; Database Migration Owner live `0005` upgrade/current, FK/index, and actual `ON DELETE SET NULL` evidence; and a reviewed Node-compatible builder from Container Runtime Owner. Ownerless rows were quarantined and were not an active IDOR, but that did not clear the ownership blocker. This remains the faithful historical finding.
- The later Project Owner decision recorded in `docs/migration/decisions/ADR-0002-ownerless-material-disposition.md` supplies the previously absent joint Security Owner + Backend Owner disposition evidence for evaluation by the next named Phase 7 Reviewer. It does not amend `MR-2EC4192-20260713-01`, does not show that the Reviewer accepted ADR-0002, and creates no Phase 7 verdict or `accepted_commit`. Phase 7 remains `pending`. The unresolved technical blockers are the Database Migration Owner's live PostgreSQL `0005` upgrade/current, FK/index, actual `ON DELETE SET NULL`, and authenticated 404 evidence, plus the Container Runtime Owner's reviewed Node-compatible builder. Browser smoke remains eligible for documented deferral and is not independently the acceptance blocker. Phase 8 remains `pending` / `closed`.
- Phase 8 dependencies are Phases 3, 4, 5, and 7. Its verdict is `pending` and its gate state is `closed`: planning cannot begin until Phase 7 has a named reviewer verdict of `accepted` or `accepted_with_documented_deferral` with explicit owner/trigger and all canonical dependencies are acceptable; implementation cannot begin before its planning package is reviewed. No Phase 8 planning or implementation artifact exists.
- Phase 5's `sync-library`, `push-framework`, and `log-event` successful behaviors are intentionally deleted; the authenticated HTTP 501 route shells are a quarantined deferred compatibility surface, not functional parity. Phase 9 RAG Replacement Owner owns any future replacement contract and need not preserve the legacy route names or request schemas. Phase 9 is not implemented by this correction.
