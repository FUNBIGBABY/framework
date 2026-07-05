# Phase 07 Report - Domain and Legacy Cleanup

Round 0/1 implementation status: fresh inventory and domain/brand active runtime naming cleanup have been performed. A requested deploy/nginx/docker naming cleanup pass was performed on 2026-07-02. Phase 7 is not complete, and later migration placeholder cleanup, tenant/org/invite route cleanup, obsolete docs/scripts cleanup, browser smoke, and reviewer acceptance remain pending. Phase 7 execution relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

## Status

This report now records the Phase 7 planning package and the first narrow Round 0/1 implementation pass after the Phase 6 frontend de-Firebase closeout docs were corrected to record Migration Reviewer acceptance.

Current Phase 7 state:

- Planning package created: `checklist.md`, `phase-plan.md`, `verification.md`, and this `phase-report.md`.
- Round 0/1 implementation performed on 2026-07-02: focused inventory, active runtime/domain cleanup, app-visible Valorie brand cleanup, CORS origin configuration cleanup, focused tests, lint, build, backend syntax, and Docker availability check.
- Requested deploy/nginx/docker naming cleanup performed on 2026-07-02: neutral Docker image/container/database defaults, neutral nginx template replacement, rewritten deployment helper, and removal of the obsolete tenant preflight/deploy header.
- Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance.
- Phase 6 Round 6 closeout commit is `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- Phase 7 scope is semantic cleanup of Valorie/domain, tenant/org/invite/migration residue, obsolete docs, obsolete scripts/tests, and legacy deploy/env naming.
- Phase 6 browser smoke remains documented as deferred because Docker/Postgres/seeded local environment was unavailable.
- Phase 7 implementation has started but is not complete.
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

For Phase 7 implementation, Phase 6 `checklist.md` remains required context alongside Phase 6 `phase-report.md` and `verification.md`; the report/verification pair alone is not sufficient for the Phase 6 gate.

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

Round 0/1 allowlist entries are recorded here and mirrored in `verification.md`:

- `MIGRATION_PHASES.md`: retains legacy strings such as `valorie.ai`, `framework-builder-55896`, `webmaster@valorie`, `UNSW`, `ad.unsw`, tenant, invite, and migration terms because it is the canonical migration plan and names the cleanup targets and acceptance scans. It is not active runtime/config/deploy/current user documentation.
- `docs/migration/phases/**`: retains historical phase evidence and current phase verification records that quote legacy strings, commands, and outputs. These records must remain auditable and are not active runtime/config/deploy/current user documentation.
- `backend_py/tests/test_main.py`: retains `https://expert.valorie.ai` and `X-Tenant-ID` only as intentional negative assertions proving the old Valorie production origin is no longer accepted by backend CORS and the legacy tenant header is no longer advertised by backend preflight handling.
- `frontend/src/lib/api.test.js`: retains `tenant_id` and `X-Tenant-ID` only as intentional negative assertions proving frontend request payload/header helpers strip client-supplied identity fields.

These allowlist entries do not cover active runtime/config/deploy/current-doc residue. The deploy/nginx/docker naming residue previously present in `deploy.sh`, `nginx-valorie.conf`, `docker-compose.yml`, `docker-entrypoint.sh`, and backend preflight handling has now been cleaned. Active tenant/org/invite/migration route residue and obsolete current-doc/script residue remain explicit Phase 7 follow-up work rather than allowlisted closeout exceptions.

## Round 0/1 Implementation - 2026-07-02

Scope performed:

- Re-read required Phase 7 context, ADR-0001, the personal-use boundary, and Phase 6 dependency docs.
- Re-ran focused legacy/domain and tenant/org/invite/migration inventory scans.
- Classified matches into active runtime/config, deploy, current docs, historical migration docs, active route residue, obsolete script/test residue, and intentional negative assertions.
- Cleaned Round 1 active runtime/config/app-visible domain and brand residue only.
- Left `/migrate`, tenant, organization, invite, Docker image/container/database naming, deploy/nginx cleanup, current README rewrite, and obsolete helper script cleanup for later Phase 7 rounds.

Files changed in Round 0/1:

- `.env.example`
- `backend_py/.env.example`
- `backend_py/alembic.ini`
- `backend_py/main.py`
- `backend_py/tests/test_main.py`
- `frontend/.env.example`
- `frontend/index.html`
- `frontend/src/lib/appConfig.js`
- `frontend/src/lib/api.js`
- `frontend/src/lib/api.test.js`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/LandingPage.jsx`
- `frontend/src/components/Navbar.jsx`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

Implementation details:

- `backend_py/main.py` now derives the FastAPI title from `APP_NAME` with a neutral default and builds credentialed CORS origin patterns from localhost/127.0.0.1 plus exact configured `FRONTEND_URL` and `APP_BASE_DOMAIN` origins. The old `expert.valorie.ai` and wildcard `*.valorie.ai` CORS patterns were removed.
- Env examples and Alembic sample URLs use neutral `framework` database/user names instead of `valorie`, and document `APP_NAME`, `APP_BASE_DOMAIN`, `SUPER_ADMIN_EMAIL`, and Vite-side `VITE_APP_*` knobs.
- `frontend/src/lib/api.js` no longer infers production mode or tenant identity from `expert.valorie.ai` / `*.valorie.ai`. It uses `VITE_API_BASE_URL` first, then relative API paths only for the exact configured `VITE_APP_BASE_DOMAIN`, and keeps the legacy route shim path-based until the route cleanup round.
- Login, landing, navbar, and `frontend/index.html` now use neutral personal-use naming. The landing page no longer advertises organization invites or team collaboration as current behavior.
- Focused tests cover backend CORS/app-title behavior and frontend API base URL/path-shim behavior.

Round 0/1 inventory classification:

- Cleaned active runtime/config/app-visible targets: `backend_py/main.py`, `.env.example`, `backend_py/.env.example`, `backend_py/alembic.ini`, `frontend/.env.example`, `frontend/index.html`, `frontend/src/lib/api.js`, `frontend/src/components/Login.jsx`, `frontend/src/components/LandingPage.jsx`, and `frontend/src/components/Navbar.jsx`.
- Deferred active deploy targets: `deploy.sh` and `nginx-valorie.conf` still contain `expert.valorie.ai`, `*.valorie.ai`, and `valorie.ai`; these belong to Phase 7 Round 4.
- Deferred Docker naming targets: `docker-compose.yml` still contains Valorie container/image/database defaults; this belongs to Phase 7 Round 4 because this Round 1 pass did not rename containers/images/local volumes.
- Deferred active route/navigation targets: `frontend/src/App.jsx`, `TenantRoute.jsx`, `TenantSettings.jsx`, `YourOrganization.jsx`, `InviteAccept.jsx`, `MigrationTool.jsx`, `AuthContext.jsx`, framework route helpers, and related route/component tests still contain tenant/org/invite/migration residue; these belong to Phase 7 Rounds 2 and 3.
- Deferred current-doc/script/test targets: `README.md`, `Project-Startup-and-Operation-Flow.md`, `firebaseDoc.md`, `docs/CN_DEPLOY.md`, `backend_py/README-DIFF.md`, and top-level backend helper scripts/tests still need Round 5 cleanup.
- Historical migration records: retained under the allowlist above.
- Intentional negative assertions: retained under the allowlist above.

Round 0/1 verification summary:

- Focused active runtime/config domain scan for touched Round 1 files returned no Valorie/customer string matches.
- Broader active domain scan still reports `deploy.sh` and `nginx-valorie.conf`; these are deferred Round 4 work, not hidden allowlist entries. The same scan reports `backend_py/tests/test_main.py` only for the allowlisted negative CORS assertion against the old Valorie origin.
- Focused backend tests passed: `backend_py\.venv\Scripts\python.exe -m pytest -q tests/test_main.py` produced `3 passed` with existing Pydantic deprecation warnings.
- Backend syntax passed: `backend_py\.venv\Scripts\python.exe -m py_compile main.py tests/test_main.py`.
- Focused frontend tests passed on escalated rerun after the sandboxed Vitest config-read failure: 2 files, 25 tests.
- Frontend lint passed.
- Frontend build passed on escalated rerun after the sandboxed Vite config-read failure; warnings were stale browser data and chunk size.
- Browser smoke was not run because `docker compose ps` still cannot connect to Docker Desktop's Linux engine pipe, and no live Postgres/seeded browser-smoke environment is available in this turn.

Round 0/1 boundaries honored:

- Did not delete or rewrite `/migrate`, tenant, organization, invite, or placeholder route files.
- Did not remove `TenantRoute`, `tenantId` route shims, `getCurrentTenantId`, or organization sharing UI beyond removing Valorie-domain inference and stale landing copy.
- Did not rename Docker containers/images/database defaults in `docker-compose.yml`.
- Did not rewrite README/current user docs or delete obsolete backend helper scripts.
- Did not implement Agent loop, Tool Registry, RAG, LLMWiki, Chat UI, Skill Registry, MCP, public registration, SaaS tenant/org sharing, workspace sharing, or a new invite system.

## Requested Deploy/Nginx/Docker Naming Cleanup - 2026-07-02

Scope performed:

- Cleaned active deployment naming only: `deploy.sh`, nginx template naming, Docker Compose image/container/database defaults, Docker entrypoint startup label, and the backend CORS preflight header list.
- Replaced `nginx-valorie.conf` with `nginx-framework.conf`, a neutral single-domain HTTP template rendered by `deploy.sh` from `APP_DOMAIN`; `certbot --nginx` is left to add HTTPS after certificates exist.
- Removed wildcard Valorie tenant subdomain handling and `proxy_set_header X-Tenant-ID` from the nginx deployment template.
- Rewrote `deploy.sh` so it no longer copies a Valorie-named site, provisions `expert.valorie.ai`, provisions `*.valorie.ai`, or mentions GCP-specific firewall instructions. It now requires `APP_DOMAIN`, validates the hostname shape, renders the HTTP `nginx-framework.conf` template, and points the operator to `APP_BASE_DOMAIN`, `FRONTEND_URL`, and `VITE_APP_BASE_DOMAIN`.
- Renamed Docker defaults from `valorie-db`, `valorie-app`, `valorie-framework-builder:latest`, `POSTGRES_DB=valorie`, `POSTGRES_USER=valorie`, and `postgresql+psycopg://valorie:.../valorie` to neutral `framework` defaults.
- Passed active deployment env knobs through Compose for `FRONTEND_URL`, `APP_BASE_DOMAIN`, `APP_NAME`, and `SUPER_ADMIN_EMAIL`.
- Removed `X-Tenant-ID` from backend preflight `Access-Control-Allow-Headers` after a backend scan found no active backend consumer for that header. `backend_py/app/api/vector_sync.py` still contains the Phase 9-deferred `include_organization` request field and was intentionally not changed in this pass.

Files changed in this pass:

- `deploy.sh`
- `docker-compose.yml`
- `docker-entrypoint.sh`
- `nginx-valorie.conf` deleted
- `nginx-framework.conf` added
- `backend_py/main.py`
- `backend_py/tests/test_main.py`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

Local Docker volume implication:

- Compose still uses the named volume `pgdata`, but Compose projects it as `framework_pgdata` under the current project name. Existing local volumes initialized with the old `valorie` database/user defaults may not contain the new `framework` database/user. Developers with an old local volume may need to set explicit `POSTGRES_DB`, `POSTGRES_USER`, and `DATABASE_URL` compatibility values, or intentionally recreate the local dev volume after backing up any needed data.

Verification summary:

- Focused deploy legacy scans now return no active deploy/config Valorie or wildcard tenant-domain matches. Remaining `https://expert.valorie.ai` and `X-Tenant-ID` matches are intentional negative assertions in `backend_py/tests/test_main.py`.
- `docker compose config` exited 0 and rendered `framework-app`, `framework-db`, `framework-builder:latest`, `POSTGRES_DB=framework`, `POSTGRES_USER=framework`, and the neutral `DATABASE_URL`. It warned that `JWT_SECRET_KEY` and `DEEPSEEK_API_KEY` are unset and that the Compose `version` attribute is obsolete.
- Focused backend tests passed after replacing a `TestClient`-based assertion with direct middleware invocation compatible with the current Starlette/httpx versions: `4 passed, 3 warnings`.
- Backend syntax compilation passed.
- `bash -n deploy.sh` could not validate the script because the only `bash.exe` on PATH is the Windows WSL launcher and WSL is not installed/configured in this environment.
- `nginx` is not available on PATH, so nginx syntax validation was not run.
- Browser smoke was not claimed or run.

Boundaries honored:

- Did not delete `/migrate` or any migration placeholder route/tool files.
- Did not touch tenant/org/invite route/model deletion.
- Did not change backend auth semantics beyond removing the unused legacy preflight header advertisement.
- Did not touch Agent loop, Tool Registry, RAG, LLMWiki, Chat UI, Skill Registry, public registration, SaaS expansion, invite systems, or MCP marketplace work.
- Did not rewrite current README or obsolete deployment/docs beyond the Phase 7 execution record.

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
- The Docker/container/database defaults have been renamed to neutral `framework` values; existing local volumes created with old `valorie` database/user defaults may require explicit compatibility env values or an intentional local volume reset.
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
