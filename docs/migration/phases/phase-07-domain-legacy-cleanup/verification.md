# Phase 07 Verification - Domain and Legacy Cleanup

## Current Reviewer Transcription - 2026-07-13

Review event `MR-2EC4192-20260713-01` records Phase 7 as `pending` at reviewed commit `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`, with no `accepted_commit`. Three blockers remain: Security Owner + Backend Owner legacy-owner mapping/disposition approval; Database Migration Owner live `0005` upgrade/current, FK/index inspection and actual `ON DELETE SET NULL` evidence; and a reviewed Node-compatible builder from Container Runtime Owner. Ownerless rows remain safely quarantined and are not an active IDOR, but that does not clear the ownership blocker. Browser smoke may later be carried as a documented deferral and is not independently the acceptance blocker. This transcription did not run live PostgreSQL, Docker, browser, or other tests and does not make Phase 7 complete.

## Post-review Owner Decision - 2026-07-15

ADR-0002 records the Project Owner, acting as Security Owner and Backend Owner, approving continued quarantine of every historical Material row whose `owner_id IS NULL` as the final disposition for this migration / Phase 7 scope. It supplies the previously missing joint owner decision for evaluation by a future named Phase 7 re-review. It does not amend `MR-2EC4192-20260713-01`, create a Phase 7 verdict or `accepted_commit`, or make Phase 7 complete. Phase 7 remains `pending`.

The two technical blockers remain:

1. Database Migration Owner live PostgreSQL `0005` upgrade/current, FK/index, actual `ON DELETE SET NULL`, and authenticated 404 evidence.
2. Container Runtime Owner reviewed Node-compatible builder.

No runtime, migration, database, Docker, browser, or external-system action occurred. This docs-only record did not enumerate, modify, map, delete, or unquarantine any Material rows. Phase 8 remains `pending` / `closed`.

### Docs-only candidate verification

All commands in this subsection were run from the repository root unless a working directory is stated. They were read-only and used no network, database, Docker, browser, runtime, migration, or test action.

#### Git preconditions, refs, scope, and index

Commands:

```powershell
git rev-parse HEAD
git rev-parse main
git rev-parse refs/remotes/origin/main
git rev-list --left-right --count main...refs/remotes/origin/main
git status --porcelain=v1 --untracked-files=all
git diff --cached --name-only
```

Results:

- Before editing, the worktree and index were clean; `HEAD`, `main`, and locally tracked `origin/main` all equalled `0f86d9cffdd656d5d4463a0577395e1d82d6bdfa`; ahead/behind was `0/0`.
- After editing, the index remained empty. The candidate contained exactly seven unstaged modified Markdown files and one untracked Markdown file: `MIGRATION_PHASES.md`, `docs/migration/README.md`, `docs/migration/REVIEW_LEDGER.md`, `docs/migration/decisions/ADR-0002-ownerless-material-disposition.md`, and the Phase 7 `checklist.md`, `phase-plan.md`, `phase-report.md`, and `verification.md`.
- There were no non-Markdown changes. No file was staged, committed, or pushed.

#### Ledger and historical-section preservation

Commands:

```powershell
git cat-file blob HEAD:docs/migration/REVIEW_LEDGER.md
git show HEAD:docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md
git show HEAD:docs/migration/phases/phase-07-domain-legacy-cleanup/phase-plan.md
git show HEAD:docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md
git show HEAD:docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md
```

The ledger blob was captured as bytes and compared with the same-length worktree prefix. Each historical H2 section was extracted through the next H2 and compared with its `HEAD` version.

Results:

- The original ledger prefix was byte-for-byte unchanged: `45,680` bytes, SHA-256 `2712ec2607508634355ea1e9326d19651af7584945f1cee86b04fc2945e257fc`. The new H2 starts immediately after the original EOF.
- The appended record contained all 15 required fields and no exact `review_id`, `verdict`, or `accepted_commit` field. Its `decided_at` value matched RFC 3339 with `+08:00`.
- The four `Current Reviewer Transcription - 2026-07-13` sections were unchanged. Their SHA-256 values were `be31f9ea21ca320f68124cf1a144027d674bf229d3c827026792d53da4dc28d3` (checklist), `914336eb553989cce61452ebb0055c45558ef0fd346e3762ed89ecf6a8398cf4` (plan), `4da4b7c081604418d3ef9b05888ccd03848bb46385153b9dc89f34dd14e662e1` (report), and `8f49193b1ead843b6caf86238e518c780e4ffab6e326153934469b2690594ae1` (verification).

#### Status-content, whitespace, formatting, and links

Commands:

```powershell
rg -n -C 1 "three blockers|三个 blocker|三-blocker|ADR-0002|two technical blockers|两个 technical blocker|unresolved technical blockers|Phase 7 remains.*pending|Phase 8 remains.*(?:pending|closed)|Browser smoke.*documented deferral" MIGRATION_PHASES.md docs/migration/README.md
git diff --check
```

```powershell
# working directory: frontend
npm run format:check
```

```powershell
& '.\frontend\node_modules\.bin\prettier.cmd' --config '.\frontend\.prettierrc' --check 'MIGRATION_PHASES.md' 'docs\migration\README.md' 'docs\migration\REVIEW_LEDGER.md' 'docs\migration\decisions\ADR-0002-ownerless-material-disposition.md' 'docs\migration\phases\phase-07-domain-legacy-cleanup\checklist.md' 'docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md' 'docs\migration\phases\phase-07-domain-legacy-cleanup\phase-report.md' 'docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md'
```

```powershell
$markdownFiles = @(git ls-files --cached --others --exclude-standard -- '*.md')
# Inline PowerShell validation classified Markdown link targets, resolved every
# local path, and checked any local :line target against the target line count.
```

Results:

- Required-clause assertions passed for both current summaries, all four post-review sections, and ADR-0002. The strict false-state scan found zero affirmative acceptance/completion/opening claims. The summaries consistently retain the historical three blockers, add the later owner decision, and identify the two unresolved technical blockers.
- `git diff --check` exited `0`.
- The repository-established `npm run format:check` exited `1` on 10 pre-existing frontend JS/JSX formatting warnings. Its configured glob covers only `frontend/src/**/*.{js,jsx,json,css,md}` and does not cover these eight Markdown files. No rewrite command was used.
- The candidate-specific Prettier 3.6.2 check exited `1`, warning on `MIGRATION_PHASES.md` and this Phase 7 `phase-report.md`; read-only comparison confirmed both `HEAD` versions already differ from the same formatter. The other six candidate Markdown files passed. No rewrite command was used.
- Link validation examined 47 Markdown files: 30 local links, 13 external links, and zero broken local links. It did not query external URLs.
- All eight candidate files were UTF-8 without BOM, LF-only, and ended with LF.

## Governance Reconciliation - 2026-07-10

- Current verdict: `pending`.
- `fa97afd2de0fd9dea66fe86a519f440285717552` is a pushed candidate only; it is not an accepted closeout or accepted commit.
- Browser smoke status: `not run`, not passed.
- Exact blockers: historical Docker Desktop Linux engine unavailability plus no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded credentials; current Dockerfile Node 18 builder incompatibility with the locked Vite 7.1.9 / React Router 7.9.3 engine requirements.
- Owners: Container Runtime Owner for the build correction; Migration Verification Owner for browser smoke.
- Triggers: a separately reviewed compatible runtime candidate, then the complete authorized environment; run before a release relying on these flows or carry as an explicit later reviewer condition.
- Missing browser smoke is not automatically a blocker. A named reviewer may record `accepted` or `accepted_with_documented_deferral`; the latter requires explicit conditions, owner, and trigger and does not require `conditions=none`.
- Phase 8 planning must remain closed until Phase 7 receives a named `accepted` or `accepted_with_documented_deferral` verdict with explicit conditions, owners, and triggers, and all canonical dependencies are in acceptable states. Phase 8 implementation remains prohibited until its planning package is reviewed.
- Materials ownership is a P1 remediation, not reviewer-attention-only. Pre-existing rows remain ownerless without arbitrary backfill or deletion and are quarantined from authenticated retrieval. Security Owner + Backend Owner must approve verified legacy-owner mapping/disposition before Phase 7 acceptance or any multi-user/production use; unquarantine remains blocked until then. Legacy `vector_sync` HTTP 501 shells are quarantined deferred compatibility surfaces rather than parity; Phase 9 RAG Replacement Owner owns any future replacement.
- Dormant legacy/security cleanup removed `backend_py/app/api/test.py` only after repository-wide scans found no import, mount, explicit path reference, or router auto-discovery. It was an unauthenticated duplicate that could have revived the Materials IDOR if mounted, but no current reachability is claimed. Post-deletion prefix scans leave only `app.api.materials`.

The historical commands/results below remain execution evidence. This corrective remediation adds no Docker, browser, real DeepSeek, or live-Postgres result.

Round 0/1 implementation status: this document defines the verification contract, records initial planning scans, and records Round 0/1 implementation verification. A requested deploy/nginx/docker naming cleanup pass was verified on 2026-07-02. Migration placeholder route/tool cleanup was verified on 2026-07-05. Frontend personal-route cleanup was verified on 2026-07-06. Unmounted frontend tenant/org/invite placeholder cleanup was verified on 2026-07-07. Frontend organization-sharing UI residue cleanup was verified on 2026-07-07. Frontend AuthContext tenant/org state cleanup was verified on 2026-07-08. Frontend API request-normalization cleanup was verified on 2026-07-08. Obsolete current docs/scripts cleanup was verified on 2026-07-09. It does not mark Phase 7 complete; current verdict remains pending. Historical Phase 7 execution relied on the Phase 6 accepted-with-deferral handoff; `P6-DEFIREBASE-CORRECTION-01` later corrected its audit status, and `MR-2EC4192-20260713-01` now supplies the current named Phase 6 accepted-with-deferral re-review. The historical execution evidence remains unchanged, and none of those Phase 6 records completes Phase 7.

## 2026-07-13 Dormant Materials Router Verification

Before deletion, the tracked-tree search excluded the dormant file itself and found no import or mount reference:

```powershell
git grep -n -E 'app\.api\.test|api\.test|include_router.*test|test.*include_router' HEAD -- '*.py' ':(exclude)backend_py/app/api/test.py'
```

Result: no matches (`git grep` exit `1`). A repository-wide scan also found no `import_module`, `__import__`, `walk_packages`, `iter_modules`, or entry-point router discovery. `backend_py/main.py` imported and mounted `app.api.materials` only. This establishes dormancy, not current reachability.

After deletion, the application-router prefix scan returned exactly one definition:

```powershell
rg -n 'APIRouter.*materials' backend_py/app -g '*.py'
```

```text
backend_py/app\api\materials.py:14:router = APIRouter(prefix="/materials", tags=["materials"])
```

The final Python import/mount scan returned `NO_PYTHON_IMPORT_OR_MOUNT_MATCHES`, and the dynamic-discovery scan returned `NO_DYNAMIC_ROUTER_DISCOVERY_PRIMITIVES`. The focused auth/Materials/DeepSeek/provider command passed `50` tests, and the full backend command passed `128` tests. Python compilation of the changed backend, smoke, test, and migration files exited `0`.

Transcription note (review event `MR-2EC4192-20260713-01`): the `50` focused / `128` backend results above belong to an earlier corrective run and remain unchanged as historical evidence. At the exact reviewed HEAD `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`, the Reviewer recorded focused backend `52 passed` and complete backend `130 passed`. This documentation transcription did not rerun either test command and does not replace the earlier result.

## Verification Principles

- Record exact commands and outputs after each implementation round.
- Distinguish active-surface cleanup from explicitly allowlisted historical migration records and security/negative assertion tests.
- Do not use this document as code review.
- Do not mark Phase 7 complete until implementation evidence exists and a reviewer accepts the closeout.
- Gate Phase 7 implementation if Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` do not record Migration Reviewer closeout acceptance.
- Do not claim browser smoke unless it was actually run against a live backend/Postgres/frontend environment with seeded credentials.
- Preserve Phase 6 browser-smoke deferral unless Phase 7 execution actually unblocks and runs it.
- Active surfaces are runtime source, config, deploy scripts, current README/user docs, and active tests.
- Historical migration records under `docs/migration/phases/**` and intentional security/negative assertion tests may retain forbidden legacy strings only with an explicit allowlist recorded here and in `phase-report.md`.
- The allowlist must not hide active runtime/config/deploy/current-doc residue.

## Required Context For Phase 7 Verification

- `MIGRATION_PHASES.md`
- `docs/PERSONAL_USE_BOUNDARY.md`
- `docs/migration/README.md`
- `docs/migration/decisions/ADR-0001-auth-strategy.md`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-plan.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`

Phase 6 status basis:

- Phase 6 closeout is recorded as accepted by Migration Reviewer in Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
- Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable; this document must not convert that deferral into a run result.

## Docs-Only Planning Consistency Repair - 2026-07-02

Scope: documentation-only repair for Phase 6 closeout status and Phase 7 required-context consistency. No browser smoke, backend tests, frontend tests, package commands, env changes, runtime code edits, or migration implementation changes were run or made.

### Phase 6 Stale Closeout Status Scan

Command:

```powershell
rg -n -i 'phase 6.*(pending|awaiting|under review|reviewer review|closeout remain open|closeout remains open|still pending)|pending.*phase 6|awaiting.*phase 6|reviewer closeout remain open|phase 6 closeout is pending|phase 6 closeout.*pending' docs\migration\phases\phase-06-frontend-defirebase docs\migration\phases\phase-07-domain-legacy-cleanup -g '!docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md'
```

Result:

```text
No stdout. `rg` exited 1.
```

### Accepted Phase 6 Status And Browser-Smoke Deferral Scan

Command:

```powershell
rg -n -i 'Phase 6 closeout.*accepted|accepted.*Phase 6 closeout|browser smoke remains deferred|browser smoke deferred|27679f8|Phase 6 `checklist.md`' docs\migration\phases\phase-06-frontend-defirebase docs\migration\phases\phase-07-domain-legacy-cleanup
```

Result:

```text
docs\migration\phases\phase-06-frontend-defirebase\checklist.md:3:Round 0/1/2/3/4/5/6 implementation status: Round 0 inventory, Round 1 cookie-session/AuthContext foundation, Round 0/1 review repairs, Round 2 core framework REST wiring, Round 2 review repairs, Round 3 Library plus publish/unpublish REST wiring, Round 4 Admin users REST wiring, Round 5 artefact child-resource UI wiring, and Round 6 Firebase SDK removal/Bearer closeout are implemented with static scan, lint, unit-test, backend-test, and build verification. Phase 6 closeout was accepted by Migration Reviewer with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable. Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\checklist.md:7:- [x] Phase 6 closeout accepted by Migration Reviewer.
docs\migration\phases\phase-06-frontend-defirebase\checklist.md:8:- [x] Acceptance recorded with browser smoke deferred due to unavailable Docker/Postgres/seeded local environment.
docs\migration\phases\phase-06-frontend-defirebase\checklist.md:9:- [x] Round 6 closeout commit recorded: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\checklist.md:208:- [x] Phase 6 closeout acceptance is recorded only after Migration Reviewer accepted Round 6.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:33:- Phase 6 closeout is recorded as accepted by Migration Reviewer in Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:34:- Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:38:- Browser smoke remains deferred unless a later executor actually runs it.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:40:- If Phase 6 closeout docs do not record accepted status in a future checkout, Phase 7 implementation is gated until that documentation contradiction is corrected.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:42:For Phase 7 implementation, Phase 6 `checklist.md` is required context alongside Phase 6 `phase-report.md` and `verification.md`; do not treat the report/verification pair alone as sufficient.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:418:- Before implementation, verify Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance, browser smoke deferred due unavailable Docker/Postgres/seeded local environment, and Round 6 closeout commit `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:419:- If Phase 6 docs do not record accepted closeout status, stop Phase 7 implementation and correct Phase 6 closeout docs first.
docs\migration\phases\phase-07-domain-legacy-cleanup\checklist.md:11:- [ ] Read Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
docs\migration\phases\phase-07-domain-legacy-cleanup\checklist.md:12:- [ ] Confirm Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance before starting or merging Phase 7 implementation.
docs\migration\phases\phase-07-domain-legacy-cleanup\checklist.md:13:- [ ] Gate Phase 7 implementation if Phase 6 closeout docs do not record accepted status.
docs\migration\phases\phase-07-domain-legacy-cleanup\checklist.md:14:- [ ] Confirm Phase 6 browser smoke remains deferred unless it has actually been run in the current environment.
docs\migration\phases\phase-06-frontend-defirebase\phase-plan.md:3:Historical planning status: documentation only. This plan did not implement backend or frontend code and did not mark Phase 6 complete when written; the current Phase 6 closeout status is accepted by Migration Reviewer after Round 6, with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-report.md:12:- Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-report.md:13:- Phase 6 Round 6 closeout commit is `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-report.md:18:- If Phase 6 closeout docs do not record accepted status in a future checkout, Phase 7 implementation is gated until that documentation contradiction is corrected.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-report.md:31:For Phase 7 implementation, Phase 6 `checklist.md` remains required context alongside Phase 6 `phase-report.md` and `verification.md`; the report/verification pair alone is not sufficient for the Phase 6 gate.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:3:Round 0/1/2/3/4/5/6 implementation status: Round 0 inventory, Round 1 cookie-session/AuthContext foundation, Round 2 core framework REST wiring, Round 2 review repairs, Round 3 Library plus publish/unpublish REST wiring, Round 4 Admin users REST wiring, Round 5 artefact child-resource UI wiring, and Round 6 Firebase SDK removal/Bearer closeout have been implemented with static scan, lint, unit-test, backend-test, and build verification. Phase 6 closeout was accepted by Migration Reviewer with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable. Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:7:This report is now the Round 0/1/2/3/4/5/6 implementation and review-repair record. Earlier planning-only wording has been superseded; Phase 6 closeout acceptance is recorded here after Migration Reviewer accepted Round 6.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:14:- Phase 6 closeout accepted by Migration Reviewer.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:15:- Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable; this report does not claim browser smoke was run.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:16:- Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:23:- Phase 7 may use the accepted Phase 6 closeout status recorded in this report, `checklist.md`, and `verification.md`.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:27:This historical repair fixed only the remaining Round 2 review findings. Rounds 3, 4, 5, and 6 are now implemented, and Migration Reviewer accepted the Phase 6 closeout after Round 6.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:240:Round 4 implemented Admin users REST wiring only. Historical Round 4 handoff did not complete Phase 6 because Round 5 and Round 6 had not run yet; the current Phase 6 closeout status is accepted by Migration Reviewer after Round 6, with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:291:Round 5 implemented artefact child-resource UI wiring only. Historical Round 5 handoff did not complete Phase 6 because Round 6 and Migration Reviewer acceptance had not happened yet; the current Phase 6 closeout status is accepted by Migration Reviewer after Round 6, with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:344:Round 6 removed the frontend Firebase SDK runtime dependency, isolated remaining Firebase-dependent Phase 7 residue, removed frontend/container Firebase env hooks, and closed the backend Bearer compatibility gate. Migration Reviewer accepted the Phase 6 closeout with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable. Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:416:- Phase 6 closeout was accepted by Migration Reviewer after Round 6.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:452:- The full Phase 6 closeout state is now updated: Migration Reviewer accepted Phase 6 after Round 6, with browser smoke deferred for environment reasons.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:548:- Phase 6 closeout is accepted; Phase 7 semantic deferrals continue after Round 6.
docs\migration\phases\phase-06-frontend-defirebase\phase-report.md:561:Phase 6 closeout is accepted by Migration Reviewer. This report records Round 0/1/2/3/4/5/6 implementation and current review repairs. Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable, and Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\verification.md:3:Round 0/1/2/3/4/5/6 implementation status: Round 0 inventory, Round 1 cookie-session/AuthContext foundation, Round 0/1 reviewer repairs, Round 2 core framework REST wiring, Round 2 review repairs, Round 3 Library plus publish/unpublish REST wiring, Round 4 Admin users REST wiring, Round 5 artefact child-resource UI wiring, and Round 6 Firebase SDK removal/Bearer closeout have static scan, lint, unit-test, backend-test, and build verification. Phase 6 closeout was accepted by Migration Reviewer with browser smoke deferred because Docker/Postgres/seeded local environment was unavailable. Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\verification.md:10:- Phase 6 closeout acceptance is recorded after Migration Reviewer accepted Round 6.
docs\migration\phases\phase-06-frontend-defirebase\verification.md:11:- Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable; this verification record does not claim browser smoke was run.
docs\migration\phases\phase-06-frontend-defirebase\verification.md:12:- Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-06-frontend-defirebase\verification.md:1484:Status: Phase 6 closeout accepted by Migration Reviewer after Round 6. Browser smoke could not run because the local Docker/Postgres service is unavailable; do not claim browser-smoke coverage from this evidence.
docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md:11:- Gate Phase 7 implementation if Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` do not record Migration Reviewer closeout acceptance.
docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md:33:- Phase 6 closeout is recorded as accepted by Migration Reviewer in Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md:34:- Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md:35:- Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable; this document must not convert that deferral into a run result.
```

### Phase 7 Required Context Consistency Scan

Command:

```powershell
rg -n 'docs/migration/phases/phase-06-frontend-defirebase/checklist.md|Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`|Read Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`' docs\migration\phases\phase-07-domain-legacy-cleanup
```

Result:

```text
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:27:- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:33:- Phase 6 closeout is recorded as accepted by Migration Reviewer in Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:409:- docs/migration/phases/phase-06-frontend-defirebase/checklist.md
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-plan.md:418:- Before implementation, verify Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance, browser smoke deferred due unavailable Docker/Postgres/seeded local environment, and Round 6 closeout commit `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
docs\migration\phases\phase-07-domain-legacy-cleanup\checklist.md:11:- [ ] Read Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
docs\migration\phases\phase-07-domain-legacy-cleanup\checklist.md:12:- [ ] Confirm Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance before starting or merging Phase 7 implementation.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-report.md:12:- Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance.
docs\migration\phases\phase-07-domain-legacy-cleanup\phase-report.md:26:- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md:11:- Gate Phase 7 implementation if Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` do not record Migration Reviewer closeout acceptance.
docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md:24:- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
docs\migration\phases\phase-07-domain-legacy-cleanup\verification.md:33:- Phase 6 closeout is recorded as accepted by Migration Reviewer in Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
```

### Whitespace Check

Command:

```powershell
git diff --check
```

Result:

```text
No stdout. Command exited 0.
```

## Allowlist Record

Round 0/1 allowlist entries are recorded here and mirrored in `phase-report.md`:

- `MIGRATION_PHASES.md`: retains legacy strings such as `valorie.ai`, `framework-builder-55896`, `webmaster@valorie`, `UNSW`, `ad.unsw`, tenant, invite, and migration terms because it is the canonical migration plan and names the cleanup targets and acceptance scans. It is not active runtime/config/deploy/current user documentation.
- `docs/migration/phases/**`: retains historical phase evidence and current phase verification records that quote legacy strings, commands, and outputs. These records must remain auditable and are not active runtime/config/deploy/current user documentation.
- `docs/migration/README.md` and `docs/migration/decisions/ADR-0001-auth-strategy.md`: retain Firebase Auth / Firebase ID Token references only as migration decision evidence explaining why backend JWT is the accepted auth route. ADR-0001 was updated in the docs/scripts cleanup to avoid stale future-tense wording about frontend Firebase removal.
- `docs/skills/migration-reviewer/SKILL.md` and `docs/skills/migration-phase-planner/SKILL.md`: retain legacy terms only as migration-tooling scan/review prompts so future phase agents can find residue; they are not app setup, runtime, config, deploy, or user workflow documentation.
- `backend_py/tests/test_main.py`: retains `https://expert.valorie.ai` and `X-Tenant-ID` only as intentional negative assertions proving the old Valorie production origin is no longer accepted by backend CORS and the legacy tenant header is no longer advertised by backend preflight handling.
- `frontend/src/lib/api.test.js`: retains generic client-owned identity field names such as `user_id`, `creator_id`, `framework_id`, `owner_id`, `accountId`, `created_by`, `updatedBy`, and `X-Owner-ID` only as intentional negative assertions proving frontend request payload/header helpers strip client-supplied identity fields. It also retains `publishedToOrganization` only as a negative assertion proving obsolete organization-sharing state is no longer surfaced by owner framework summary normalization.

These allowlist entries do not cover active runtime/config/deploy/current-doc residue. The deploy/nginx/docker naming residue previously present in `deploy.sh`, `nginx-valorie.conf`, `docker-compose.yml`, `docker-entrypoint.sh`, and backend preflight handling has now been cleaned. The active `/migrate` route and isolated migration placeholder files have now been removed. Active tenant/org/invite route residue has been removed from frontend runtime surfaces, obsolete current-doc/script residue has been cleaned, and `backend_py/app/api/vector_sync.py` remains preserved as a Phase 9-deferred RAG/indexing API contract rather than a Phase 7 docs/scripts target.

## Round 0/1 Verification - 2026-07-02

### Working Tree Baseline

Command:

```powershell
git status --short
```

Outcome:

```text
Pre-existing uncommitted migration-doc edits were present before Round 0/1 source edits:
 M docs/migration/phases/phase-06-frontend-defirebase/phase-plan.md
 M docs/migration/phases/phase-06-frontend-defirebase/phase-report.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/phase-plan.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md
```

Result: existing docs-only changes were preserved and not reverted.

### Round 0 Domain And Customer String Inventory

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|valorie\.ai|expert\.valorie\.ai|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" . -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" -g "!.git"
```

Outcome:

```text
Exit 0. Active hits were classified in `.env.example`, `backend_py/.env.example`, `backend_py/alembic.ini`, `backend_py/main.py`, `frontend/src/lib/api.js`, `frontend/src/components/LandingPage.jsx`, `frontend/src/components/Login.jsx`, `frontend/src/components/Navbar.jsx`, `docker-compose.yml`, `docker-entrypoint.sh`, `deploy.sh`, and `nginx-valorie.conf`.
Historical migration hits were classified in `MIGRATION_PHASES.md` and `docs/migration/phases/**`.
```

### Round 0 Tenant/Org/Invite/Migration Inventory

Command:

```powershell
rg -n --hidden -S "tenant|Tenant|organization|Organization|invite|Invite|MigrationTool|migrate-data|cleanupData|updateFrameworkTenants" frontend/src backend_py docs README.md Dockerfile docker-compose.yml .env.example -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv"
```

Outcome:

```text
Exit 0. Active route/navigation hits remain in `frontend/src/App.jsx`, `AuthContext.jsx`, `TenantRoute.jsx`, `TenantSettings.jsx`, `YourOrganization.jsx`, `InviteAccept.jsx`, `MigrationTool.jsx`, framework route helpers, and related tests.
Phase 6 isolated placeholder hits remain in `frontend/src/migrate-data.js`, `frontend/src/utils/cleanupData.js`, `frontend/src/utils/DataCleanupButton.jsx`, and `frontend/src/utils/updateFrameworkTenants.js`.
Backend residue includes `backend_py/main.py` `X-Tenant-ID` preflight allowance and `backend_py/app/api/vector_sync.py` `include_organization`.
Current docs/scripts residue remains in `README.md`, `backend_py/README-DIFF.md`, and top-level backend helper scripts/tests.
Historical migration hits remain in `docs/migration/phases/**`.
```

### Round 0 Obsolete Script And Doc Inventory

Command:

```powershell
rg --files -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" | rg -i "firebase|Project-Startup|README-DIFF|deploy|nginx|test_|check_|diagnose|migrate|cleanup|tenant|organization|invite"
```

Outcome:

```text
Exit 0. Likely Round 5 obsolete docs/scripts remain: `Project-Startup-and-Operation-Flow.md`, `firebaseDoc.md`, `docs/CN_DEPLOY.md`, `backend_py/README-DIFF.md`, `backend_py/test_firebase.py`, `backend_py/test_cloud_llm.py`, `backend_py/test_update.py`, `backend_py/test_update_publish.py`, `backend_py/test_vec_base.py`, `backend_py/check_versions.py`, `backend_py/check_vector_store_attributes.py`, and `backend_py/diagnose_env.py`.
Maintained pytest files under `backend_py/tests/**` are not obsolete solely because their names match `test_*`.
```

### Round 1 Active Domain Scan

Command:

```powershell
rg -n --hidden -S "valorie\.ai|expert\.valorie\.ai|webmaster@valorie|framework-builder-55896|UNSW|ad\.unsw" backend_py/app backend_py/tests frontend/src frontend/index.html .env.example frontend/.env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py Dockerfile docker-compose.yml docker-entrypoint.sh deploy.sh nginx-valorie.conf -g "!frontend/dist"
```

Outcome:

```text
Exit 0. Remaining active matches are limited to Round 4 deploy/nginx cleanup targets plus one allowlisted backend negative assertion:
nginx-valorie.conf:5:    server_name expert.valorie.ai;
nginx-valorie.conf:30:# HTTPS - expert.valorie.ai
nginx-valorie.conf:34:    server_name expert.valorie.ai;
nginx-valorie.conf:36:    ssl_certificate /etc/letsencrypt/live/expert.valorie.ai/fullchain.pem;
nginx-valorie.conf:37:    ssl_certificate_key /etc/letsencrypt/live/expert.valorie.ai/privkey.pem;
nginx-valorie.conf:56:# HTTPS - *.valorie.ai
nginx-valorie.conf:62:    ssl_certificate /etc/letsencrypt/live/valorie.ai/fullchain.pem;
nginx-valorie.conf:63:    ssl_certificate_key /etc/letsencrypt/live/valorie.ai/privkey.pem;
deploy.sh:29:echo "1. Make sure DNS is configured (expert.valorie.ai and *.valorie.ai)"
deploy.sh:31:echo "   sudo certbot --nginx -d expert.valorie.ai"
deploy.sh:32:echo "   sudo certbot certonly --manual --preferred-challenges dns -d '*.valorie.ai' -d valorie.ai"
backend_py/tests\test_main.py:27:    assert not main.is_valid_origin("https://expert.valorie.ai")
```

### Round 1 Touched Runtime/Config Domain Scan

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|valorie\.ai|expert\.valorie\.ai|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" backend_py/main.py frontend/src/lib/api.js frontend/src/components/Login.jsx frontend/src/components/LandingPage.jsx frontend/src/components/Navbar.jsx frontend/index.html .env.example frontend/.env.example backend_py/.env.example backend_py/alembic.ini
```

Outcome:

```text
No stdout. `rg` exited 1.
```

### Round 1 Config Knob Scan

Command:

```powershell
rg -n "APP_BASE_DOMAIN|APP_NAME|VITE_APP_BASE_DOMAIN|VITE_APP_NAME|SUPER_ADMIN_EMAIL|FRONTEND_URL|Access-Control-Allow-Origin|ALLOWED_ORIGIN" backend_py/main.py .env.example frontend/.env.example backend_py/.env.example frontend/src/lib/api.js frontend/src/lib/appConfig.js
```

Outcome:

```text
Exit 0. Matches confirm `APP_NAME`, `APP_BASE_DOMAIN`, `FRONTEND_URL`, `SUPER_ADMIN_EMAIL`, `VITE_APP_NAME`, `VITE_APP_BASE_DOMAIN`, and `VITE_API_BASE_URL` are documented or used in the changed runtime/config files. Backend CORS emits exact `Access-Control-Allow-Origin` for allowed origins only.
```

### Focused Backend Tests

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q tests/test_main.py
```

Outcome:

```text
3 passed, 3 warnings in 18.77s.
Warnings were existing Pydantic V2 deprecation warnings from `app/api/users.py`.
```

### Backend Syntax

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m py_compile main.py tests/test_main.py
```

Outcome:

```text
No stdout. Command exited 0.
```

### Focused Frontend Tests

Initial sandboxed command:

```powershell
cd frontend
npm test -- src/lib/api.test.js src/components/Login.test.jsx
```

Sandboxed outcome:

```text
Failed before tests: esbuild could not read/resolve `frontend/vitest.config.js` because the sandbox denied reading directory "../../../..".
```

Escalated rerun command:

```powershell
cd frontend
npm test -- src/lib/api.test.js src/components/Login.test.jsx
```

Outcome:

```text
2 test files passed, 25 tests passed.
Warnings/notices: baseline-browser-mapping data over two months old; npm minor update notice.
```

### Frontend Lint

Command:

```powershell
cd frontend
npm run lint
```

Outcome:

```text
No lint errors. Command exited 0.
```

### Frontend Build

Initial sandboxed command:

```powershell
cd frontend
npm run build
```

Sandboxed outcome:

```text
Failed before build: esbuild could not read/resolve `frontend/vite.config.js` because the sandbox denied reading directory "../../../..".
```

Escalated rerun command:

```powershell
cd frontend
npm run build
```

Outcome:

```text
Build passed. Vite transformed 141 modules and produced `dist/index.html`, `dist/assets/index-BnompmXA.css`, and `dist/assets/index-D5mOTOV1.js`.
Warnings: baseline-browser-mapping data over two months old; browserslist/caniuse-lite data 9 months old; one chunk larger than 500 kB after minification.
```

### Browser Smoke Availability

Command:

```powershell
docker compose ps
```

Outcome:

```text
Exit 1. Docker emitted unset-env warnings for `JWT_SECRET_KEY`, `DEEPSEEK_API_KEY`, and `VITE_API_BASE_URL`, warned that `docker-compose.yml` `version` is obsolete, then failed to connect to Docker Desktop's Linux engine pipe:
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

Browser smoke result: not run. Concrete blocker: Docker Desktop Linux engine is unavailable, and no live Postgres service or seeded browser-smoke credentials were available in this turn.

### Skipped Checks

- Full frontend `npm test`: not run for Round 0/1 because this pass touched focused API-domain, login/app-name, landing/navbar copy, and backend CORS surfaces; focused frontend tests plus lint/build were run.
- Full backend pytest: not run because backend code change was limited to startup title/CORS origin construction and covered by `tests/test_main.py` plus syntax compilation.
- Browser smoke: not run because `docker compose ps` failed to connect to Docker Desktop's Linux engine pipe, leaving no live Docker/Postgres/seeded local environment.

### Whitespace Check

Command:

```powershell
git diff --check
```

Outcome:

```text
No stdout. Command exited 0.
```

## Requested Deploy/Nginx/Docker Naming Cleanup Verification - 2026-07-02

### Baseline Working Tree And Commit

Command:

```powershell
git status --short
```

Outcome before this pass:

```text
No stdout. Working tree was clean.
```

Command:

```powershell
git log -5 --oneline
```

Outcome:

```text
1d489d3 Complete Phase 7 Round 0/1 domain cleanup
ea32cbf Fix Phase 6 closeout docs and Phase 7 planning
27679f8 Complete Phase 6 frontend de-Firebase closeout
68a03e3 Implement Phase 6 Round 5 artefact wiring
3179837 Implement Phase 6 Round 4 admin REST wiring
```

### Initial Focused Deploy Legacy Scan

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|expert\.valorie\.ai|valorie\.ai|nginx-valorie|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" deploy.sh nginx-valorie.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py -g "!.git"
```

Outcome:

```text
Exit 0. Active deployment/config matches were found in `docker-entrypoint.sh`, `docker-compose.yml`, `deploy.sh`, and `nginx-valorie.conf`.
Key matches included `Starting Valorie Framework Builder`, `valorie-db`, `valorie-app`, `valorie-framework-builder:latest`, `POSTGRES_DB`/`POSTGRES_USER`/`DATABASE_URL` defaults using `valorie`, `nginx-valorie.conf`, `expert.valorie.ai`, `*.valorie.ai`, and wildcard Valorie nginx server names.
```

Command:

```powershell
rg -n --hidden -S "tenant|Tenant|X-Tenant-ID|organization|Organization|invite|Invite|server_name|ssl_certificate|container_name|image:|POSTGRES_DB|POSTGRES_USER|DATABASE_URL" deploy.sh nginx-valorie.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py
```

Outcome:

```text
Exit 0. Active deployment/config matches included backend preflight `X-Tenant-ID`, wildcard tenant nginx `server_name` entries, `proxy_set_header X-Tenant-ID $tenant`, Valorie container/image/database defaults, and neutral env-example database defaults from Round 0/1.
```

### Backend Contract Check For Tenant Header

Command:

```powershell
rg -n --hidden -S "X-Tenant-ID|tenant_id|tenantId|include_organization|organization" backend_py/app backend_py/tests docker-compose.yml docker-entrypoint.sh deploy.sh nginx-valorie.conf .env.example backend_py/.env.example -g "!backend_py/.venv"
```

Outcome:

```text
nginx-valorie.conf:77:        proxy_set_header X-Tenant-ID $tenant;
backend_py/app\api\vector_sync.py:19:    include_organization: bool = True
```

Interpretation: no active backend route consumes `X-Tenant-ID`; the remaining backend app hit is `include_organization` in the Phase 9-deferred vector sync request shape, which this pass did not change.

### Post-Edit Active Deploy Legacy Scan

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|expert\.valorie\.ai|valorie\.ai|nginx-valorie|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py backend_py/tests/test_main.py -g "!.git"
```

Outcome:

```text
backend_py/tests/test_main.py:29:    assert not main.is_valid_origin("https://expert.valorie.ai")
```

Interpretation: no active deploy/config files in the command contain Valorie/customer deployment naming. The remaining match is an allowlisted negative CORS assertion.

Command:

```powershell
rg -n --hidden -S "X-Tenant-ID|nginx-valorie|server_name ~|\*\.valorie|tenant subdomain|valorie-db|valorie-app|valorie-framework-builder" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh backend_py/main.py backend_py/tests/test_main.py
```

Outcome:

```text
The only match was the allowlisted negative preflight assertion in
`backend_py/tests/test_main.py`: `assert "X-Tenant-ID" not in allowed_headers`.
The exact line number is intentionally omitted because it is not part of the
acceptance evidence.
```

Interpretation: no active deploy/config files in the command contain legacy tenant nginx/header naming. The remaining match is an allowlisted negative preflight assertion.

### Docker Compose Config

Command:

```powershell
docker compose config
```

Outcome:

```text
Exit 0. Rendered config included `container_name: framework-app`, `container_name: framework-db`, `image: framework-builder:latest`, `POSTGRES_DB: framework`, `POSTGRES_USER: framework`, `DATABASE_URL: postgresql+psycopg://framework:change-me@db:5432/framework`, `APP_NAME: Personal AI Framework Studio`, `FRONTEND_URL: http://localhost:5173`, and `APP_BASE_DOMAIN: ""`.
Warnings:
time="2026-07-02T21:25:19+08:00" level=warning msg="The \"JWT_SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-07-02T21:25:19+08:00" level=warning msg="The \"DEEPSEEK_API_KEY\" variable is not set. Defaulting to a blank string."
time="2026-07-02T21:25:19+08:00" level=warning msg="C:\\Users\\micha\\Desktop\\project\\framework\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
```

### Backend Focused Tests

Initial meaningful run after adding a preflight assertion:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q tests/test_main.py
```

Outcome:

```text
1 failed, 3 passed, 3 warnings in 10.23s.
Failure: `TestClient(main.app)` raised `TypeError: Client.__init__() got an unexpected keyword argument 'app'` due the current Starlette/httpx versions. The test was rewritten to call `CustomCORSMiddleware.dispatch()` directly instead of using `TestClient`.
```

Corrected command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q tests/test_main.py
```

Outcome:

```text
4 passed, 3 warnings in 9.92s.
Warnings were existing Pydantic V2 deprecation warnings from `app/api/users.py`.
```

### Backend Syntax

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m py_compile main.py tests/test_main.py
```

Outcome:

```text
No stdout. Command exited 0.
```

### Shell And Nginx Config Validators

Command:

```powershell
Get-Command bash -All -ErrorAction SilentlyContinue | Select-Object Source,CommandType
```

Outcome:

```text
Source                       CommandType
------                       -----------
C:\WINDOWS\system32\bash.exe Application
```

Command:

```powershell
bash -n deploy.sh
```

Outcome:

```text
Exit 1. Windows launched the WSL `bash.exe` shim and failed before reading `deploy.sh` because WSL is not installed/configured in this environment. The terminal rendered the failure as mojibake, but it included WSL guidance for `wsl.exe --list --online` and `wsl.exe --install <Distro>`.
```

Command:

```powershell
Get-Command nginx -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
```

Outcome:

```text
No stdout. Command exited 1.
```

Nginx syntax validation result: not run because `nginx` is unavailable on PATH in this environment.

### Final Post-Documentation Scans And Whitespace Check

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|expert\.valorie\.ai|valorie\.ai|nginx-valorie|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py -g "!.git"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n --hidden -S "X-Tenant-ID|nginx-valorie|server_name ~|\*\.valorie|tenant subdomain|valorie-db|valorie-app|valorie-framework-builder|ssl_certificate" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh backend_py/main.py
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path -LiteralPath nginx-valorie.conf
```

Outcome:

```text
False
```

Command:

```powershell
Test-Path -LiteralPath nginx-framework.conf
```

Outcome:

```text
True
```

Command:

```powershell
git diff --check
```

Outcome:

```text
No stdout. Command exited 0.
```

Command:

```powershell
git status --short
```

Outcome:

```text
 M backend_py/main.py
 M backend_py/tests/test_main.py
 M deploy.sh
 M docker-compose.yml
 M docker-entrypoint.sh
 M docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md
 D nginx-valorie.conf
?? nginx-framework.conf
```

### Browser Smoke

Browser smoke was not run and is not claimed. This pass only changed deploy/config files and backend preflight handling; no live Docker/Postgres/frontend/seeded browser-smoke environment was started.

## Migration Placeholder Route/Tool Cleanup Verification - 2026-07-05

### Baseline Working Tree

Command:

```powershell
git status --short
```

Outcome before this pass:

```text
No stdout. Working tree was clean.
```

### Focused Placeholder Inventory

Command:

```powershell
rg -n --hidden -S "MigrationTool|migrate-data|cleanupData|DataCleanupButton|updateFrameworkTenants|/migrate|migration placeholder|data migration|cleanup data|migration tool" frontend/src backend_py docs README.md -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv"
```

Outcome:

```text
Exit 0. Active frontend matches were found in:
frontend/src\App.jsx:16:import MigrationTool from './components/MigrationTool'
frontend/src\App.jsx:66:        <Route path="/migrate" element={<MigrationTool />} />
frontend/src\App.route.test.jsx:39:vi.mock('./components/MigrationTool', () => ({
frontend/src\migrate-data.js:2:  'Legacy client-side migration tooling is isolated for Phase 6 SDK removal.'
frontend/src\components\MigrationTool.jsx:1:function MigrationTool() {
frontend/src\components\MigrationTool.jsx:18:export default MigrationTool
frontend/src\utils\cleanupData.js:4:export async function cleanupData() {
frontend/src\utils\DataCleanupButton.jsx:1:function DataCleanupButton() {
frontend/src\utils\DataCleanupButton.jsx:14:export default DataCleanupButton

The same scan also matched historical migration docs under `docs/migration/phases/**`,
which remain allowlisted audit records. `backend_py/app/services/vectorstore/openai_legacy.py`
matched only the phrase "legacy migration tool" inside provider compatibility code; it
is not a frontend migration placeholder route/tool and was not edited.
```

Candidate classification:

- Deleted obsolete active placeholders: `frontend/src/components/MigrationTool.jsx`, `frontend/src/migrate-data.js`, `frontend/src/utils/cleanupData.js`, `frontend/src/utils/DataCleanupButton.jsx`, and `frontend/src/utils/updateFrameworkTenants.js`.
- Removed active route/import: `frontend/src/App.jsx` `/migrate` route and `MigrationTool` import.
- Removed active-test placeholder mock: `frontend/src/App.route.test.jsx` `MigrationTool` mock.
- Deferred/non-target: tenant/org/invite route shells and `backend_py/app/services/vectorstore/openai_legacy.py` provider compatibility text.

### Post-Edit Placeholder Scan

Command:

```powershell
rg -n --hidden -S "MigrationTool|migrate-data|cleanupData|DataCleanupButton|updateFrameworkTenants|/migrate" frontend/src -g "!frontend/dist"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path frontend\src\migrate-data.js; Test-Path frontend\src\utils\cleanupData.js; Test-Path frontend\src\utils\DataCleanupButton.jsx; Test-Path frontend\src\utils\updateFrameworkTenants.js; Test-Path frontend\src\components\MigrationTool.jsx
```

Outcome:

```text
False
False
False
False
False
```

### Focused Frontend Route Test

Initial sandboxed command:

```powershell
cd frontend
npm test -- App.route.test.jsx
```

Sandboxed outcome:

```text
Failed before tests: esbuild could not read/resolve `frontend/vitest.config.js`
because the sandbox denied reading directory "../../../..".
```

Escalated rerun command:

```powershell
cd frontend
npm test -- App.route.test.jsx
```

Outcome:

```text
1 test file passed, 1 test passed.
Warning: baseline-browser-mapping data is over two months old.
```

### Full Frontend Tests

Command:

```powershell
cd frontend
npm test
```

Outcome:

```text
10 test files passed, 53 tests passed.
Warnings/notices: baseline-browser-mapping data over two months old;
Browserslist/caniuse-lite data 9 months old.
```

### Frontend Lint

Command:

```powershell
cd frontend
npm run lint
```

Outcome:

```text
No lint errors. Command exited 0.
```

### Frontend Build

Initial sandboxed command:

```powershell
cd frontend
npm run build
```

Sandboxed outcome:

```text
Failed before build: esbuild could not read/resolve `frontend/vite.config.js`
because the sandbox denied reading directory "../../../..".
```

Escalated rerun command:

```powershell
cd frontend
npm run build
```

Outcome:

```text
Build passed. Vite transformed 140 modules and produced `dist/index.html`,
`dist/assets/index-DfLzCzBj.css`, and `dist/assets/index-D53k77nA.js`.
Warnings: baseline-browser-mapping data over two months old; browserslist/caniuse-lite
data 9 months old; one chunk larger than 500 kB after minification.
```

### Skipped Checks

- Backend syntax and backend tests: not run because this pass changed only frontend route/test files plus migration docs.
- Browser smoke: not run because this pass only removed inactive frontend placeholder tooling, and the prior Docker/Postgres/seeded-credential blocker remains unresolved in this environment.

### Final Post-Documentation Scans And Whitespace Check

Command:

```powershell
rg -n --hidden -S "MigrationTool|migrate-data|cleanupData|DataCleanupButton|updateFrameworkTenants|/migrate" frontend/src backend_py/app -g "!frontend/dist" -g "!backend_py/.venv"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path frontend\src\migrate-data.js; Test-Path frontend\src\utils\cleanupData.js; Test-Path frontend\src\utils\DataCleanupButton.jsx; Test-Path frontend\src\utils\updateFrameworkTenants.js; Test-Path frontend\src\components\MigrationTool.jsx
```

Outcome:

```text
False
False
False
False
False
```

Command:

```powershell
git diff --check
```

Outcome:

```text
No stdout. Command exited 0.
```

Command:

```powershell
git status --short
```

Outcome:

```text
 M docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md
 M frontend/src/App.jsx
 M frontend/src/App.route.test.jsx
 D frontend/src/components/MigrationTool.jsx
 D frontend/src/migrate-data.js
 D frontend/src/utils/DataCleanupButton.jsx
 D frontend/src/utils/cleanupData.js
 D frontend/src/utils/updateFrameworkTenants.js
```

## Tenant/Org/Invite Cleanup Inventory Verification - 2026-07-06

Scope: inventory-only pass. No runtime code deletion, backend/frontend tests, database model edits, Alembic migration edits, auth/session behavior changes, or replacement tenant/org/invite/workspace behavior were performed.

### Baseline Working Tree

Command:

```powershell
git status --short
```

Outcome:

```text
No stdout. Working tree was clean before this inventory pass.
```

### Active Frontend Source Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" frontend/src -g "!**/*.test.*" -g "!frontend/dist"
```

Outcome summary:

```text
15 active frontend source files, 72 total matches.

File counts:
- frontend/src/App.jsx: 9
- frontend/src/components/CreateFramework.jsx: 4
- frontend/src/components/FrameworkCard.jsx: 3
- frontend/src/components/FrameworkEditor.jsx: 5
- frontend/src/components/InviteAccept.jsx: 1
- frontend/src/components/LandingPage.jsx: 2
- frontend/src/contexts/AuthContext.jsx: 4
- frontend/src/components/Login.jsx: 1
- frontend/src/lib/api.js: 1
- frontend/src/components/Navbar.jsx: 19
- frontend/src/components/TenantRoute.jsx: 14
- frontend/src/components/TenantSettings.jsx: 1
- frontend/src/components/UpdateFrameworksButton.jsx: 1
- frontend/src/components/YourFrameworks.jsx: 6
- frontend/src/components/YourOrganization.jsx: 1
```

Interpretation: active frontend cleanup remains. The matches are route shells, route guards, user-state compatibility fields, route-generation helpers, inert org-sharing UI, and isolated org/invite/tenant placeholders.

### Frontend API Split-String Identity-Strip Scan

Command:

```powershell
rg -n --hidden -F "tenant_id" frontend\src\lib\api.js
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n --hidden -F "X-Tenant-ID" frontend\src\lib\api.js
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n --hidden -S "stripArtefactResourceFields|\['tenant', 'id'\]|\['X', 'Tenant-ID'\]" frontend\src\lib\api.js
```

Outcome:

```text
frontend\src\lib\api.js:180:function stripArtefactResourceFields(artefactData = {}) {
frontend\src\lib\api.js:187:    ['tenant', 'id'].join('_'),
frontend\src\lib\api.js:188:    ['X', 'Tenant-ID'].join('-'),
frontend\src\lib\api.js:236:    const contentJson = stripArtefactResourceFields(artefactData)
```

Interpretation: literal full-string scans missed the `api.js` `tenant_id` and `X-Tenant-ID` handling because the active guard constructs those names from split strings. The inventory now documents this as a security-preserving identity-strip guard that prevents client-supplied identity/header data from being forwarded in artefact payloads; it is preserved for now and assigned only to a focused future frontend API cleanup that keeps equivalent strip coverage.

### UpdateFrameworksButton Import/Render Scan

Command:

```powershell
rg -n --hidden -S "UpdateFrameworksButton|YourFrameworks" frontend\src\components\UpdateFrameworksButton.jsx frontend\src\components\YourFrameworks.jsx frontend\src\App.jsx
```

Outcome:

```text
frontend\src\App.jsx:12:import YourFrameworks from './components/YourFrameworks'
frontend\src\App.jsx:71:              <YourFrameworks />
frontend\src\components\YourFrameworks.jsx:5:import UpdateFrameworksButton from './UpdateFrameworksButton'
frontend\src\components\YourFrameworks.jsx:8:function YourFrameworks() {
frontend\src\components\YourFrameworks.jsx:130:        <UpdateFrameworksButton />
frontend\src\components\YourFrameworks.jsx:313:export default YourFrameworks
frontend\src\components\UpdateFrameworksButton.jsx:1:function UpdateFrameworksButton() {
frontend\src\components\UpdateFrameworksButton.jsx:6:export default UpdateFrameworksButton
```

Interpretation: `UpdateFrameworksButton.jsx` is active source residue because `YourFrameworks.jsx` imports and renders it in the active framework list, even though the component currently returns null. The inventory now assigns it to a focused frontend org placeholder cleanup, not backend tenant/model cleanup.

### Frontend Test Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" frontend/src -g "**/*.test.*" -g "!frontend/dist"
```

Outcome summary:

```text
6 frontend test files, 34 total matches.

File counts:
- frontend/src/lib/api.test.js: 20
- frontend/src/App.route.test.jsx: 6
- frontend/src/components/TenantRoute.test.jsx: 3
- frontend/src/components/FrameworkEditor.test.jsx: 2
- frontend/src/components/FrameworkCard.test.jsx: 1
- frontend/src/components/Login.test.jsx: 2
```

Interpretation: route/component tests need frontend cleanup updates. `frontend/src/lib/api.test.js` also contains intentional negative assertions proving frontend helpers strip client-supplied `tenant_id` and `X-Tenant-ID`; keep equivalent coverage unless rewritten.

### Backend App, Services, Models, And Migrations Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py/app/models.py backend_py/app/db.py backend_py/app/api backend_py/app/services backend_py/alembic -g "!backend_py/.venv"
```

Outcome summary:

```text
1 backend app file, 1 total match:
- backend_py/app/api/vector_sync.py: 1
```

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py/app/models.py backend_py/alembic
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no tenant/org/invite residue was found in the active database model or Alembic migration files. The single backend app match is `include_organization` in `backend_py/app/api/vector_sync.py`, which remains deferred because that route is Phase 9-deferred indexing/RAG plumbing.

### Backend Tenant/Invite Router Absence Scan

Command:

```powershell
rg -n --hidden -S "/api/tenants|tenants/|tenant_members|invites|invite_token|organization_id|org_id" backend_py/app backend_py/alembic backend_py/tests -g "!backend_py/.venv"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no active backend tenant/invite router, tenant-member schema, invite token field, organization id field, or org id field was found.

### Backend Ownership/Auth Preservation Scan

Command:

```powershell
rg -n --hidden -S "Depends\(get_current_user_id\)|Depends\(get_current_user\)|current_user_id|owner|creator_id|user_id" backend_py/app/api/frameworks_crud.py backend_py/app/api/frameworks_public.py backend_py/app/api/artefacts.py backend_py/app/api/admin_users.py backend_py/app/api/users.py
```

Outcome summary:

```text
Matches show current framework, artefact, admin, and user routes derive identity from JWT-backed dependencies and enforce ownership through backend user id / creator_id checks.
```

Interpretation: backend personal-use ownership/auth concepts should be preserved and are not classified as tenant/org/invite residue.

### Backend Test And Obsolete Helper Scan

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py/app/api/vector_sync.py backend_py/tests/test_main.py
```

Outcome summary:

```text
backend_py/tests/test_main.py has 2 matches, both in the negative preflight assertion that `X-Tenant-ID` is not advertised.
backend_py/app/api/vector_sync.py has 1 match: `include_organization`.
```

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py -g "!backend_py/.venv" -g "!backend_py/app/**" -g "!backend_py/tests/**" -g "!backend_py/alembic/**" -g "!backend_py/scripts/**"
```

Outcome summary:

```text
5 obsolete backend doc/helper files, 26 total matches.

File counts:
- backend_py/README-DIFF.md: 5
- backend_py/test_update.py: 1
- backend_py/test_update_publish.py: 11
- backend_py/test_firebase.py: 7
- backend_py/check_vector_store_attributes.py: 2
```

Interpretation: top-level backend helper scripts and obsolete backend docs remain Round 5 cleanup material, not active backend app behavior.

### Env, Config, And Deploy Scan

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" .env.example frontend/.env.example backend_py/.env.example Dockerfile docker-compose.yml docker-entrypoint.sh deploy.sh nginx-framework.conf
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: active env/config/deploy files are clean for the requested tenant/org/invite terms.

### Current And Historical Docs Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" MIGRATION_PHASES.md README.md docs -g "!docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md"
```

Outcome summary:

```text
20 files, 382 total matches.

Current docs/tooling:
- README.md: 1
- docs/skills/migration-reviewer/SKILL.md: 1
- docs/skills/migration-phase-planner/SKILL.md: 1

Canonical/historical records:
- MIGRATION_PHASES.md: 12
- docs/migration/phases/**: 367
```

Interpretation: `README.md` remains Round 5 current-doc cleanup. `MIGRATION_PHASES.md` and `docs/migration/phases/**` are historical/canonical allowlist records. `docs/skills/**` are migration tooling references and are deferred unless a later docs-tooling cleanup updates them.

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" MIGRATION_PHASES.md README.md docs/PERSONAL_USE_BOUNDARY.md docs/migration/README.md docs/migration/decisions/ADR-0001-auth-strategy.md
```

Outcome summary:

```text
README.md has one current-doc match: "Legacy Multi-Tenant Compatibility".
MIGRATION_PHASES.md has canonical cleanup-target matches.
docs/PERSONAL_USE_BOUNDARY.md, docs/migration/README.md, and ADR-0001 had no matches for this term set.
```

### Specific Hidden-Identifier Scan

Command:

```powershell
rg -n --hidden -S "default_tenant|framework_tenant|invite_token|organization_id|org_id" . -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" -g "!.git"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no `default_tenant`, `framework_tenant`, `invite_token`, `organization_id`, or `org_id` residue was found in the scanned workspace.

### Skipped Checks

- Backend tests: not run because this pass changed only migration documentation.
- Frontend tests: not run because this pass changed only migration documentation.
- Browser smoke: not run and not claimed; this was an inventory-only documentation pass.

### Post-Documentation Whitespace Check

Command:

```powershell
git diff --check
```

Outcome:

```text
No stdout. Command exited 0.
```

## Frontend Personal Route Cleanup Verification - 2026-07-06

Scope: frontend personal-route cleanup only. Backend auth/session behavior, backend ownership checks, database models, migrations, README, obsolete backend helper scripts, `UpdateFrameworksButton.jsx`, and the `api.js` split-string identity-strip guard were not changed.

### Active Route Residue Scan

Command:

```powershell
rg -n 'TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept|/:tenantId|/invite/:token|/personal/frameworks|/editor/|getPath\(|tenantShim|getCurrentTenantId' frontend\src
```

Outcome:

```text
frontend\src\components\InviteAccept.jsx:1:function InviteAccept() {
frontend\src\components\InviteAccept.jsx:17:export default InviteAccept
frontend\src\components\TenantRoute.jsx:5: * TenantRoute - Tenant Route Protection Component (Path Mode - Simplified Version)
frontend\src\components\TenantRoute.jsx:11:function TenantRoute({ children }) {
frontend\src\components\TenantRoute.jsx:92:export default TenantRoute
frontend\src\components\YourOrganization.jsx:1:function YourOrganization() {
frontend\src\components\YourOrganization.jsx:18:export default YourOrganization
frontend\src\components\TenantSettings.jsx:1:function TenantSettings() {
frontend\src\components\TenantSettings.jsx:17:export default TenantSettings
frontend\src\components\TenantCreationModal.jsx:1:function TenantCreationModal() {
frontend\src\components\TenantCreationModal.jsx:5:export default TenantCreationModal
```

Interpretation: no active old route paths, route helpers, or active route imports remain. The remaining matches are unmounted placeholder component files deferred to the frontend org/invite placeholder cleanup slice.

Command:

```powershell
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/' frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: active frontend source and tests no longer define or assert the removed tenant/invite/personal-shim route paths.

### Removed Placeholder Import Scan

Command:

```powershell
rg -n "from './components/(TenantRoute|TenantSettings|InviteAccept|YourOrganization)'|from './(TenantRoute|TenantSettings|InviteAccept|YourOrganization)'|<TenantRoute|<TenantSettings|<InviteAccept|<YourOrganization" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: `App.jsx` no longer imports or mounts `TenantRoute`, `TenantSettings`, `InviteAccept`, or `YourOrganization`.

Command:

```powershell
rg -n "getCurrentTenantId" frontend\src -g "!frontend/src/lib/api.js" -g "!frontend/src/lib/api.test.js"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no component or active route-generation code imports the removed legacy route shim. The shim was also removed from `api.js` and `api.test.js`.

### Remaining Tenant/Org/Invite Residue Scan

Command:

```powershell
rg -n 'tenant|Tenant|organization|Organization|invite|Invite|joinedOrganization|tenantId|publishedToOrganization|Publish to Organization|Tenant Settings|My Organization|X-Tenant-ID|tenant_id' frontend\src -g '!frontend/src/components/TenantRoute.jsx' -g '!frontend/src/components/TenantCreationModal.jsx' -g '!frontend/src/components/TenantSettings.jsx' -g '!frontend/src/components/YourOrganization.jsx' -g '!frontend/src/components/InviteAccept.jsx'
```

Outcome summary:

```text
frontend\src\contexts\AuthContext.jsx retains tenantId, joinedOrganization, and updateUserTenant.
frontend\src\lib\api.js retains split-string tenant_id / X-Tenant-ID identity-strip guard lines and publishedToOrganization normalization.
frontend\src\lib\api.test.js retains tenant_id / X-Tenant-ID negative assertions.
frontend\src\components\FrameworkCard.jsx retains organization sharing labels/actions.
frontend\src\components\YourFrameworks.jsx retains organization filters and publishedToOrganization checks.
frontend\src\components\UpdateFrameworksButton.jsx remains as the documented org-field repair placeholder.
```

Interpretation: remaining matches are the previously documented deferrals: frontend auth-state cleanup, frontend org placeholder/sharing cleanup, and focused API identity-strip guard cleanup. They are not active tenant route shells.

### Focused Route/API Tests

Initial sandboxed command:

```powershell
cd frontend
npm test -- src/App.route.test.jsx src/components/Login.test.jsx src/components/FrameworkEditor.test.jsx src/lib/api.test.js
```

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read ../../../.. and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
cd frontend
npm test -- src/App.route.test.jsx src/components/Login.test.jsx src/components/FrameworkEditor.test.jsx src/lib/api.test.js
```

Escalated rerun result:

```text
4 test files passed.
30 tests passed.
Duration 5.16s.
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Lint

Command:

```powershell
cd frontend
npm run lint
```

Result:

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

Exit code: `0`.

### Full Frontend Tests

Initial sandboxed command:

```powershell
cd frontend
npm test
```

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read ../../../.. and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
cd frontend
npm test
```

Escalated rerun result:

```text
9 test files passed.
52 tests passed.
Duration 4.06s.
```

Warnings/output: existing stdout from `PublishModal.test.jsx` and `Login.test.jsx`; existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Build

Initial sandboxed command:

```powershell
cd frontend
npm run build
```

Initial result:

```text
Failed before build compilation: esbuild/Vite could not read ../../../.. and could not resolve frontend\vite.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
cd frontend
npm run build
```

Escalated rerun result:

```text
vite v7.1.9 building for production...
136 modules transformed.
dist/index.html                 0.48 kB | gzip:   0.31 kB
dist/assets/index-DfLzCzBj.css 38.87 kB | gzip:   7.06 kB
dist/assets/index-BZMVfgS5.js  851.64 kB | gzip: 257.11 kB
built in 5.19s
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings; existing chunk larger than 500 kB after minification warning.

### Skipped Checks

- Backend tests: not run because this slice changed only frontend route/navigation/test files and migration docs.
- Browser smoke: not run and not claimed; Docker/Postgres/seeded local environment availability remains the blocker recorded earlier in Phase 6 and Phase 7 docs.

### Post-Documentation Rerun

Commands:

```powershell
rg -n 'TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept|/:tenantId|/invite/:token|/personal/frameworks|/editor/|getPath\(|tenantShim|getCurrentTenantId' frontend\src
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/' frontend\src
git diff --check
```

Results:

```text
The first scan still reports only the unmounted placeholder component files: InviteAccept.jsx, TenantCreationModal.jsx, TenantSettings.jsx, TenantRoute.jsx, and YourOrganization.jsx.
The active old-route path scan returned no stdout; `rg` exited 1.
`git diff --check` returned no stdout and exited 0.
```

## Unmounted Frontend Tenant/Org/Invite Placeholder Cleanup Verification - 2026-07-07

Scope: delete only confirmed-unmounted frontend tenant/org/invite placeholder files. Backend auth/session behavior, database models, migrations, ownership checks, API contracts, `AuthContext.jsx` tenant/org state, `FrameworkCard.jsx`/`YourFrameworks.jsx` organization-sharing UI, `UpdateFrameworksButton.jsx`, and the `api.js` split-string identity-strip guard were not changed.

### Baseline Working Tree

Command:

```powershell
git status --short
```

Outcome:

```text
No stdout. Working tree was clean before this placeholder cleanup slice.
```

### Pre-Delete Placeholder Inventory

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src
```

Outcome:

```text
frontend\src\components\InviteAccept.jsx:1:function InviteAccept() {
frontend\src\components\InviteAccept.jsx:17:export default InviteAccept
frontend\src\components\TenantCreationModal.jsx:1:function TenantCreationModal() {
frontend\src\components\TenantCreationModal.jsx:5:export default TenantCreationModal
frontend\src\components\TenantRoute.jsx:5: * TenantRoute - Tenant Route Protection Component (Path Mode - Simplified Version)
frontend\src\components\TenantRoute.jsx:11:function TenantRoute({ children }) {
frontend\src\components\TenantRoute.jsx:92:export default TenantRoute
frontend\src\components\TenantSettings.jsx:1:function TenantSettings() {
frontend\src\components\TenantSettings.jsx:17:export default TenantSettings
frontend\src\components\YourOrganization.jsx:1:function YourOrganization() {
frontend\src\components\YourOrganization.jsx:18:export default YourOrganization
```

Interpretation: each placeholder name appeared only inside its own component file.

Command:

```powershell
rg -n "from .*TenantRoute|from .*TenantCreationModal|from .*TenantSettings|from .*YourOrganization|from .*InviteAccept|<TenantRoute|<TenantCreationModal|<TenantSettings|<YourOrganization|<InviteAccept" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no active imports or JSX renders remained for the five placeholder components.

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src -g "**/*.test.*"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no frontend test referenced the five placeholder components.

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src -g "!frontend/src/components/TenantRoute.jsx" -g "!frontend/src/components/TenantCreationModal.jsx" -g "!frontend/src/components/TenantSettings.jsx" -g "!frontend/src/components/YourOrganization.jsx" -g "!frontend/src/components/InviteAccept.jsx"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: excluding the five candidate files left no active source or test references.

Command:

```powershell
Test-Path frontend\src\components\TenantRoute.jsx; Test-Path frontend\src\components\TenantCreationModal.jsx; Test-Path frontend\src\components\TenantSettings.jsx; Test-Path frontend\src\components\YourOrganization.jsx; Test-Path frontend\src\components\InviteAccept.jsx
```

Outcome:

```text
True
True
True
True
True
```

### Deleted Files

- `frontend/src/components/TenantRoute.jsx`
- `frontend/src/components/TenantCreationModal.jsx`
- `frontend/src/components/TenantSettings.jsx`
- `frontend/src/components/YourOrganization.jsx`
- `frontend/src/components/InviteAccept.jsx`

No tests were updated or deleted because no test referenced only these removed placeholders.

### Post-Delete Placeholder Scans

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path frontend\src\components\TenantRoute.jsx; Test-Path frontend\src\components\TenantCreationModal.jsx; Test-Path frontend\src\components\TenantSettings.jsx; Test-Path frontend\src\components\YourOrganization.jsx; Test-Path frontend\src\components\InviteAccept.jsx
```

Outcome:

```text
False
False
False
False
False
```

### Invite/Tenant Route Residue Scan

Command:

```powershell
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/|Tenant Settings|My Organization|<Invite|<YourOrganization|<TenantSettings|<TenantRoute' frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no active tenant or invite route paths, old personal-route shim paths, or deleted placeholder JSX route mounts remain in `frontend/src`.

### Remaining Frontend Tenant/Org Residue Scan

Command:

```powershell
rg -n "tenant|Tenant|organization|Organization|invite|Invite|joinedOrganization|tenantId|publishedToOrganization|Publish to Organization|X-Tenant-ID|tenant_id" frontend\src -g "!**/*.test.*"
```

Outcome:

```text
frontend\src\contexts\AuthContext.jsx:24:    tenantId: existingUser?.tenantId || null,
frontend\src\contexts\AuthContext.jsx:25:    joinedOrganization: existingUser?.joinedOrganization || null,
frontend\src\contexts\AuthContext.jsx:125:  const updateUserTenant = async (tenantId, reload = false) => {
frontend\src\contexts\AuthContext.jsx:132:      tenantId,
frontend\src\contexts\AuthContext.jsx:162:    updateUserTenant,
frontend\src\lib\api.js:177:    ['tenant', 'id'].join('_'),
frontend\src\lib\api.js:178:    ['X', 'Tenant-ID'].join('-'),
frontend\src\lib\api.js:385:    publishedToOrganization: Boolean(framework.publishedToOrganization),
frontend\src\components\FrameworkCard.jsx:25:  const isShared = Boolean(framework.publishedToOrganization)
frontend\src\components\FrameworkCard.jsx:102:    alert('Organization sharing is not available in this migration round.')
frontend\src\components\FrameworkCard.jsx:107:    alert('Organization sharing is not available in this migration round.')
frontend\src\components\FrameworkCard.jsx:389:                <span>Unpublish from Organization</span>
frontend\src\components\FrameworkCard.jsx:396:                <span>Publish to Organization</span>
frontend\src\components\YourFrameworks.jsx:57:        return frameworks.filter(f => !f.isPublic && !f.publishedToOrganization)
frontend\src\components\YourFrameworks.jsx:60:      case 'organization':
frontend\src\components\YourFrameworks.jsx:61:        return frameworks.filter(f => f.publishedToOrganization)
frontend\src\components\YourFrameworks.jsx:162:                      f => !f.isPublic && !f.publishedToOrganization
frontend\src\components\YourFrameworks.jsx:171:                <option value="organization">
frontend\src\components\YourFrameworks.jsx:172:                  Published to Organization (
frontend\src\components\YourFrameworks.jsx:173:                  {frameworks.filter(f => f.publishedToOrganization).length})
frontend\src\components\UpdateFrameworksButton.jsx:2:  // Phase 7 owns the old organization-field repair path.
```

Interpretation: remaining matches are the explicitly deferred frontend auth-state, API identity-strip guard/published-org normalization, organization-sharing UI, organization filters, and `UpdateFrameworksButton.jsx` residue. This slice intentionally did not change them.

### Frontend Lint

Command:

```powershell
npm run lint
```

Working directory: `frontend`

Outcome:

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

Exit code: `0`.

### Full Frontend Tests

Initial sandboxed command:

```powershell
npm test
```

Working directory: `frontend`

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read "../../../.." and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm test
```

Working directory: `frontend`

Escalated rerun result:

```text
9 test files passed.
52 tests passed.
Duration 6.90s.
```

Warnings/output: existing stdout from `PublishModal.test.jsx` and `Login.test.jsx`; existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Build

Initial sandboxed command:

```powershell
npm run build
```

Working directory: `frontend`

Initial result:

```text
Failed before build compilation: esbuild/Vite could not read "../../../.." and could not resolve frontend\vite.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm run build
```

Working directory: `frontend`

Escalated rerun result:

```text
vite v7.1.9 building for production...
136 modules transformed.
dist/index.html                 0.48 kB | gzip:   0.31 kB
dist/assets/index-DfLzCzBj.css  38.87 kB | gzip:   7.06 kB
dist/assets/index-BZMVfgS5.js   851.64 kB | gzip: 257.11 kB
built in 6.56s
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings; existing chunk larger than 500 kB after minification warning.

### Skipped Checks

- Backend tests: not run because this slice changed only frontend placeholder files and migration docs.
- Browser smoke: not run and not claimed; Docker/Postgres/seeded local environment availability remains the blocker recorded earlier in Phase 6 and Phase 7 docs.

### Post-Documentation Rerun

Commands:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/|Tenant Settings|My Organization|<Invite|<YourOrganization|<TenantSettings|<TenantRoute' frontend\src
git diff --check
```

Results:

```text
The deleted-component scan returned no stdout; `rg` exited 1.
The active old-route path scan returned no stdout; `rg` exited 1.
`git diff --check` returned no stdout and exited 0.
```

## Frontend Organization-Sharing UI Residue Cleanup Verification - 2026-07-07

Scope: active frontend org-sharing UI residue cleanup only. `AuthContext.jsx` tenant/org state, the `api.js` identity-strip guard/request normalization, backend behavior, database models, migrations, API contracts, README, and obsolete backend helper scripts were not changed.

### Focused Pre-Edit Component Inventory

Command:

```powershell
rg -n "publishedToOrganization|UpdateFrameworksButton|Publish to Organization|Unpublish from Organization|Organization sharing|Published to Organization|organization" frontend\src\components
```

Outcome:

```text
frontend\src\components\FrameworkCard.jsx:25:  const isShared = Boolean(framework.publishedToOrganization)
frontend\src\components\FrameworkCard.jsx:102:    alert('Organization sharing is not available in this migration round.')
frontend\src\components\FrameworkCard.jsx:107:    alert('Organization sharing is not available in this migration round.')
frontend\src\components\FrameworkCard.jsx:389:                <span>Unpublish from Organization</span>
frontend\src\components\FrameworkCard.jsx:396:                <span>Publish to Organization</span>
frontend\src\components\UpdateFrameworksButton.jsx:1:function UpdateFrameworksButton() {
frontend\src\components\UpdateFrameworksButton.jsx:2:  // Phase 7 owns the old organization-field repair path.
frontend\src\components\UpdateFrameworksButton.jsx:6:export default UpdateFrameworksButton
frontend\src\components\YourFrameworks.jsx:5:import UpdateFrameworksButton from './UpdateFrameworksButton'
frontend\src\components\YourFrameworks.jsx:57:        return frameworks.filter(f => !f.isPublic && !f.publishedToOrganization)
frontend\src\components\YourFrameworks.jsx:60:      case 'organization':
frontend\src\components\YourFrameworks.jsx:61:        return frameworks.filter(f => f.publishedToOrganization)
frontend\src\components\YourFrameworks.jsx:129:        <UpdateFrameworksButton />
frontend\src\components\YourFrameworks.jsx:162:                      f => !f.isPublic && !f.publishedToOrganization
frontend\src\components\YourFrameworks.jsx:171:                <option value="organization">
frontend\src\components\YourFrameworks.jsx:172:                  Published to Organization (
frontend\src\components\YourFrameworks.jsx:173:                  {frameworks.filter(f => f.publishedToOrganization).length})
```

Command:

```powershell
rg -n "UpdateFrameworksButton" frontend\src
```

Outcome:

```text
frontend\src\components\UpdateFrameworksButton.jsx:1:function UpdateFrameworksButton() {
frontend\src\components\UpdateFrameworksButton.jsx:6:export default UpdateFrameworksButton
frontend\src\components\YourFrameworks.jsx:5:import UpdateFrameworksButton from './UpdateFrameworksButton'
frontend\src\components\YourFrameworks.jsx:129:        <UpdateFrameworksButton />
```

Interpretation: `UpdateFrameworksButton.jsx` was only a null org-field repair placeholder and was actively imported/rendered by `YourFrameworks.jsx`; `FrameworkCard.jsx` and `YourFrameworks.jsx` contained the active visible/inert org-sharing UI residue.

### Files Changed Or Deleted

- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/FrameworkCard.test.jsx`
- `frontend/src/components/YourFrameworks.jsx`
- `frontend/src/components/UpdateFrameworksButton.jsx` deleted
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

### Post-Cleanup Active Component Scans

Command:

```powershell
rg -n "publishedToOrganization|UpdateFrameworksButton|Publish to Organization|Unpublish from Organization|Organization sharing|Published to Organization|organization|Organization" frontend\src\components
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n "UpdateFrameworksButton" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path frontend\src\components\UpdateFrameworksButton.jsx
```

Outcome:

```text
False
```

### Remaining Deferred Frontend Residue Scan

Command:

```powershell
rg -n "tenantId|joinedOrganization|updateUserTenant|tenant_id|X-Tenant-ID|publishedToOrganization|organization|Organization|invite|Invite" frontend\src -g '!**/*.test.*'
```

Outcome:

```text
frontend\src\contexts\AuthContext.jsx:24:    tenantId: existingUser?.tenantId || null,
frontend\src\contexts\AuthContext.jsx:25:    joinedOrganization: existingUser?.joinedOrganization || null,
frontend\src\contexts\AuthContext.jsx:125:  const updateUserTenant = async (tenantId, reload = false) => {
frontend\src\contexts\AuthContext.jsx:132:      tenantId,
frontend\src\contexts\AuthContext.jsx:162:    updateUserTenant,
frontend\src\lib\api.js:385:    publishedToOrganization: Boolean(framework.publishedToOrganization),
```

Interpretation: the remaining non-test frontend matches are the explicitly deferred `AuthContext.jsx` tenant/org state and `api.js` framework normalization/identity-strip cleanup. Active component org-sharing UI residue is removed.

### Focused Component Test

Initial sandboxed command:

```powershell
npm test -- FrameworkCard.test.jsx
```

Working directory: `frontend`

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read "../../../.." and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm test -- FrameworkCard.test.jsx
```

Working directory: `frontend`

Escalated rerun result:

```text
1 test file passed.
2 tests passed.
Duration 3.76s.
```

Warning: existing stale `baseline-browser-mapping` warning.

### Full Frontend Tests

Command:

```powershell
npm test
```

Working directory: `frontend`

Outcome:

```text
9 test files passed.
53 tests passed.
Duration 9.10s.
```

Warnings/output: existing stdout from `PublishModal.test.jsx` and `Login.test.jsx`; existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Lint

Command:

```powershell
npm run lint
```

Working directory: `frontend`

Outcome:

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

Exit code: `0`.

### Frontend Build

Initial sandboxed command:

```powershell
npm run build
```

Working directory: `frontend`

Initial result:

```text
Failed before build compilation: esbuild/Vite could not read "../../../.." and could not resolve frontend\vite.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm run build
```

Working directory: `frontend`

Escalated rerun result:

```text
vite v7.1.9 building for production...
135 modules transformed.
dist/index.html                 0.48 kB | gzip:   0.31 kB
dist/assets/index-DfLzCzBj.css  38.87 kB | gzip:   7.06 kB
dist/assets/index-p47zIFo3.js   850.58 kB | gzip: 256.93 kB
built in 6.86s
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings; existing chunk larger than 500 kB after minification warning.

### Skipped Checks

- Backend tests: not run because this slice changed only frontend components/tests and migration docs.
- Browser smoke: not run and not claimed; Docker/Postgres/seeded local environment availability remains the blocker recorded earlier in Phase 6 and Phase 7 docs.

### Post-Documentation Rerun

Commands:

```powershell
rg -n "publishedToOrganization|UpdateFrameworksButton|Publish to Organization|Unpublish from Organization|Organization sharing|Published to Organization|organization|Organization" frontend\src\components
rg -n "UpdateFrameworksButton" frontend\src
rg -n "tenantId|joinedOrganization|updateUserTenant|tenant_id|X-Tenant-ID|publishedToOrganization|organization|Organization|invite|Invite" frontend\src -g '!**/*.test.*'
git diff --check
```

Results:

```text
The active component org-sharing UI scan returned no stdout; `rg` exited 1.
The `UpdateFrameworksButton` scan returned no stdout; `rg` exited 1.
The remaining deferred frontend residue scan returned only `AuthContext.jsx` tenant/org state and `api.js` `publishedToOrganization` normalization.
`git diff --check` returned no stdout and exited 0.
```

## Frontend AuthContext Tenant/Org State Cleanup Verification - 2026-07-08

Scope: active frontend AuthContext tenant/org state cleanup only. `frontend/src/lib/api.js` identity-strip guard/request normalization, backend behavior, database models, migrations, API contracts, README, obsolete backend helper scripts, and browser smoke were not changed.

### Focused Pre-Edit AuthContext Inventory

Command:

```powershell
rg -n "tenantId|joinedOrganization|updateUserTenant" frontend\src
```

Outcome:

```text
frontend\src\contexts\AuthContext.jsx:24:    tenantId: existingUser?.tenantId || null,
frontend\src\contexts\AuthContext.jsx:25:    joinedOrganization: existingUser?.joinedOrganization || null,
frontend\src\contexts\AuthContext.jsx:125:  const updateUserTenant = async (tenantId, reload = false) => {
frontend\src\contexts\AuthContext.jsx:132:      tenantId,
frontend\src\contexts\AuthContext.jsx:162:    updateUserTenant,
```

Command:

```powershell
rg -n "useAuth\(|AuthProvider|AuthContext" frontend\src
```

Outcome summary:

```text
Active AuthContext consumers were `App.jsx`, `LandingPage.jsx`, `Login.jsx`, `Navbar.jsx`, `PrivateRoute.jsx`, and `YourFrameworks.jsx`, plus test mocks. These consumers used `user`, `loading`, `login`, `logout`, and `isAuthenticated`; none referenced `tenantId`, `joinedOrganization`, or `updateUserTenant`.
```

Command:

```powershell
rg -n "roles|expertProfile|isSuperAdmin|authProvider|backendUserId" frontend\src
```

Outcome summary:

```text
`roles` and `expertProfile` were limited to `AuthContext.jsx` tenant-update normalization. `isSuperAdmin` remains consumed by `Navbar.jsx`; `authProvider` appears in route/login tests; `backendUserId` remains AuthContext backend identity normalization.
```

### Files Changed

- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/contexts/AuthContext.test.jsx`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

### Focused AuthContext Test

Initial sandboxed command:

```powershell
npm test -- AuthContext.test.jsx
```

Working directory: `frontend`

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read "../../../.." and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm test -- AuthContext.test.jsx
```

Working directory: `frontend`

Escalated rerun result:

```text
1 test file passed.
2 tests passed.
Duration 1.25s.
```

Warning: existing stale `baseline-browser-mapping` warning.

### Post-Cleanup AuthContext Scans

Command:

```powershell
rg -n "tenantId|joinedOrganization|updateUserTenant" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n "roles|expertProfile" frontend\src\contexts\AuthContext.jsx frontend\src\contexts\AuthContext.test.jsx
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n "tenant_id|X-Tenant-ID|publishedToOrganization|organization|Organization|invite|Invite" frontend\src -g "!**/*.test.*"
```

Outcome:

```text
frontend\src\lib\api.js:385:    publishedToOrganization: Boolean(framework.publishedToOrganization),
```

Interpretation: exact removed AuthContext names are absent from `frontend/src`. The remaining non-test frontend org residue visible to this scan is the deferred `api.js` `publishedToOrganization` normalization. The `api.js` split-string `tenant_id` / `X-Tenant-ID` identity-strip guard and `api.test.js` negative assertions remain deferred by scope and were intentionally not rewritten in this slice.

### Full Frontend Tests

Command:

```powershell
npm test
```

Working directory: `frontend`

Outcome:

```text
10 test files passed.
55 tests passed.
Duration 4.38s.
```

Warnings/output: existing stdout from `PublishModal.test.jsx` and `Login.test.jsx`; existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Lint

Command:

```powershell
npm run lint
```

Working directory: `frontend`

Outcome:

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

Exit code: `0`.

### Frontend Build

Command:

```powershell
npm run build
```

Working directory: `frontend`

Outcome:

```text
vite v7.1.9 building for production...
135 modules transformed.
dist/index.html                 0.48 kB | gzip:   0.31 kB
dist/assets/index-DfLzCzBj.css  38.87 kB | gzip:   7.06 kB
dist/assets/index-BtLA-T-L.js   850.17 kB | gzip: 256.80 kB
built in 5.96s
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings; existing chunk larger than 500 kB after minification warning.

### Git Diff Check

Command:

```powershell
git diff --check
```

Outcome before documentation updates:

```text
No stdout. Command exited 0.
```

### Skipped Checks

- Backend tests: not run because this slice changed only frontend AuthContext/tests and migration docs.
- Browser smoke: not run and not claimed; Docker/Postgres/seeded local environment availability remains the blocker recorded earlier in Phase 6 and Phase 7 docs.

### Post-Documentation Rerun

Commands:

```powershell
rg -n "tenantId|joinedOrganization|updateUserTenant" frontend\src
rg -n "roles|expertProfile" frontend\src\contexts\AuthContext.jsx frontend\src\contexts\AuthContext.test.jsx
rg -n "tenant_id|X-Tenant-ID|publishedToOrganization|organization|Organization|invite|Invite" frontend\src -g "!**/*.test.*"
rg -n "\['tenant'|Tenant-ID|publishedToOrganization|tenant_id|X-Tenant-ID" frontend\src\lib\api.js frontend\src\lib\api.test.js
git diff --check
```

Results:

```text
The exact removed AuthContext name scan returned no stdout; `rg` exited 1.
The AuthContext legacy role/profile scan returned no stdout; `rg` exited 1.
The remaining non-test frontend residue scan returned only `frontend\src\lib\api.js:385` `publishedToOrganization` normalization.
The guard-specific scan confirmed the intentionally deferred `api.js` split-string `tenant_id` / `X-Tenant-ID` identity-strip guard and `api.test.js` negative assertions remain.
`git diff --check` returned no stdout and exited 0.
```

## Frontend API Request-Normalization Cleanup Verification - 2026-07-08

Scope: active frontend `api.js` request-normalization residue only. Backend auth/session behavior, backend ownership checks, database models, migrations, API contracts, README, obsolete backend helper scripts, and browser smoke were not changed.

### Focused Pre-Edit API Inventory

Commands:

```powershell
rg -n "tenant_id|X-Tenant-ID|publishedToOrganization|organization|Organization|invite|Invite|user_id|creator_id|owner_id|created_by|createdBy|tenantId|workspace|Workspace|account_id|accountId" frontend\src\lib
rg -n "publishedToOrganization|published_to_organization|publish.*organization|organization|Organization" frontend\src backend_py\app backend_py\tests -g "!frontend/src/lib/api.test.js"
rg -n "stripArtefactResourceFields|buildArtefactPayload|expectNoClientIdentityFields|client identity|identity fields|framework_id|user_id|creator_id|tenant_id|X-Tenant-ID" frontend\src\lib\api.js frontend\src\lib\api.test.js
rg -n "tenant_id|X-Tenant-ID|publishedToOrganization|organization|Organization|user_id|creator_id|framework_id|owner_id|created_by|createdBy|account_id|accountId|workspace_id|workspaceId" frontend\src -g "!**/*.test.*"
```

Outcome summary:

```text
`publishedToOrganization` was present in `frontend\src\lib\api.js` summary normalization.
The split-string artefact guard and `tenant_id` / `X-Tenant-ID` negative fixtures were present in `api.js` / `api.test.js`.
No active UI/backend flow outside `api.js` required `publishedToOrganization`; the backend `organization` hit was limited to the already-deferred `backend_py\app\api\vector_sync.py:19 include_organization`.
Non-test frontend client-owned identity hits outside `api.js` were backend response IDs in component code, not request-owned identity propagation.
```

### Files Changed

- `frontend/src/lib/api.js`
- `frontend/src/lib/api.test.js`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

### Focused Post-Edit Scans

Commands:

```powershell
rg -n "tenant_id|X-Tenant-ID|tenantId|joinedOrganization|updateUserTenant|publishedToOrganization|organization|Organization|invite|Invite" frontend\src\lib
rg -n "tenant_id|X-Tenant-ID|tenantId|joinedOrganization|updateUserTenant|publishedToOrganization|organization|Organization|invite|Invite" frontend\src\lib\api.js
rg -n "user_id|creator_id|framework_id|owner_id|accountId|created_by|updatedBy|X-Owner-ID|password_hash" frontend\src\lib
git diff -- frontend\src\lib\api.js frontend\src\lib\api.test.js
```

Results:

```text
The broad frontend/src/lib legacy scan returned only `api.test.js` negative assertions for `publishedToOrganization` / organization-sharing summary normalization.
The `api.js` runtime scan returned no stdout; `rg` exited 1.
The client-owned identity scan returned matches only in `api.test.js` negative fixtures and backend response shape fixtures.
The diff showed `api.js` removed the split-string tenant/header guard, added generic identity-field stripping, and removed `publishedToOrganization` summary normalization.
```

### Focused API Test

Initial sandboxed command:

```powershell
npm test -- src/lib/api.test.js
```

Working directory: `frontend`

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read "../../../.." and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm test -- src/lib/api.test.js
```

Working directory: `frontend`

Escalated rerun result:

```text
1 test file passed.
24 tests passed.
Duration 2.22s.
```

Warning: existing stale `baseline-browser-mapping` warning.

### Full Frontend Tests

Command:

```powershell
npm test
```

Working directory: `frontend`

Outcome:

```text
10 test files passed.
56 tests passed.
Duration 8.22s.
```

Warnings/output: existing stdout from `PublishModal.test.jsx` and `Login.test.jsx`; existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Lint

Command:

```powershell
npm run lint
```

Working directory: `frontend`

Outcome:

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

Exit code: `0`.

### Frontend Build

Initial sandboxed command:

```powershell
npm run build
```

Working directory: `frontend`

Initial result:

```text
Failed before build compilation: esbuild/Vite could not read "../../../.." and could not resolve frontend\vite.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm run build
```

Working directory: `frontend`

Escalated rerun result:

```text
vite v7.1.9 building for production...
135 modules transformed.
dist/index.html                 0.48 kB | gzip:   0.31 kB
dist/assets/index-DfLzCzBj.css  38.87 kB | gzip:   7.06 kB
dist/assets/index-DovgRqZ9.js   850.25 kB | gzip: 256.85 kB
built in 7.28s
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings; existing chunk larger than 500 kB after minification warning.

### Required Focused Scans And Whitespace Check

Commands:

```powershell
rg -n "tenant_id|X-Tenant-ID" frontend\src\lib
rg -n "publishedToOrganization" frontend\src\lib
rg -n "organization|Organization" frontend\src\lib
rg -n "user_id|creator_id|framework_id|owner_id|accountId|created_by|updatedBy|X-Owner-ID|password_hash" frontend\src\lib
git diff --check
```

Results:

```text
The `tenant_id|X-Tenant-ID` scan returned no stdout; `rg` exited 1.
The `publishedToOrganization` scan returned only `frontend\src\lib\api.test.js` negative assertion matches.
The `organization|Organization` scan returned only `frontend\src\lib\api.test.js` negative assertion text for obsolete organization-sharing summary normalization.
The client-owned identity field scan returned matches only in `frontend\src\lib\api.test.js` negative fixtures, backend response shape fixtures, and the existing password-hash negative assertion.
`git diff --check` returned no stdout and exited 0.
```

### Skipped Checks

- Backend tests: not run because this slice changed only frontend API helper/tests and migration docs.
- Browser smoke: not run and not claimed; Docker/Postgres/seeded local environment availability remains the blocker recorded earlier in Phase 6 and Phase 7 docs.

### Post-Documentation Rerun

Commands:

```powershell
rg -n "tenant_id|X-Tenant-ID" frontend\src\lib
rg -n "publishedToOrganization" frontend\src\lib
rg -n "organization|Organization" frontend\src\lib
rg -n "user_id|creator_id|framework_id|owner_id|accountId|created_by|updatedBy|X-Owner-ID|password_hash" frontend\src\lib
git diff --check
```

Results:

```text
The `tenant_id|X-Tenant-ID` scan returned no stdout; `rg` exited 1.
The `publishedToOrganization` scan returned only `frontend\src\lib\api.test.js` negative assertion matches.
The `organization|Organization` scan returned only `frontend\src\lib\api.test.js` negative assertion text for obsolete organization-sharing summary normalization.
The client-owned identity field scan returned matches only in `frontend\src\lib\api.test.js` negative fixtures, backend response shape fixtures, and the existing password-hash negative assertion.
`git diff --check` returned no stdout and exited 0.
```

## Obsolete Current Docs/Scripts Cleanup Verification - 2026-07-09

Scope: current README/user docs, obsolete top-level backend helper scripts, obsolete helper docs, and Phase 7 documentation. No runtime app code, backend auth/session behavior, database models, migrations, ownership checks, API contracts, frontend routes, Agent/RAG/LLMWiki/Tool Registry/Chat UI/MCP code, public registration, org sharing, invites, or workspaces were changed.

### Focused Pre-Edit Inventory

Command:

```powershell
rg -n --hidden -S "Valorie|valorie|valorie\.ai|expert\.valorie\.ai|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw|Firebase|Firestore|Firebase Auth|OpenAI Vector Store|SaaS|tenant|Tenant|organization|Organization|invite|Invite|MigrationTool|migrate-data|cleanupData|updateFrameworkTenants|migrate tool|migration tool" README.md Project-Startup-and-Operation-Flow.md firebaseDoc.md docs backend_py -g "*.md" -g "*.py" -g "*.sh" -g "*.ps1" -g "*.js" -g "*.jsx" -g "!docs/migration/phases/**" -g "!backend_py/.venv/**" -g "!backend_py/app/**" -g "!backend_py/tests/**"
```

Outcome summary:

```text
Stale active/current docs and helper hits were found in README.md, Project-Startup-and-Operation-Flow.md, firebaseDoc.md, backend_py/README-DIFF.md, backend_py/check_vector_store_attributes.py, backend_py/test_firebase.py, backend_py/test_update.py, and backend_py/test_update_publish.py.
docs/CN_DEPLOY.md did not contain stale legacy setup instructions and was preserved.
backend_py/diagnose_env.py did not contain stale legacy setup instructions and was preserved because it checks the current DeepSeek/provider env path.
docs/migration/README.md, docs/migration/decisions/ADR-0001-auth-strategy.md, and docs/skills/** retained migration decision/tooling references rather than current setup instructions.
```

### Deleted Helper Dependency Proof

Command:

```powershell
rg -n --hidden -S "Project-Startup-and-Operation-Flow\.md|firebaseDoc\.md|README-DIFF\.md|test_firebase\.py|test_cloud_llm\.py|test_update\.py|test_update_publish\.py|test_vec_base\.py|check_versions\.py|check_vector_store_attributes\.py|diagnose_env\.py" . -g "!docs/migration/phases/**" -g "!backend_py/.venv/**" -g "!frontend/node_modules/**" -g "!frontend/dist/**" -g "!.git/**"
```

Pre-delete outcome summary:

```text
No active runtime imports or current workflow references depended on the obsolete helper scripts.
Matches were limited to canonical migration instructions, migration-reviewer scan prompts, obsolete backend_py/README-DIFF.md references, and self-comments in the helper scripts.
```

### Files Changed

- `README.md`
- `docs/migration/decisions/ADR-0001-auth-strategy.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

### Files Deleted

- `Project-Startup-and-Operation-Flow.md`
- `firebaseDoc.md`
- `backend_py/README-DIFF.md`
- `backend_py/check_versions.py`
- `backend_py/check_vector_store_attributes.py`
- `backend_py/test_cloud_llm.py`
- `backend_py/test_firebase.py`
- `backend_py/test_update.py`
- `backend_py/test_update_publish.py`
- `backend_py/test_vec_base.py`

### Active README Stale-Reference Scan

Command:

```powershell
rg -n --hidden -S "Valorie|valorie|valorie\.ai|expert\.valorie\.ai|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw|Firebase|Firestore|Firebase Auth|OpenAI Vector Store|SaaS|tenant|Tenant|organization|Organization|invite|Invite|MigrationTool|migrate-data|cleanupData|updateFrameworkTenants|migrate tool|migration tool" README.md
```

Result:

```text
No stdout. `rg` exited 1.
```

### Current Docs/Scripts Stale-Reference Scan

Command:

```powershell
rg -n --hidden -S "Valorie|valorie|valorie\.ai|expert\.valorie\.ai|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw|Firebase|Firestore|Firebase Auth|OpenAI Vector Store|SaaS|tenant|Tenant|organization|Organization|invite|Invite|MigrationTool|migrate-data|cleanupData|updateFrameworkTenants|migrate tool|migration tool" README.md docs backend_py -g "*.md" -g "*.py" -g "*.sh" -g "*.ps1" -g "*.js" -g "*.jsx" -g "!docs/migration/phases/**" -g "!backend_py/.venv/**" -g "!backend_py/app/**" -g "!backend_py/tests/**"
```

Result:

```text
docs\skills\migration-reviewer\SKILL.md:40:- Legacy isolation: Are Firebase, GCP LLM, OpenAI Vector Store, tenant-era paths, and old docs either removed, guarded, or explicitly deferred?
docs\skills\migration-phase-planner\SKILL.md:75:rg -n "OpenAI|Firebase|Vector Store|GCP|LOCAL_LLM|tenant" backend_py frontend docs
docs\migration\README.md:20:Phase 0 locks the Auth strategy to option A: self-hosted backend JWT, allowlist, and no public registration. Firebase Auth and Firebase ID Token are not part of the new project route.
docs\migration\decisions\ADR-0001-auth-strategy.md:9:The legacy project mixed Firebase Auth, backend-local JWT, and frontend-provided `user_id` values in request body, query, or form data. This created a severe identity trust-chain problem because private backend actions could trust user identity supplied by the client instead of deriving identity from a verified token.
docs\migration\decisions\ADR-0001-auth-strategy.md:17:- Frontend Firebase Auth was removed from the active frontend route in Phase 6.
docs\migration\decisions\ADR-0001-auth-strategy.md:20:- Firebase ID Token is not the main route for the new project.
```

Interpretation: remaining matches are allowlisted migration decision evidence and migration tooling scan prompts. They are not active app setup docs, runtime source, config, deploy scripts, or user workflow instructions.

### Deleted File Presence Checks

Commands:

```powershell
rg --files backend_py -g "test_firebase.py" -g "test_cloud_llm.py" -g "test_update.py" -g "test_update_publish.py" -g "test_vec_base.py" -g "check_versions.py" -g "check_vector_store_attributes.py" -g "README-DIFF.md"
rg --files -g "Project-Startup-and-Operation-Flow.md" -g "firebaseDoc.md"
```

Results:

```text
Both commands returned no stdout; `rg` exited 1.
```

### Deleted File Reference Scan

Command:

```powershell
rg -n --hidden -S "Project-Startup-and-Operation-Flow\.md|firebaseDoc\.md|README-DIFF\.md|test_firebase\.py|test_cloud_llm\.py|test_update\.py|test_update_publish\.py|test_vec_base\.py|check_versions\.py|check_vector_store_attributes\.py" . -g "!docs/migration/phases/**" -g "!backend_py/.venv/**" -g "!frontend/node_modules/**" -g "!frontend/dist/**" -g "!.git/**"
```

Result summary:

```text
Matches remain only in `MIGRATION_PHASES.md`, where the canonical plan names obsolete docs/scripts as Phase 7 cleanup targets, and in `docs\skills\migration-reviewer\SKILL.md`, where a review prompt scans for stale audit/startup docs.
```

Interpretation: remaining references are canonical migration instructions or migration-reviewer scan prompts, not active workflows depending on the deleted files.

### Backend Residue Classification Scan

Command:

```powershell
rg -n "tenant|Tenant|organization|Organization|invite|Invite|X-Tenant-ID|include_organization" backend_py\app backend_py\alembic backend_py\tests -g "!backend_py/.venv/**"
```

Result:

```text
backend_py\tests\test_main.py:40:def test_cors_preflight_omits_legacy_tenant_header(monkeypatch):
backend_py\tests\test_main.py:67:    assert "X-Tenant-ID" not in allowed_headers
backend_py\app\api\vector_sync.py:19:    include_organization: bool = True
```

Interpretation: `backend_py/tests/test_main.py` remains an allowlisted negative CORS assertion. `backend_py/app/api/vector_sync.py` remains a Phase 9-deferred RAG/indexing stub and was intentionally not changed because this slice did not alter runtime API contracts.

### Whitespace Check

Command:

```powershell
git diff --check
```

Result:

```text
No stdout. Command exited 0.
```

### Browser Smoke Feasibility Check

Command:

```powershell
docker compose ps
```

Result:

```text
Warnings: JWT_SECRET_KEY and DEEPSEEK_API_KEY were not set; docker-compose.yml `version` is obsolete.
Failed to connect to the Docker API at npipe:////./pipe/dockerDesktopLinuxEngine. The system cannot find the file specified.
Command exited 1.
```

Interpretation: browser smoke was not run because Docker Desktop's Linux engine is unavailable, leaving no live Docker/Postgres/backend/frontend environment or seeded credentials for a smoke session.

### Skipped Checks

- Script syntax checks: not run because obsolete scripts were deleted, and no current script was edited.
- Frontend tests/lint/build: not run because no frontend runtime or test code changed in this slice.
- Backend tests: not run because no backend runtime app code, maintained backend tests, database models, migrations, auth/session, ownership checks, or API contracts changed in this slice.
- Browser smoke: not run and not claimed; `docker compose ps` could not connect to Docker Desktop's Linux engine pipe, leaving no live Docker/Postgres/backend/frontend environment with seeded credentials in this turn.

## Initial Planning Scan Summary

These scans were run only to ground planning. They are not acceptance evidence for completed implementation.

### Phase 7 Canonical Section

Command:

```powershell
$lines = Get-Content -Encoding UTF8 -LiteralPath 'MIGRATION_PHASES.md'; $lines[377..425]
```

Result summary:

- Phase 7 target: remove Valorie/UNSW/customer-specific strings, one-time scripts, and unnecessary multi-tenant paths.
- Phase 7 acceptance now requires active-surface zero matches instead of unconditional repo-wide zero matches.
- Canonical steps include domain/brand env cleanup, deleting migration scripts/routes, removing tenant/org/invite components and routes, cleaning nginx/deploy scripts, deleting or rewriting obsolete docs, and removing obsolete backend helper scripts/tests.

### Active Domain And Customer String Planning Scan

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|valorie\.ai|framework-builder-55896|webmaster@valorie|APP_BASE_DOMAIN|APP_NAME|SUPER_ADMIN_EMAIL" . -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" -g "!.git"
```

Result summary:

- Active hits include `.env.example`, `backend_py/.env.example`, `backend_py/alembic.ini`, `backend_py/main.py`, `frontend/src/lib/api.js`, `LandingPage.jsx`, `Login.jsx`, `Navbar.jsx`, `docker-compose.yml`, `docker-entrypoint.sh`, `deploy.sh`, and `nginx-valorie.conf`.
- Historical hits also exist in `MIGRATION_PHASES.md` and prior `docs/migration/phases/**` records; only `docs/migration/phases/**` historical records may be allowlisted under the canonical rule.

### Tenant/Org/Invite/Migration Planning Scan

Command:

```powershell
rg -n --hidden -S "tenant|Tenant|organization|Organization|org|invite|Invite|MigrationTool|migrate-data|cleanupData|updateFrameworkTenants" frontend/src backend_py docs README.md Dockerfile docker-compose.yml nginx.conf .env.example -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv"
```

Result summary:

- Active frontend route hits include `App.jsx`, `TenantRoute.jsx`, `TenantSettings.jsx`, `TenantCreationModal.jsx`, `YourOrganization.jsx`, `InviteAccept.jsx`, `MigrationTool.jsx`, `Navbar.jsx`, `CreateFramework.jsx`, `FrameworkEditor.jsx`, `FrameworkCard.jsx`, and `YourFrameworks.jsx`.
- Phase 6 isolated placeholders include `migrate-data.js`, `cleanupData.js`, `DataCleanupButton.jsx`, and `updateFrameworkTenants.js`.
- Test hits exist in route/component/API tests, some as intentional negative assertions.
- `nginx.conf` does not exist; the active legacy nginx file is `nginx-valorie.conf`.

### Backend Tenant/Invite Router Planning Scan

Command:

```powershell
rg -n --hidden -S "APIRouter|tenants|tenant|invite|organization|workspace|X-Tenant-ID" backend_py/app backend_py/alembic backend_py/tests -g "!backend_py/.venv"
```

Result summary:

- No `/api/tenants/*` router was found in `backend_py/app`.
- `backend_py/app/api/vector_sync.py` contains `include_organization`.
- `backend_py/main.py` CORS preflight still allows `Authorization, X-Tenant-ID`.

### Obsolete Script And Doc Planning Scan

Command:

```powershell
rg --files -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" | rg -i "firebase|Project-Startup|README-DIFF|deploy|nginx|test_|check_|diagnose|migrate|cleanup|tenant|organization|invite"
```

Result summary:

- Likely obsolete docs: `Project-Startup-and-Operation-Flow.md`, `firebaseDoc.md`, `backend_py/README-DIFF.md`, and possibly current README sections.
- Likely obsolete backend helper scripts: `backend_py/test_firebase.py`, `backend_py/test_cloud_llm.py`, `backend_py/test_update.py`, `backend_py/test_update_publish.py`, `backend_py/test_vec_base.py`, `backend_py/check_versions.py`, `backend_py/check_vector_store_attributes.py`, and `backend_py/diagnose_env.py`.
- Maintained pytest files under `backend_py/tests/**` should not be deleted just because their names match `test_*`.

## Planned Round Verification

### Round 0 - Inventory

Record:

- Exact inventory commands and full or summarized outputs.
- Match classification table.
- Allowlist policy for historical migration docs and intentional security/negative assertion tests, recorded in both this document and `phase-report.md`.

### Round 1 - Domain And Brand Cleanup

Suggested scans:

```powershell
rg -n --hidden -S "valorie\.ai|expert\.valorie\.ai|webmaster@valorie|framework-builder-55896|UNSW|ad\.unsw" backend_py/app frontend/src .env.example backend_py/.env.example Dockerfile docker-compose.yml docker-entrypoint.sh deploy.sh nginx-valorie.conf -g "!frontend/dist"
rg -n "APP_BASE_DOMAIN|APP_NAME|SUPER_ADMIN_EMAIL|FRONTEND_URL|ALLOWED_ORIGINS|Access-Control-Allow-Origin" backend_py/main.py .env.example backend_py/.env.example frontend/src/lib/api.js
```

Expected evidence:

- Active runtime/config/deploy/current README/user docs and active tests no longer contain forbidden legacy Valorie/customer strings, except explicitly allowlisted security/negative assertion tests.
- Backend CORS remains explicit for local dev and configured production origins.
- Frontend API base URL logic supports local dev and configured deployment.

Minimum tests:

```powershell
cd frontend
npm run lint
npm test
npm run build
```

Run focused backend tests if `backend_py/main.py` changes.

### Round 2 - Migration Tool Placeholder Removal

Suggested scans:

```powershell
Test-Path frontend/src/migrate-data.js
Test-Path frontend/src/utils/cleanupData.js
Test-Path frontend/src/utils/DataCleanupButton.jsx
Test-Path frontend/src/utils/updateFrameworkTenants.js
Test-Path frontend/src/components/MigrationTool.jsx
rg -n "MigrationTool|migrate-data|cleanupData|DataCleanupButton|updateFrameworkTenants|/migrate" frontend/src
```

Expected evidence:

- Deleted placeholders are absent.
- `/migrate` route is gone.
- No active imports remain.

### Round 3 - Personal Route Flow Cleanup

Suggested scans:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept|/:tenantId|/invite/:token|joinedOrganization|getCurrentTenantId|publishedToOrganization|Publish to Organization|Tenant Settings|My Organization" frontend/src
rg -n "tenantId|tenant_id|X-Tenant-ID|organization|invite" frontend/src -g "!**/*.test.*"
```

Expected evidence:

- Personal route flow uses non-tenant paths.
- Tenant/org/invite components are deleted or no longer active.
- Organization-sharing UI and inert alerts are gone.
- Any remaining test-only legacy strings are intentional security/negative assertions and are explicitly allowlisted in both this document and `phase-report.md`.

Suggested behavior tests:

- Root authenticated redirect lands on `/frameworks`.
- Login lands on `/frameworks`.
- Framework list create/editor navigation uses personal routes.
- Removed routes return not found or redirect predictably.
- Library remains authenticated.
- Admin remains backend-authorized.

### Round 4 - Backend/Deploy/Env/Nginx Cleanup

Suggested scans:

```powershell
rg -n "valorie|Valorie|expert\.valorie\.ai|tenant|X-Tenant-ID|nginx-valorie" Dockerfile docker-compose.yml docker-entrypoint.sh deploy.sh nginx-framework.conf .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py backend_py/app
Test-Path nginx-valorie.conf
rg -n "container_name|image:|POSTGRES_DB|POSTGRES_USER|DATABASE_URL" docker-compose.yml .env.example backend_py/.env.example backend_py/alembic.ini
```

Expected evidence:

- Deploy/config files no longer reference Valorie domains, tenant subdomains, or nginx tenant headers.
- Local dev defaults remain coherent.
- Backend tests pass if backend code changes.

### Round 5 - Obsolete Docs, Scripts, And Tests Cleanup

Suggested scans:

```powershell
rg -n --hidden -S "Firebase|Firestore|Firebase Auth|OpenAI Vector Store|test_firebase|test_vec_base|tenant invite|expert\.valorie\.ai|valorie\.ai|100%" README.md Project-Startup-and-Operation-Flow.md firebaseDoc.md backend_py/README-DIFF.md docs/CN_DEPLOY.md
rg --files backend_py | rg -i "test_firebase|test_cloud_llm|test_update|test_vec_base|check_versions|check_vector_store_attributes|diagnose_env|README-DIFF"
```

Expected evidence:

- Current docs no longer instruct users to use obsolete Firebase/Firestore/tenant invite workflows.
- Obsolete helper scripts are deleted or rewritten into maintained scripts.
- Maintained pytest suite remains under `backend_py/tests/**`.

### Round 6 - Closeout

Required commands:

```powershell
cd frontend
npm run lint
npm test
npm run build
```

Run when backend code changed:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Always run:

```powershell
git diff --check
```

Browser smoke checklist, only if local environment is available:

- [ ] Login with a backend-created user.
- [ ] Confirm login sets/uses cookies and stores no frontend token.
- [ ] Refresh page and remain logged in.
- [ ] Confirm root redirects to `/frameworks`.
- [ ] Load owner framework list.
- [ ] Create or generate a framework.
- [ ] Open and save a framework.
- [ ] Load Library as authenticated user.
- [ ] Publish and unpublish an owned framework.
- [ ] Access AdminPanel as super-admin.
- [ ] Confirm non-admin admin access fails.
- [ ] Logout and confirm private routes require login.
- [ ] Confirm removed tenant/org/invite/migration routes are not active.

If browser smoke cannot run, record the exact blocker and leave every browser checklist item unchecked.

## Reviewer Handoff Evidence

The final Phase 7 handoff should include:

- Round-by-round changed/deleted/rewritten file list.
- Final inventory classification and any allowlist, recorded in both this document and `phase-report.md`.
- Exact static scan commands and outputs.
- Exact frontend lint/test/build commands and outputs.
- Exact backend test commands and outputs when applicable.
- Browser smoke notes, either actual results or blocker.
- Confirmation that personal-use auth boundaries remain enforced.
- Confirmation that no future-phase features were added.
- Confirmation that Phase 7 semantic cleanup did not claim Phase 8+ work.

## Known Planning Risks

- Historical migration docs contain legacy strings by design; only `docs/migration/phases/**` historical records may retain them, and only with explicit allowlist entries.
- Route cleanup will affect multiple frontend tests and navigation helpers at once.
- Domain/CORS cleanup is security-sensitive because cookie auth depends on correct origin handling.
- Docker/Postgres unavailability may continue to block browser smoke.
