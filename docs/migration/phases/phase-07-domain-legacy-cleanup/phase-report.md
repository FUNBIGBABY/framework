# Phase 07 Report - Domain and Legacy Cleanup

Planning status: documentation only. No Phase 7 implementation has been performed in this report, and Phase 7 is not complete. Phase 7 planning relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

## Status

This initial report creates the Phase 7 planning record after the Phase 6 frontend de-Firebase closeout docs were corrected to record Migration Reviewer acceptance.

Current Phase 7 state:

- Planning package created: `checklist.md`, `phase-plan.md`, `verification.md`, and this `phase-report.md`.
- Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance.
- Phase 6 Round 6 closeout commit is `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- Phase 7 scope is semantic cleanup of Valorie/domain, tenant/org/invite/migration residue, obsolete docs, obsolete scripts/tests, and legacy deploy/env naming.
- Phase 6 browser smoke remains documented as deferred because Docker/Postgres/seeded local environment was unavailable.
- Phase 7 implementation has not started.
- Phase 7 must not be marked complete before implementation evidence and reviewer acceptance.
- If Phase 6 closeout docs do not record accepted status in a future checkout, Phase 7 implementation is gated until that documentation contradiction is corrected.

## Required Context Read For Planning

- `MIGRATION_PHASES.md`
- `docs/PERSONAL_USE_BOUNDARY.md`
- `docs/migration/README.md`
- `docs/migration/decisions/ADR-0001-auth-strategy.md`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`
- Local planner skill instructions at `docs/skills/migration-phase-planner/SKILL.md`

## Planning Inventory Snapshot

Focused planning scans found likely Phase 7 work in these categories.

Active domain/app naming residue:

- `.env.example`
- `backend_py/.env.example`
- `backend_py/alembic.ini`
- `backend_py/main.py`
- `frontend/src/lib/api.js`
- `frontend/src/components/LandingPage.jsx`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/Navbar.jsx`
- `docker-compose.yml`
- `docker-entrypoint.sh`
- `deploy.sh`
- `nginx-valorie.conf`

Tenant/org/invite/migration route residue:

- `frontend/src/App.jsx`
- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/lib/api.js`
- `frontend/src/components/TenantRoute.jsx`
- `frontend/src/components/TenantCreationModal.jsx`
- `frontend/src/components/TenantSettings.jsx`
- `frontend/src/components/YourOrganization.jsx`
- `frontend/src/components/InviteAccept.jsx`
- `frontend/src/components/MigrationTool.jsx`
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/CreateFramework.jsx`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/YourFrameworks.jsx`
- related frontend route/component tests

Phase 6 isolated placeholders:

- `frontend/src/migrate-data.js`
- `frontend/src/utils/cleanupData.js`
- `frontend/src/utils/DataCleanupButton.jsx`
- `frontend/src/utils/updateFrameworkTenants.js`

Obsolete docs and helper scripts:

- `README.md`
- `Project-Startup-and-Operation-Flow.md`
- `firebaseDoc.md`
- `backend_py/README-DIFF.md`
- `docs/CN_DEPLOY.md`
- `backend_py/test_firebase.py`
- `backend_py/test_cloud_llm.py`
- `backend_py/test_update.py`
- `backend_py/test_update_publish.py`
- `backend_py/test_vec_base.py`
- `backend_py/check_versions.py`
- `backend_py/check_vector_store_attributes.py`
- `backend_py/diagnose_env.py`

Backend scan note:

- No current `/api/tenants/*` router was found in `backend_py/app`.
- `backend_py/app/api/vector_sync.py` still contains `include_organization`; it should be reviewed carefully because the route is Phase 9-deferred indexing residue, not an active org-sharing system.

## Canonical Acceptance Decision

The canonical Phase 7 acceptance text in `MIGRATION_PHASES.md` has been amended from unconditional repo-wide zero matches to active-surface zero matches for legacy strings such as `valorie.ai`, `framework-builder-55896`, `webmaster@valorie`, `UNSW`, and `ad.unsw`.

Canonical rule recorded in `phase-plan.md` and `verification.md`:

- Active surfaces are runtime source, config, deploy scripts, current README/user docs, and active tests.
- Active-surface scans must reach zero forbidden legacy-string matches, except explicitly allowlisted security/negative assertion tests.
- Historical migration records under `docs/migration/phases/**` may retain legacy strings only with an explicit allowlist.
- The allowlist must be recorded in both this report and `verification.md`.
- The allowlist must not hide active runtime/config/deploy/current-doc residue.

## Allowlist Record

No Phase 7 implementation allowlist has been populated yet. Before Phase 7 can close, any retained historical migration-record matches or intentional security/negative assertion test matches must be listed here and in `verification.md` with file paths, matched terms, and rationale.

## Scope

Included:

- Valorie/domain naming cleanup.
- Tenant/org/invite/migration residue cleanup.
- Legacy migration tools and inert placeholders left from Phase 6.
- Obsolete docs cleanup or rewrite.
- Obsolete scripts/tests cleanup.
- Env/deploy/nginx naming cleanup where it is legacy-domain residue.
- Route cleanup for personal-use app flow.

Excluded:

- Agent loop or Tool Registry.
- RAG indexing, retrieval, or citations.
- LLMWiki.
- Chat UI or Skill Registry.
- MCP marketplace.
- Public registration.
- SaaS tenant/org sharing model.
- New invite system.
- Broad UI redesign.
- Browser smoke claim unless actually run.

## Recommended Round Breakdown

Round 0: fresh inventory and boundary confirmation.

Round 1: domain, brand, and active runtime naming cleanup.

Round 2: legacy migration tool and placeholder removal.

Round 3: personal route flow and tenant/org/invite cleanup.

Round 4: backend, deploy, env, and nginx legacy naming cleanup.

Round 5: obsolete docs, scripts, and tests cleanup.

Round 6: verification, documentation closeout, and reviewer handoff.

## Open Risks

- The new active-surface acceptance rule depends on accurate match classification; an overly broad allowlist could hide residue unless reviewers check runtime source, config, deploy scripts, current README/user docs, and active tests separately.
- Route cleanup touches many frontend files at once; the executor should avoid mixing route rewrites with docs/script deletion in one oversized diff.
- CORS/domain changes must preserve secure cookie-session behavior and must not introduce wildcard credentialed origins.
- Renaming Docker/container/database defaults can affect local volumes and smoke commands.
- Some tenant terms may remain in tests as intentional negative assertions from Phase 6; the executor must either rewrite those tests or record a narrow allowlist in both this report and `verification.md`.
- Browser smoke may still be blocked by Docker/Postgres availability and seeded credentials.

## Verification Plan

Verification should record exact commands and outputs in `verification.md` after implementation. Planned checks include:

- Active Valorie/domain/customer scans.
- Active tenant/org/invite/migration scans.
- Obsolete docs/scripts scans.
- `npm run lint`, `npm test`, and `npm run build` from `frontend/`.
- Focused backend tests for changed backend startup/config surfaces.
- Full backend tests when backend app code changes.
- `git diff --check`.
- Browser smoke only if a real local backend/Postgres/frontend/seeded-account environment is available.

## Reviewer Attention

- Phase 7 should not self-close; reviewer acceptance is required.
- The reviewer should receive a final changed/deleted/rewritten file list and all remaining allowed legacy-string matches.
- If browser smoke is unavailable, the handoff must state the exact blocker and leave browser evidence unchecked.
- Any retained compatibility or historical match must be documented instead of hidden.
