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

## Corrective review records

### GOV-C32BB88-REJECTION-01

- `review_id`: `GOV-C32BB88-REJECTION-01`
- `phase_slice`: `Phase 1-7 governance repair candidate`
- `reviewer`: `artifact unavailable; the supplied brief identifies only the Migration Reviewer role`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `c32bb88ce21eabde2141712499713e3c9569b4cd`
- `verdict`: `rejected`
- `conditions`: The supplied findings require all of the following corrective work: (A) append this rejection without altering `GOV-20260710-01`, supersede the unsupported Phase 6 acceptance record with current verdict `pending`, treat `27679f8ff832a70a7f69782d8d45a52eab343525` as an implementation candidate only, keep Phase 7 pending, and keep the Phase 8 gate closed; (B) remediate Materials as a P1 object-authorization defect with authenticated ownership on both creation paths, owner-filtered non-enumerating retrieval, two-user isolation tests, and an explicit ownerless-row policy owned by Security Owner and Backend Owner; (C) ensure DeepSeek thinking-mode tool calls never send `tool_choice`, preserve non-thinking behavior and response fields, replace the contrary unit assertion, and retain real-provider smoke as not run unless authorized evidence exists; (D) export a host-reachable `DATABASE_URL` before every host Alembic command, use placeholders, and make Compose startup health-aware before `/health`, without claiming unrun Docker/live-Postgres checks; and (E) classify `sync-library`, `push-framework`, and `log-event` as intentionally deleted successful behavior with quarantined deferred compatibility shells, not REST parity, while assigning any RAG replacement to Phase 9 without implementing it.
- `accepted_commit`: `—; absent`
- `pushed_ref`: `origin/main@c32bb88ce21eabde2141712499713e3c9569b4cd; transport state only, not acceptance`
- `evidence`: supplied corrective-remediation brief; the full raw reviewer artifact is not preserved as a repository file
- `artifact_status`: `reviewed SHA, transport state, role, verdict, and findings supplied; reviewer identity, review date, and raw artifact unavailable`

### P6-DEFIREBASE-CORRECTION-01

- `review_id`: `P6-DEFIREBASE-CORRECTION-01`
- `phase_slice`: `Phase 6 frontend de-Firebase current audit status correction`
- `reviewer`: `artifact unavailable; focused Migration Reviewer review required`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `—; 27679f8ff832a70a7f69782d8d45a52eab343525 is an implementation candidate only`
- `verdict`: `pending`
- `conditions`: This record supersedes `P6-DEFIREBASE-20260710-01` for current audit status without altering that historical record. No preserved artifact identifies a reviewer identity, review date, reviewed SHA, and verdict for the asserted acceptance. Browser smoke remains `not run`; Migration Verification Owner owns it, triggered when an authorized environment has live Postgres/pgvector, migrated schema, running backend/frontend, and seeded credentials, before a release relying on those flows or as an explicit condition in a future named review.
- `accepted_commit`: `—; absent`
- `pushed_ref`: `origin/main contains 27679f8ff832a70a7f69782d8d45a52eab343525; transport evidence only`
- `evidence`: `P6-DEFIREBASE-20260710-01`; `docs/migration/phases/phase-06-frontend-defirebase/` historical execution records
- `artifact_status`: `correction recorded; current verdict pending; reviewer identity/date/raw verdict artifact unavailable`

### P3-DEEPSEEK-CONTRACT-CORRECTION-01

- `review_id`: `P3-DEEPSEEK-CONTRACT-CORRECTION-01`
- `phase_slice`: `Phase 3 DeepSeek status and future Phase 8 replay-contract wording correction`
- `reviewer`: `artifact unavailable`
- `review_date`: `artifact unavailable`
- `reviewed_commit`: `artifact unavailable`
- `verdict`: `pending`
- `conditions`: This record explicitly supersedes only the Phase 8 replay-condition wording in `P3-DEEPSEEK-20260710-01`; it does not supersede any other wording or evidence in that record, and the Phase 3 verdict remains `pending`. Real DeepSeek smoke remains not run. The future continuing active-run contract is: every applicable subsequent provider request, including requests triggered by later user interactions, replays the required `reasoning_content`; assistant `content` is non-null at every replay serialization; regressions span beyond the immediately following request; and full reasoning remains short-lived and is excluded from long-term logs. This Phase 8 behavior is not implemented, and the Phase 8 gate remains closed.
- `accepted_commit`: `artifact unavailable; no acceptance claimed`
- `pushed_ref`: `artifact unavailable`
- `evidence`: `P3-DEEPSEEK-20260710-01`; `P8-PLANNING-GATE-20260710-01`; supplied contract-correction requirements
- `artifact_status`: `correction recorded; Phase 3 verdict pending; real DeepSeek smoke not run; Phase 8 behavior not implemented; Phase 8 gate closed; no acceptance claimed`

## Review event MR-2EC4192-20260713-01

The six entries below are verdict slices transcribed from the single review event `MR-2EC4192-20260713-01`; they are not six independent reviews. Findings labelled P0/P1/P2/P3 in the source artifact are finding priorities, not migration Phase numbers. The transcription source is `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`.

### GOV-MR-2EC4192-20260713-01

- `verdict_slice_id`: `GOV-MR-2EC4192-20260713-01`
- `review_id`: `MR-2EC4192-20260713-01`
- `phase_slice`: `Three-commit corrective remediation as a whole`
- `reviewer`: `Migration Reviewer Agent`
- `review_date`: `2026-07-13T21:44:01.9648007+08:00`
- `timezone`: `China Standard Time — (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi`
- `base_commit`: `c32bb88ce21eabde2141712499713e3c9569b4cd`
- `reviewed_HEAD`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `reviewed_commits`: `23831f2545ec715418348f1dc5e7aa711e339b60` — Fix material ownership authorization; `e902205f198540cc7a3abcc6b802ef285f45554f` — Harden DeepSeek thinking tool calls; `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` — Record corrective migration governance.
- `reviewed_commit`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `verdict`: `accepted`
- `conditions`: Accepts the corrective code and governance package; it does not override the separate pending/deferral phase verdicts below.
- `residual_risks`: No separate residual-risk field was stated for the overall slice; the Phase 3, 5, 6, 7, and 8 conditions and risks recorded in the other slices remain in force.
- `owners`: No separate owner was stated for the overall slice; the named owners in the phase slices remain responsible for their conditions.
- `triggers`: No separate trigger was stated for the overall slice; the named triggers in the phase slices remain in force.
- `blockers`: None for acceptance of the corrective remediation as a whole; separate Phase 3 and Phase 7 blockers and the closed Phase 8 gate are not cleared by this verdict.
- `accepted_commit`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `scope_note`: The source finding `P0: None` applies only to this three-commit review scope and does not establish completion of the historical Phase 0 external GCP-key or reachable-history evidence. The source's priority-P3 Materials assertion finding is non-blocking and is not a Phase 3 verdict or blocker.
- `pushed_ref`: At the review timestamp, local `main` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` was three commits ahead of the locally tracked `origin/main` at `c32bb88ce21eabde2141712499713e3c9569b4cd`. The reviewer did not query the remote or push during the review.
- `verification_performed`: The reviewer recorded focused backend `52 passed`, `29 warnings`, `8.04s` and complete backend `130 passed`, `219 warnings`, `16.16s`; the warnings were existing Pydantic v2 and `datetime.utcnow()` deprecations. Seven existing changed Python files compiled in memory with exit `0`. Alembic `heads` returned `0005_material_owner (head)`; offline `upgrade head --sql` exited `0`, produced `372` lines with SHA-256 `b3556584cf1f1ee6aab78f70dab47afcab257cb05df04d2a98323f29cc6c7674`, and contained `owner_id`, `ON DELETE SET NULL` FK, and index DDL. Frontend lint exited `0`; Vitest reported `10` files and `56 passed` in `9.47s`; the out-of-tree production build exited `0` with `135` modules in `6.59s` and retained the stated stale-browser-data and `850.25 kB` chunk warnings. The reviewer recorded `42` Markdown files, `0` local links, `10` external links, and `0` broken local links; the route/vendor/legacy/router/Phase 8-9 scans stated in the artifact; exact parent-chain and three-commit checks; clean worktree/index before and after; and aggregate/worktree/index diff checks exiting `0`.
- `verification_not_performed`: Docker build/runtime, browser smoke, live PostgreSQL upgrade/current/FK inspection or live `ON DELETE SET NULL` exercise, real DeepSeek, external GCP/key evidence, remote-server query, and push were not performed; `DEEPSEEK_API_KEY=NOT SET`.
- `artifact`: `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`
- `artifact_status`: `named reviewer artifact preserved; this record is a transcription of that artifact, not a new review`

### P3-MR-2EC4192-20260713-01

- `verdict_slice_id`: `P3-MR-2EC4192-20260713-01`
- `review_id`: `MR-2EC4192-20260713-01`
- `phase_slice`: `Phase 3 DeepSeek provider`
- `reviewer`: `Migration Reviewer Agent`
- `review_date`: `2026-07-13T21:44:01.9648007+08:00`
- `timezone`: `China Standard Time — (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi`
- `base_commit`: `c32bb88ce21eabde2141712499713e3c9569b4cd`
- `reviewed_HEAD`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `reviewed_commits`: `23831f2545ec715418348f1dc5e7aa711e339b60` — Fix material ownership authorization; `e902205f198540cc7a3abcc6b802ef285f45554f` — Harden DeepSeek thinking tool calls; `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` — Record corrective migration governance.
- `reviewed_commit`: `e902205f198540cc7a3abcc6b802ef285f45554f`, as represented at reviewed HEAD.
- `verdict`: `pending`
- `conditions`: Missing evidence is an authorized real `DeepSeekProvider.tool_call()` smoke against the official endpoint.
- `residual_risks`: The real provider call path has not been evidenced by the required authorized smoke.
- `owners`: LLM Provider Owner for readiness; Migration Verification Owner for execution.
- `triggers`: Authorized key, reachable official endpoint, non-dev/non-dry-run configuration, and reviewed candidate; rerun after base URL, model, thinking policy, SDK/default transport, or provider call-path changes.
- `blockers`: The authorized real `DeepSeekProvider.tool_call()` smoke against the official endpoint is absent.
- `pushed_ref`: At the review timestamp, local `main` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` was three commits ahead of the locally tracked `origin/main` at `c32bb88ce21eabde2141712499713e3c9569b4cd`. The reviewer did not query the remote or push during the review.
- `verification_performed`: The reviewer recorded focused backend `52 passed`, `29 warnings`, `8.04s` and complete backend `130 passed`, `219 warnings`, `16.16s`; the warnings were existing Pydantic v2 and `datetime.utcnow()` deprecations. Seven existing changed Python files compiled in memory with exit `0`. Alembic `heads` returned `0005_material_owner (head)`; offline `upgrade head --sql` exited `0`, produced `372` lines with SHA-256 `b3556584cf1f1ee6aab78f70dab47afcab257cb05df04d2a98323f29cc6c7674`, and contained `owner_id`, `ON DELETE SET NULL` FK, and index DDL. Frontend lint exited `0`; Vitest reported `10` files and `56 passed` in `9.47s`; the out-of-tree production build exited `0` with `135` modules in `6.59s` and retained the stated stale-browser-data and `850.25 kB` chunk warnings. The reviewer recorded `42` Markdown files, `0` local links, `10` external links, and `0` broken local links; the route/vendor/legacy/router/Phase 8-9 scans stated in the artifact; exact parent-chain and three-commit checks; clean worktree/index before and after; and aggregate/worktree/index diff checks exiting `0`.
- `verification_not_performed`: Docker build/runtime, browser smoke, live PostgreSQL upgrade/current/FK inspection or live `ON DELETE SET NULL` exercise, real DeepSeek, external GCP/key evidence, remote-server query, and push were not performed; `DEEPSEEK_API_KEY=NOT SET`.
- `artifact`: `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`
- `artifact_status`: `named reviewer artifact preserved; pending verdict transcribed without an accepted_commit`

### P5-MR-2EC4192-20260713-01

- `verdict_slice_id`: `P5-MR-2EC4192-20260713-01`
- `review_id`: `MR-2EC4192-20260713-01`
- `phase_slice`: `Phase 5 capability/governance`
- `reviewer`: `Migration Reviewer Agent`
- `review_date`: `2026-07-13T21:44:01.9648007+08:00`
- `timezone`: `China Standard Time — (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi`
- `base_commit`: `c32bb88ce21eabde2141712499713e3c9569b4cd`
- `reviewed_HEAD`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `reviewed_commits`: `23831f2545ec715418348f1dc5e7aa711e339b60` — Fix material ownership authorization; `e902205f198540cc7a3abcc6b802ef285f45554f` — Harden DeepSeek thinking tool calls; `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` — Record corrective migration governance.
- `reviewed_commit`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `verdict`: `accepted_with_documented_deferral`
- `conditions`: Historical embedded artefact versus child-row reconciliation remains `not run`; the three legacy sync routes remain authenticated 501 quarantine shells.
- `residual_risks`: Legacy artefact count/identity mismatches could exist; successful indexing/retrieval/logging is intentionally unavailable.
- `owners`: Data Reconciliation Owner; Phase 9 RAG Replacement Owner.
- `triggers`: Before importing legacy rows, deleting the embedded fallback, or on any mismatch; Phase 9 replacement only after that phase is authorized.
- `blockers`: No blocker to this documented-deferral acceptance; the recorded condition and residual risk remain, and this verdict does not authorize Phase 9.
- `accepted_commit`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `pushed_ref`: At the review timestamp, local `main` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` was three commits ahead of the locally tracked `origin/main` at `c32bb88ce21eabde2141712499713e3c9569b4cd`. The reviewer did not query the remote or push during the review.
- `verification_performed`: The reviewer recorded focused backend `52 passed`, `29 warnings`, `8.04s` and complete backend `130 passed`, `219 warnings`, `16.16s`; the warnings were existing Pydantic v2 and `datetime.utcnow()` deprecations. Seven existing changed Python files compiled in memory with exit `0`. Alembic `heads` returned `0005_material_owner (head)`; offline `upgrade head --sql` exited `0`, produced `372` lines with SHA-256 `b3556584cf1f1ee6aab78f70dab47afcab257cb05df04d2a98323f29cc6c7674`, and contained `owner_id`, `ON DELETE SET NULL` FK, and index DDL. Frontend lint exited `0`; Vitest reported `10` files and `56 passed` in `9.47s`; the out-of-tree production build exited `0` with `135` modules in `6.59s` and retained the stated stale-browser-data and `850.25 kB` chunk warnings. The reviewer recorded `42` Markdown files, `0` local links, `10` external links, and `0` broken local links; the route/vendor/legacy/router/Phase 8-9 scans stated in the artifact; exact parent-chain and three-commit checks; clean worktree/index before and after; and aggregate/worktree/index diff checks exiting `0`.
- `verification_not_performed`: Docker build/runtime, browser smoke, live PostgreSQL upgrade/current/FK inspection or live `ON DELETE SET NULL` exercise, real DeepSeek, external GCP/key evidence, remote-server query, and push were not performed; `DEEPSEEK_API_KEY=NOT SET`.
- `artifact`: `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`
- `artifact_status`: `named reviewer artifact preserved; documented-deferral acceptance transcribed`

### P6-MR-2EC4192-20260713-01

- `verdict_slice_id`: `P6-MR-2EC4192-20260713-01`
- `review_id`: `MR-2EC4192-20260713-01`
- `phase_slice`: `Phase 6 focused re-review`
- `reviewer`: `Migration Reviewer Agent`
- `review_date`: `2026-07-13T21:44:01.9648007+08:00`
- `timezone`: `China Standard Time — (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi`
- `base_commit`: `c32bb88ce21eabde2141712499713e3c9569b4cd`
- `reviewed_HEAD`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `reviewed_commits`: `23831f2545ec715418348f1dc5e7aa711e339b60` — Fix material ownership authorization; `e902205f198540cc7a3abcc6b802ef285f45554f` — Harden DeepSeek thinking tool calls; `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` — Record corrective migration governance.
- `reviewed_commit`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `verdict`: `accepted_with_documented_deferral`
- `conditions`: Authenticated browser smoke was not run because the complete live environment is unavailable and the Docker builder remains incompatible.
- `residual_risks`: Host unit/static evidence may miss browser-cookie, live REST, or container integration defects.
- `owners`: Container Runtime Owner for the compatible builder; Migration Verification Owner for browser smoke.
- `triggers`: Separately reviewed Node-compatible builder plus authorized live Postgres/pgvector, migrated schema, backend/frontend, and seeded credentials; before release relying on these flows.
- `blockers`: No blocker to this documented-deferral acceptance; the recorded browser/live-environment and builder condition remains.
- `accepted_commit`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `pushed_ref`: At the review timestamp, local `main` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` was three commits ahead of the locally tracked `origin/main` at `c32bb88ce21eabde2141712499713e3c9569b4cd`. The reviewer did not query the remote or push during the review.
- `verification_performed`: The reviewer recorded focused backend `52 passed`, `29 warnings`, `8.04s` and complete backend `130 passed`, `219 warnings`, `16.16s`; the warnings were existing Pydantic v2 and `datetime.utcnow()` deprecations. Seven existing changed Python files compiled in memory with exit `0`. Alembic `heads` returned `0005_material_owner (head)`; offline `upgrade head --sql` exited `0`, produced `372` lines with SHA-256 `b3556584cf1f1ee6aab78f70dab47afcab257cb05df04d2a98323f29cc6c7674`, and contained `owner_id`, `ON DELETE SET NULL` FK, and index DDL. Frontend lint exited `0`; Vitest reported `10` files and `56 passed` in `9.47s`; the out-of-tree production build exited `0` with `135` modules in `6.59s` and retained the stated stale-browser-data and `850.25 kB` chunk warnings. The reviewer recorded `42` Markdown files, `0` local links, `10` external links, and `0` broken local links; the route/vendor/legacy/router/Phase 8-9 scans stated in the artifact; exact parent-chain and three-commit checks; clean worktree/index before and after; and aggregate/worktree/index diff checks exiting `0`.
- `verification_not_performed`: Docker build/runtime, browser smoke, live PostgreSQL upgrade/current/FK inspection or live `ON DELETE SET NULL` exercise, real DeepSeek, external GCP/key evidence, remote-server query, and push were not performed; `DEEPSEEK_API_KEY=NOT SET`.
- `artifact`: `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`
- `artifact_status`: `named reviewer artifact preserved; documented-deferral acceptance transcribed`

### P7-MR-2EC4192-20260713-01

- `verdict_slice_id`: `P7-MR-2EC4192-20260713-01`
- `review_id`: `MR-2EC4192-20260713-01`
- `phase_slice`: `Phase 7 closeout`
- `reviewer`: `Migration Reviewer Agent`
- `review_date`: `2026-07-13T21:44:01.9648007+08:00`
- `timezone`: `China Standard Time — (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi`
- `base_commit`: `c32bb88ce21eabde2141712499713e3c9569b4cd`
- `reviewed_HEAD`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `reviewed_commits`: `23831f2545ec715418348f1dc5e7aa711e339b60` — Fix material ownership authorization; `e902205f198540cc7a3abcc6b802ef285f45554f` — Harden DeepSeek thinking tool calls; `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` — Record corrective migration governance.
- `reviewed_commit`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `verdict`: `pending`
- `conditions`: Browser smoke may later be carried as a documented deferral; it is not independently the acceptance blocker. Existing ownerless Materials rows remain safely quarantined, so the absent ownership disposition is not an active IDOR, but it still blocks Phase 7 acceptance.
- `residual_risks`: Legacy Materials ownership has no approved final disposition; Alembic head `0005_material_owner` lacks live PostgreSQL constraint/behavior evidence; and the Node-incompatible builder prevents the reviewed compatible container path needed for later live/browser evidence.
- `owners`: Security Owner and Backend Owner for legacy-owner mapping/disposition; Database Migration Owner for live `0005`/FK/index/`SET NULL` evidence; Container Runtime Owner for the reviewed Node-compatible builder; Migration Verification Owner for any later browser smoke.
- `triggers`: Legacy-owner disposition is required before Phase 7 acceptance or any multi-user/production use. The new Alembic head triggered live upgrade/current, FK/index inspection, owning-user deletion with `owner_id=NULL`, and authenticated 404 retrieval evidence. The builder requires a separately reviewed Node-compatible candidate; browser smoke follows that correction and the complete authorized environment.
- `blockers`: Security Owner + Backend Owner legacy-owner mapping/disposition approval is absent; Database Migration Owner live `0005`/FK/index/`SET NULL` evidence is absent; Container Runtime Owner has not supplied the reviewed Node-compatible builder.
- `pushed_ref`: At the review timestamp, local `main` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` was three commits ahead of the locally tracked `origin/main` at `c32bb88ce21eabde2141712499713e3c9569b4cd`. The reviewer did not query the remote or push during the review.
- `verification_performed`: The reviewer recorded focused backend `52 passed`, `29 warnings`, `8.04s` and complete backend `130 passed`, `219 warnings`, `16.16s`; the warnings were existing Pydantic v2 and `datetime.utcnow()` deprecations. Seven existing changed Python files compiled in memory with exit `0`. Alembic `heads` returned `0005_material_owner (head)`; offline `upgrade head --sql` exited `0`, produced `372` lines with SHA-256 `b3556584cf1f1ee6aab78f70dab47afcab257cb05df04d2a98323f29cc6c7674`, and contained `owner_id`, `ON DELETE SET NULL` FK, and index DDL. Frontend lint exited `0`; Vitest reported `10` files and `56 passed` in `9.47s`; the out-of-tree production build exited `0` with `135` modules in `6.59s` and retained the stated stale-browser-data and `850.25 kB` chunk warnings. The reviewer recorded `42` Markdown files, `0` local links, `10` external links, and `0` broken local links; the route/vendor/legacy/router/Phase 8-9 scans stated in the artifact; exact parent-chain and three-commit checks; clean worktree/index before and after; and aggregate/worktree/index diff checks exiting `0`.
- `verification_not_performed`: Docker build/runtime, browser smoke, live PostgreSQL upgrade/current/FK inspection or live `ON DELETE SET NULL` exercise, real DeepSeek, external GCP/key evidence, remote-server query, and push were not performed; `DEEPSEEK_API_KEY=NOT SET`.
- `artifact`: `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`
- `artifact_status`: `named reviewer artifact preserved; pending verdict transcribed without an accepted_commit`

### P8-MR-2EC4192-20260713-01

- `verdict_slice_id`: `P8-MR-2EC4192-20260713-01`
- `review_id`: `MR-2EC4192-20260713-01`
- `phase_slice`: `Phase 8 gate`
- `reviewer`: `Migration Reviewer Agent`
- `review_date`: `2026-07-13T21:44:01.9648007+08:00`
- `timezone`: `China Standard Time — (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi`
- `base_commit`: `c32bb88ce21eabde2141712499713e3c9569b4cd`
- `reviewed_HEAD`: `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `reviewed_commits`: `23831f2545ec715418348f1dc5e7aa711e339b60` — Fix material ownership authorization; `e902205f198540cc7a3abcc6b802ef285f45554f` — Harden DeepSeek thinking tool calls; `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` — Record corrective migration governance.
- `verdict`: `pending`
- `state`: `closed`
- `conditions`: No Phase 8 planning or implementation artifact exists.
- `residual_risks`: Phase 8 has no reviewed planning package and cannot be treated as started or complete.
- `owners`: No separate Phase 8 gate owner was stated in the artifact; the named owners and triggers on the prerequisite phase conditions remain responsible.
- `triggers`: Phase 7 must first receive a named `accepted` or `accepted_with_documented_deferral` ledger verdict with exact owners/triggers, all canonical dependencies must be acceptable, and the Phase 8 planning package must itself be reviewed before implementation.
- `blockers`: Phase 7 remains pending; all canonical dependencies must be acceptable; and no reviewed Phase 8 planning package exists.
- `pushed_ref`: At the review timestamp, local `main` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236` was three commits ahead of the locally tracked `origin/main` at `c32bb88ce21eabde2141712499713e3c9569b4cd`. The reviewer did not query the remote or push during the review.
- `verification_performed`: The reviewer recorded focused backend `52 passed`, `29 warnings`, `8.04s` and complete backend `130 passed`, `219 warnings`, `16.16s`; the warnings were existing Pydantic v2 and `datetime.utcnow()` deprecations. Seven existing changed Python files compiled in memory with exit `0`. Alembic `heads` returned `0005_material_owner (head)`; offline `upgrade head --sql` exited `0`, produced `372` lines with SHA-256 `b3556584cf1f1ee6aab78f70dab47afcab257cb05df04d2a98323f29cc6c7674`, and contained `owner_id`, `ON DELETE SET NULL` FK, and index DDL. Frontend lint exited `0`; Vitest reported `10` files and `56 passed` in `9.47s`; the out-of-tree production build exited `0` with `135` modules in `6.59s` and retained the stated stale-browser-data and `850.25 kB` chunk warnings. The reviewer recorded `42` Markdown files, `0` local links, `10` external links, and `0` broken local links; the route/vendor/legacy/router/Phase 8-9 scans stated in the artifact; exact parent-chain and three-commit checks; clean worktree/index before and after; and aggregate/worktree/index diff checks exiting `0`.
- `verification_not_performed`: Docker build/runtime, browser smoke, live PostgreSQL upgrade/current/FK inspection or live `ON DELETE SET NULL` exercise, real DeepSeek, external GCP/key evidence, remote-server query, and push were not performed; `DEEPSEEK_API_KEY=NOT SET`.
- `artifact`: `docs/migration/review-artifacts/MR-2EC4192-20260713-01.md`
- `artifact_status`: `named reviewer artifact preserved; pending closed-gate verdict transcribed without a slice-specific reviewed_commit or accepted_commit`

## Evidence publication records

### GOV-EVIDENCE-PUBLICATION-9707C21-01

- `record_id`: `GOV-EVIDENCE-PUBLICATION-9707C21-01`
- `record_type`: `evidence publication and post-review materialization/transport mapping; not a review event or verdict`
- `recorded_at`: `2026-07-15T19:48:47.3239864+08:00`
- `publisher`: `Documentation/Governance Evidence Publisher; not the reviewer`
- `source_review_event`: `MR-2EC4192-20260713-01`
- `artifacts_published`:
  - `IGTR-2EC4192-20260714-01`: `timestamp=2026-07-14T10:06:43.4499419+08:00`; `source_verdict=rejected`; `manifest=957d033b5cbc03d14a54665f6c9d38fdbd728d7c53503a96cf14a374428c7e64`; `repo_path=docs/migration/review-artifacts/IGTR-2EC4192-20260714-01.md`; `bytes=8061`; `SHA-256=df7f54e5e0b6243cf3826e474d3ea44b6166db4fe102731320a7eecdaf130156`; `raw_blob=4f8de8baa8a19d0d171369b95996ecedb54ba5ec`
  - `IGTR-2EC4192-20260714-02`: `timestamp=2026-07-14T11:16:23.4439511+08:00`; `source_verdict=accepted`; `manifest=dbe04423848e1d1487b5a1e96f9d5a63bae59d889274d38dc7915e9e37c13143`; `repo_path=docs/migration/review-artifacts/IGTR-2EC4192-20260714-02.md`; `bytes=10215`; `SHA-256=4cd79fa0c5bb7556067885777c6f4e54981fd28120f08161ef4ad345f6faa3f3`; `raw_blob=d9223afeaf950d9b095d03abb5404ce9477aa870`
  - `IGTR-2EC4192-20260714-03`: `timestamp=2026-07-14T23:48:47.9552051+08:00`; `source_verdict=accepted`; `manifest=8799d01f8553d664fbea701175124f8883b5655bfca4268a65b46993ee0e86c2`; `repo_path=docs/migration/review-artifacts/IGTR-2EC4192-20260714-03.md`; `bytes=13691`; `SHA-256=b18b5c53d2f5a4e52a6388719bb1617e0c69ab64835a691959b91195880c0740`; `raw_blob=a3ba74a7f3102b680d8b8da7155db816cecdd373`
- `review_chain`: `IGTR-2EC4192-20260714-01` rejects only the old manifest `957d033b5cbc03d14a54665f6c9d38fdbd728d7c53503a96cf14a374428c7e64`; `IGTR-2EC4192-20260714-02` accepts only the exact 16-file manifest `dbe04423848e1d1487b5a1e96f9d5a63bae59d889274d38dc7915e9e37c13143`; `IGTR-2EC4192-20260714-03` accepts only the exact 17-file manifest `8799d01f8553d664fbea701175124f8883b5655bfca4268a65b46993ee0e86c2`. The three review events are independent; none amends, overrides, or rewrites another.
- `materialization_mapping`: The exact 17-file manifest `8799d01f8553d664fbea701175124f8883b5655bfca4268a65b46993ee0e86c2` accepted by `IGTR-2EC4192-20260714-03` subsequently materialized without byte drift as ordinary commit `9707c2144e1ef60cd4538c71035e03ab76d21b4d`, whose parent is `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`; 17/17 committed blobs match the reviewed raw candidate. This is a post-review repository fact, not a Reviewer-provided `accepted_commit`.
- `subset_note`: The 16 entries in `IGTR-2EC4192-20260714-02` are byte-identical to the corresponding entries in `IGTR-2EC4192-20260714-03`, but the 16-file candidate did not separately materialize as a commit; manifest `dbe04423848e1d1487b5a1e96f9d5a63bae59d889274d38dc7915e9e37c13143` is not mapped to an `accepted_commit`.
- `rejection_note`: `IGTR-2EC4192-20260714-01` remains rejected historical evidence and has no materialized or accepted commit.
- `transport_observation`: `c32bb88..9707c21  main -> main` was an ordinary, non-force fast-forward push. After the push, local `HEAD`/`main` and locally tracked `origin/main` were all `9707c2144e1ef60cd4538c71035e03ab76d21b4d`, with `ahead 0 / behind 0`. This is transport evidence only, does not expand the Reviewer verdict, and makes no claim of an independent remote-server query beyond the push.
- `phase_verdict_effect`: `none`; this record does not create, modify, or supersede any Reviewer verdict and does not populate any Reviewer `accepted_commit`. Overall remediation remains `accepted` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`; Phase 3 remains `pending`; Phase 4 remains `pending`; Phases 5 and 6 remain `accepted_with_documented_deferral` at `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`; Phase 7 remains `pending`; Phase 8 remains `pending/closed`; the three Phase 7 blockers remain; Phase 9 is not authorized.
- `artifact_status`: The three raw artifacts are published byte-for-byte under `-text !eol whitespace=cr-at-eol`; this mapping record is publisher-authored metadata, not reviewer-authored content.

## Owner decision records

### P7-MATERIALS-DISPOSITION-20260715-01

- `record_id`: `P7-MATERIALS-DISPOSITION-20260715-01`
- `record_type`: owner decision and post-review blocker evidence; not a review event or verdict
- `decided_at`: `2026-07-15T21:08:18.1658360+08:00`
- `decision_owners`: Project Owner acting as Security Owner and Backend Owner
- `approval_source`: explicit Project Owner confirmation to the Project Steward on 2026-07-15
- `decision`: Quarantine is the final disposition for this migration / Phase 7 scope for every historical Material row whose `owner_id IS NULL`; no database mutation or deletion is required.
- `prohibited_actions`: Do not automatically backfill, infer, fabricate, or arbitrarily assign an owner. Do not expose, list, retrieve, or unquarantine these rows through authenticated application paths.
- `future_mapping_gate`: A future ownership mapping is allowed only when authoritative provenance exists and a separately authorized, independently reviewed migration preserves that evidence.
- `future_deletion_gate`: Future deletion requires separate explicit authorization.
- `runtime_effect`: none; this docs-only record did not enumerate, modify, map, delete, or unquarantine any rows
- `evidence`: `docs/migration/decisions/ADR-0002-ownerless-material-disposition.md`
- `historical_review_effect`: none; the three blockers recorded by `MR-2EC4192-20260713-01` remain its faithful historical finding
- `current_blocker_effect`: supplies the owner-disposition evidence for evaluation by the next named Phase 7 Reviewer; does not itself accept Phase 7
- `remaining_blockers`: live PostgreSQL `0005` upgrade/current, FK/index, actual `ON DELETE SET NULL`, and authenticated 404 evidence from Database Migration Owner; reviewed Node-compatible builder from Container Runtime Owner
- `phase_verdict_effect`: none; Phase 7 remains pending and Phase 8 remains closed
