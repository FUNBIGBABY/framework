# Migration Review Ledger

This append-oriented ledger is the authoritative index for migration phase/slice review verdicts and acceptance status. `MIGRATION_PHASES.md` remains the highest canonical migration plan and defines scope, dependencies, and acceptance requirements. This ledger cannot override that plan. Phase `checklist.md`, `phase-report.md`, and `verification.md` files remain historical execution evidence.

## Ledger rules

- Append a new record for a new review, re-review, correction, or superseding verdict. Do not silently rewrite an earlier verdict.
- Allowed `verdict` values are `pending`, `rejected`, `accepted`, and `accepted_with_documented_deferral`.
- A commit title, implementation commit, status-wording commit, local branch, or pushed ref is not reviewer acceptance.
- `reviewed_commit` and `accepted_commit` use full SHAs only when the reviewer artifact or an explicit preserved owner handoff identifies the commit in that role. Known implementation, candidate, fix, status-wording, local-branch, or pushed-ref evidence belongs in `conditions`, `evidence`, or `pushed_ref`; it is not proof of review or acceptance.
- If the original reviewer, review date, or verdict artifact is missing, write `artifact unavailable`; do not infer it from commit messages or phase prose. Schedule a focused re-review.
- A documented deferral must name its exact condition, owner, and trigger. An unavailable browser environment is not automatically a blocker: a named reviewer may use `accepted_with_documented_deferral` when the residual condition is explicit.
- `artifact_status` describes whether the underlying reviewer artifact is independently available. It is separate from the historical verdict.

## Initial records

### GOV-20260710-01

- `review_id`: `GOV-20260710-01`
- `phase_slice`: `Phase 1-7 governance repair`
- `reviewer`: `artifact unavailable; focused Migration Reviewer re-review required`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `—; uncommitted candidate pending review`
- `verdict`: `pending`
- `conditions`: Review this docs-only reconciliation, including canonical/ledger authority, capability inventory coverage, auth wording, Phase 7 status, and the Phase 8 planning gate.
- `accepted_commit`: `—`
- `pushed_ref`: `—; this repair must not be committed or pushed by the executor`
- `evidence`: `fa97afd2de0fd9dea66fe86a519f440285717552` is the base Phase 7 candidate only and does not prove that this governance repair was reviewed or accepted; `MIGRATION_PHASES.md`; this ledger; `docs/migration/phases/phase-03-deepseek-v4/`; `docs/migration/phases/phase-05-backend-firestore-business/`; `docs/migration/phases/phase-06-frontend-defirebase/`; `docs/migration/phases/phase-07-domain-legacy-cleanup/`
- `artifact_status`: `pending; reviewer artifact not yet created`

### P0-SECURITY-20260710-01

- `review_id`: `P0-SECURITY-20260710-01`
- `phase_slice`: `Phase 0 exposed GCP key and reachable-history external action`
- `reviewer`: `artifact unavailable`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: Unresolved external action. Security Owner must provide sanitized manual evidence that key id `b99f494a12` was Disabled and Deleted in GCP, including actor/time or an audit-log reference. Repository Owner must provide evidence that every old reachable remote/history containing the key was removed, rewritten, or retired. A clean current working tree or reachable-tree scan does not prove either action.
- `accepted_commit`: `—`
- `pushed_ref`: `origin/main contains the implementation commit according to the local tracking ref; this is not cloud-key revocation or acceptance evidence`
- `evidence`: `61921f935756e471c676ce93c2e45ec1d35209a4` is known Phase 0 implementation evidence only and does not prove that the commit was reviewed or accepted; `docs/migration/phases/phase-00-security-auth/phase-report.md`; `docs/migration/phases/phase-00-security-auth/verification.md`
- `artifact_status`: `artifact unavailable; focused security re-review required after external evidence is attached`

### P1-AUTH-20260710-01

- `review_id`: `P1-AUTH-20260710-01`
- `phase_slice`: `Phase 1 / 1.1 auth baseline and hardening`
- `reviewer`: `artifact unavailable`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: Focused Migration Reviewer re-review of the historical Phase 1 scope. Current cookie-session behavior was completed later in Phase 6 and must not be backdated into the Phase 1 execution evidence.
- `accepted_commit`: `—`
- `pushed_ref`: `origin/main contains the candidate according to the local tracking ref; not acceptance evidence`
- `evidence`: `5c66b646be2f9012f11a764559464e0b19ef4a9e` is known Phase 1-3 fix evidence only and does not prove that Phase 1 or the commit was reviewed or accepted; `docs/migration/phases/phase-01-auth-baseline/`; `docs/migration/phases/phase-01-1-auth-hardening/`
- `artifact_status`: `phase evidence available; original reviewer artifact unavailable; focused re-review required`

### P2-PROVIDERS-20260710-01

- `review_id`: `P2-PROVIDERS-20260710-01`
- `phase_slice`: `Phase 2 provider abstraction`
- `reviewer`: `artifact unavailable`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: Focused Migration Reviewer re-review of the provider boundary and recorded Phase 2 deferrals.
- `accepted_commit`: `—`
- `pushed_ref`: `origin/main contains the candidate according to the local tracking ref; not acceptance evidence`
- `evidence`: `5c66b646be2f9012f11a764559464e0b19ef4a9e` is known Phase 1-3 fix evidence only and does not prove that Phase 2 or the commit was reviewed or accepted; `docs/migration/phases/phase-02-provider-abstraction/`
- `artifact_status`: `phase evidence available; original reviewer artifact unavailable; focused re-review required`

### P3-DEEPSEEK-20260710-01

- `review_id`: `P3-DEEPSEEK-20260710-01`
- `phase_slice`: `Phase 3 DeepSeek provider integration`
- `reviewer`: `artifact unavailable`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: Real DeepSeek smoke remains not run. LLM Provider Owner owns provider readiness; Migration Verification Owner runs the smoke when an authorized `DEEPSEEK_API_KEY`, reachable endpoint, non-dev/non-dry-run configuration, and review candidate are available. Re-run after a base URL, model, thinking policy, SDK, or provider call-path change. Phase 3 owns provider response preservation; active-run next-round `reasoning_content` carry-back belongs to Phase 8 implementation/verification and is not a pre-Phase-8 implementation condition.
- `accepted_commit`: `—`
- `pushed_ref`: `origin/main contains the candidate according to the local tracking ref; not acceptance evidence`
- `evidence`: `5c66b646be2f9012f11a764559464e0b19ef4a9e` is known Phase 1-3 fix evidence only and does not prove that Phase 3 or the commit was reviewed or accepted; `docs/migration/phases/phase-03-deepseek-v4/checklist.md`; `phase-report.md`; `verification.md`
- `artifact_status`: `real-provider artifact unavailable; focused re-review required after the authorized smoke`

### P4-POSTGRES-20260710-01

- `review_id`: `P4-POSTGRES-20260710-01`
- `phase_slice`: `Phase 4 Postgres + pgvector baseline`
- `reviewer`: `artifact unavailable`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: Focused Migration Reviewer re-review of the retained Phase 4 live-schema evidence and corrected smoke record. Any later Alembic-head change requires new live Postgres evidence owned by the Database Migration Owner.
- `accepted_commit`: `—`
- `pushed_ref`: `origin/main contains the candidate according to the local tracking ref; not acceptance evidence`
- `evidence`: `c38309de56a3958d3ca1ed2e96bfeb24f1c720b6` is known Phase 4 implementation/candidate evidence only and does not prove that the phase or commit was reviewed or accepted; `docs/migration/phases/phase-04-postgres-pgvector/`
- `artifact_status`: `phase verification available; original reviewer identity/date/verdict artifact unavailable; focused re-review required`

### P5-FIRESTORE-20260710-01

- `review_id`: `P5-FIRESTORE-20260710-01`
- `phase_slice`: `Phase 5 backend Firestore business disposition`
- `reviewer`: `artifact unavailable`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: Focused Migration Reviewer must review `capability-inventory.md`. The implementation commit is `742f1e79f3fb71d44ce21284999e64ca76c5060f`; `a2115042771d9e91e9410cf5597031f3c78bee9a` only added later status wording. Neither proves that a commit was reviewed or accepted. Artefact-history inspection remains `not run`. The existing SQL detects only non-empty embedded artefacts with zero child rows, so a zero result alone cannot establish that the whole reconciliation is `not applicable`. Data Reconciliation Owner must attach dated database/snapshot evidence comparing embedded artefact counts and identities with child rows, or an equivalent shape-aware audit with sampling and data-source provenance. Any non-zero result from that detector or partial/count/identity mismatch triggers separately authorized data reconciliation.
- `accepted_commit`: `—`
- `pushed_ref`: `origin/main contains both commits according to the local tracking ref; not acceptance evidence`
- `evidence`: `docs/migration/phases/phase-05-backend-firestore-business/`; `docs/migration/phases/phase-05-backend-firestore-business/capability-inventory.md`
- `artifact_status`: `original reviewer artifact unavailable; capability and data-disposition re-review required`

### P6-DEFIREBASE-20260710-01

- `review_id`: `P6-DEFIREBASE-20260710-01`
- `phase_slice`: `Phase 6 frontend de-Firebase closeout`
- `reviewer`: `artifact unavailable (repository history retains only the role label “Migration Reviewer”)`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `27679f8ff832a70a7f69782d8d45a52eab343525`
- `verdict`: `accepted_with_documented_deferral`
- `conditions`: Browser smoke was not run because Docker Desktop's Linux engine was unavailable and there was no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded admin credentials. This absence is not automatically a blocker. Migration Verification Owner owns the smoke; trigger when that complete environment and authorization are available, before a release that relies on the affected browser flows, or when a named reviewer carries it as an explicit later condition.
- `accepted_commit`: `27679f8ff832a70a7f69782d8d45a52eab343525 (historical accepted implementation record; not audit-grade until focused re-review)`
- `pushed_ref`: `origin/main contains the commit according to the local tracking ref and owner handoff; transport evidence is not the missing reviewer artifact`
- `evidence`: `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`; `phase-report.md`; `verification.md`
- `artifact_status`: `artifact unavailable; preserve the historical verdict, but require focused re-review with named reviewer/date before treating it as audit-grade evidence`

### P7-LEGACY-20260710-01

- `review_id`: `P7-LEGACY-20260710-01`
- `phase_slice`: `Phase 7 domain and legacy cleanup candidate`
- `reviewer`: `artifact unavailable; focused Migration Reviewer re-review required`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: `fa97afd2de0fd9dea66fe86a519f440285717552` is a pushed candidate only, not proof that it was reviewed or accepted. Run consolidated docs/static verification against one reviewed commit and obtain a named reviewer verdict. Browser smoke is currently not run because Docker Desktop's Linux engine was unavailable and there was no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded admin credentials; additionally, the current Dockerfile's Node 18 builder is incompatible with the locked Vite 7.1.9 / React Router 7.9.3 engine requirements. Container Runtime Owner owns the build correction, triggered by a separately reviewed compatible runtime candidate; Migration Verification Owner owns browser smoke, triggered after that correction and the complete authorized environment are available, before a release relying on these flows, or as an explicit later reviewer condition. The smoke may be carried by `accepted_with_documented_deferral` with those exact conditions/owners/triggers. Focused reviewer attention is also required for Materials ownership and legacy `vector_sync` request fields; this governance repair does not change either implementation.
- `accepted_commit`: `—`
- `pushed_ref`: `origin/main@fa97afd2de0fd9dea66fe86a519f440285717552 (local tracking ref observed 2026-07-10; candidate only)`
- `evidence`: `docs/migration/phases/phase-07-domain-legacy-cleanup/`; `git log --oneline`; `git status --short --branch`
- `artifact_status`: `candidate evidence available; reviewer verdict artifact not yet created`

### P8-PLANNING-GATE-20260710-01

- `review_id`: `P8-PLANNING-GATE-20260710-01`
- `phase_slice`: `Phase 8 planning prerequisite (governance gate only)`
- `reviewer`: `artifact unavailable; focused Migration Reviewer re-review required`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `—; no Phase 8 planning or implementation is authorized by this record`
- `verdict`: `pending`
- `conditions`: Canonical dependencies are Phases 3, 4, 5, and 7. Phase 8 planning cannot start until Phase 7 has a named reviewer verdict of `accepted` or `accepted_with_documented_deferral`. The latter must state exact conditions, owner, and trigger; `conditions=none` is not required. Phase 8 implementation cannot start before the Phase 8 planning package itself is reviewed.
- `accepted_commit`: `—`
- `pushed_ref`: `—`
- `evidence`: `MIGRATION_PHASES.md`; `P3-DEEPSEEK-20260710-01`; `P4-POSTGRES-20260710-01`; `P5-FIRESTORE-20260710-01`; `P7-LEGACY-20260710-01`
- `artifact_status`: `gate closed; no Phase 8 artifact exists`
