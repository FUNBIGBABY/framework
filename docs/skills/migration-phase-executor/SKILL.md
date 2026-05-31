---
name: migration-phase-executor
description: Execute phase-based migrations for Michael's framework-to-personal-AI-Agent project in the repository containing MIGRATION_PHASES.md and docs/migration/phases. Use when explicitly invoked or when Codex is asked in this project to implement or repair a migration phase, close review findings, update code and matching phase documentation, run verification, or prepare a handoff for the reviewer.
---

# Migration Phase Executor

## Purpose

Use this skill to implement migration work in a single coherent change: code, tests, phase docs, and verification records must move together. Treat `MIGRATION_PHASES.md` as the canonical plan and `docs/migration/phases/<phase>/` as the execution record.

## Operating Rules

- Work from the current phase or the explicit review findings. Do not start unrelated future phases.
- Preserve user and prior-agent changes. Read before editing; do not revert unrelated dirty files.
- Prefer existing repo patterns over new abstractions unless the phase requires one.
- Keep code comments sparse and useful.
- Never mark a checklist item complete unless code and verification support it.
- If a planned item is intentionally deferred, record the deferral with owner phase and reason.

## Required Read Order

1. `MIGRATION_PHASES.md`
2. `docs/migration/README.md`
3. Relevant ADRs in `docs/migration/decisions/`
4. Current phase `checklist.md`, `phase-report.md`, and `verification.md`
5. Prior phase handoff notes only when they define dependencies

## Execution Workflow

1. Identify the target phase, blockers, and exact acceptance criteria.
2. Inspect current code paths before editing. Use `rg` for scans and read focused files.
3. Make the smallest implementation that satisfies the phase contract.
4. Update or add tests proportional to risk.
5. Run targeted checks first, then the phase-required suite when feasible.
6. Update phase docs:
   - `checklist.md`: actual completed/remaining items.
   - `phase-report.md`: scope, files changed, decisions, known deferrals, handoff.
   - `verification.md`: commands run, exact results, warnings, skipped checks and why.
7. Re-run relevant scans after documentation changes.
8. Final response must summarize code changes, docs updated, tests run, and residual risks.

## Documentation Standards

- Keep `MIGRATION_PHASES.md` canonical. Edit it only when the plan itself is wrong or the user asks to change the plan.
- Keep phase reports factual. Do not write "passed" for a command that was not run.
- If a command could not run because of missing secrets, network, or environment, record it as not run with the concrete reason.
- Keep historical reports intact unless they contain active handoff instructions that now point to deleted or wrong files.

## Verification Baseline

Choose checks that match the phase, but default to:

- Backend syntax: `python -m py_compile` or `python -m compileall -q backend_py/app`
- Backend tests: `.venv\Scripts\python.exe -m pytest -q` from `backend_py` when available
- Frontend tests: `npm test -- --run --configLoader runner` from `frontend`
- Legacy scans: use `rg` for forbidden direct SDK calls, hardcoded secrets, stale model names, and frontend-provided `user_id`

Do not install dependencies or use network without user approval.

## Handoff Format

End implementation work with:

- What changed in code.
- What changed in docs.
- Verification commands and outcomes.
- Remaining deferrals with the phase that owns them.
- Any reviewer attention points.
