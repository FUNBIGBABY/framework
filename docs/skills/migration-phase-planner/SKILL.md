---
name: migration-phase-planner
description: Plan migration phases for Michael's framework-to-personal-AI-Agent project in the repository containing MIGRATION_PHASES.md and docs/migration/phases. Use when explicitly invoked or when Codex is asked in this project to scope a phase, split work into rounds, create or update phase planning documentation, clarify migration plan details, identify risks and tests before implementation, or prepare an executor/reviewer handoff without writing code or performing code review.
---

# Migration Phase Planner

## Purpose

Use this skill to plan migration work before implementation. The planner reconciles owner ideas, canonical docs, prior phase records, and focused repo facts into a concrete phase plan. Treat `MIGRATION_PHASES.md` as canonical, `docs/PERSONAL_USE_BOUNDARY.md` as binding, and `docs/migration/phases/<phase>/` as the execution contract.

## Planning Rules

- Do not implement backend, frontend, test, migration, or infrastructure code.
- Do not perform code review or decide whether completed implementation can be accepted; use the reviewer skill for that.
- Keep `MIGRATION_PHASES.md` canonical. Call out any conflict between owner ideas, existing phase docs, repo facts, and the canonical plan.
- Treat `docs/PERSONAL_USE_BOUNDARY.md` as binding for privacy, tenancy, auth, deployment, and personal-use constraints.
- Require `docs/migration/README.md` and relevant ADRs as context before planning.
- Avoid scope creep into future phases. Identify future work as non-goals or explicit deferrals with owning phase.
- Recommend one path. Mention alternatives only when they explain the recommendation or a tradeoff.
- Create or update planning docs only when the user asks for documentation changes.
- Make only narrow canonical-plan clarifications when explicitly asked and the clarification preserves canonical intent.

## Required Read Order

1. `MIGRATION_PHASES.md`
2. `docs/PERSONAL_USE_BOUNDARY.md`
3. `docs/migration/README.md`
4. Relevant ADRs in `docs/migration/decisions/`
5. Prior phase docs under `docs/migration/phases/`
6. Existing current phase docs if present
7. Focused repo scans only as needed to ground planning

## Planning Workflow

1. Identify the target phase, current state, and any user-provided goal or constraint.
2. Read the required context in order. Prefer focused reads over broad repo sweeps.
3. Compare owner ideas and current phase docs against `MIGRATION_PHASES.md`, the personal-use boundary, migration README, and ADRs.
4. Inspect only the repo areas needed to ground file/module estimates, risk, compatibility, and tests.
5. Define the recommended phase and round breakdown, including sequence, dependencies, and stopping points.
6. Define scope, non-goals, likely files/modules, risks, tests, verification, docs, and handoff criteria.
7. If asked to write docs, update the relevant phase planning files under `docs/migration/phases/<phase>/` and keep the execution contract internally consistent.
8. If useful, include a suggested first Executor prompt that is narrow enough for implementation.

## Planning Output

Include these sections unless the user asks for a narrower artifact:

- Recommended phase/round breakdown.
- Scope and non-goals.
- Files or modules likely involved.
- Security risks, especially auth, identity, secrets, file access, tool permissions, and private data.
- Compatibility risks, including frontend/backend contracts, persistence, config, deployment, and legacy behavior.
- Documentation updates needed.
- Testing strategy.
- Verification checklist.
- Reviewer handoff criteria.
- Suggested first Executor prompt only when useful.

## Documentation Standards

- Keep phase docs under `docs/migration/phases/<phase>/` as the execution contract for the executor.
- Do not mark implementation tasks complete during planning.
- Record unresolved conflicts as planning blockers or decisions needed, not as completed work.
- Keep canonical-plan edits rare and explicit. Prefer phase-level clarifications unless the canonical plan itself must change.
- Preserve prior phase records. Add new planning context instead of rewriting history unless the user explicitly asks for cleanup.

## Useful Scans

Adapt scans to the phase. Use `rg` and focused file reads to ground planning without drifting into review:

```powershell
rg -n "Phase [0-9]+|docs/migration/phases" MIGRATION_PHASES.md docs/migration
rg -n "user_id|auth|session|secret|token|upload|private" backend_py/app frontend/src
rg -n "OpenAI|Firebase|Vector Store|GCP|LOCAL_LLM|tenant" backend_py frontend docs
rg -n "TODO|Deferred|Handoff|Risk|Verification" docs/migration/phases
```

Use scan results to estimate scope and risks. Do not turn scans into acceptance findings unless the user explicitly requested review.

## Handoff Format

End planning work with:

- Recommended plan and why.
- Scope boundaries and non-goals.
- Key risks and mitigations.
- Testing and verification checklist.
- Docs created or updated, if any.
- Conflicts with canonical docs or owner ideas.
- Executor prompt, when useful.
