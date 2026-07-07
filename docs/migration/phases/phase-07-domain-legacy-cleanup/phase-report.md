# Phase 07 Report - Domain and Legacy Cleanup

Round 0/1 implementation status: fresh inventory and domain/brand active runtime naming cleanup have been performed. A requested deploy/nginx/docker naming cleanup pass was performed on 2026-07-02. Migration placeholder route/tool cleanup was performed on 2026-07-05. Frontend personal-route cleanup was performed on 2026-07-06. Unmounted frontend tenant/org/invite placeholder cleanup was performed on 2026-07-07. Phase 7 is not complete, and remaining frontend auth-state cleanup, organization-sharing UI/API-guard cleanup, obsolete docs/scripts cleanup, browser smoke, and reviewer acceptance remain pending. Phase 7 execution relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

## Status

This report now records the Phase 7 planning package and the first narrow Round 0/1 implementation pass after the Phase 6 frontend de-Firebase closeout docs were corrected to record Migration Reviewer acceptance.

Current Phase 7 state:

- Planning package created: `checklist.md`, `phase-plan.md`, `verification.md`, and this `phase-report.md`.
- Round 0/1 implementation performed on 2026-07-02: focused inventory, active runtime/domain cleanup, app-visible Valorie brand cleanup, CORS origin configuration cleanup, focused tests, lint, build, backend syntax, and Docker availability check.
- Requested deploy/nginx/docker naming cleanup performed on 2026-07-02: neutral Docker image/container/database defaults, neutral nginx template replacement, rewritten deployment helper, and removal of the obsolete tenant preflight/deploy header.
- Migration placeholder route/tool cleanup performed on 2026-07-05: removed the inert `/migrate` frontend route, deleted the isolated client-side migration/cleanup placeholders, and removed the route-test mock that existed only for the placeholder component.
- Frontend personal-route cleanup performed on 2026-07-06: replaced active `/:tenantId/*` route shells with `/frameworks`, `/frameworks/create`, and `/frameworks/:id`, removed `TenantRoute` and tenant/org/invite placeholder imports from `App.jsx`, routed `/` and successful login to `/frameworks`, and updated route/navigation tests.
- Unmounted frontend tenant/org/invite placeholder cleanup performed on 2026-07-07: deleted the five confirmed-unreferenced placeholder component files left after the personal-route cleanup, without changing auth state, organization-sharing UI, the API identity-strip guard, backend behavior, models, or migrations.
- Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance.
- Phase 6 Round 6 closeout commit is `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- Phase 7 scope is semantic cleanup of Valorie/domain, tenant/org/invite/migration residue, obsolete docs, obsolete scripts/tests, and legacy deploy/env naming.
- Phase 6 browser smoke remains documented as deferred because Docker/Postgres/seeded local environment was unavailable.
- Phase 7 implementation has started, migration placeholders are removed, personal framework routes are active, and unmounted tenant/org/invite placeholders are deleted, but Phase 7 is not complete.
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

These allowlist entries do not cover active runtime/config/deploy/current-doc residue. The deploy/nginx/docker naming residue previously present in `deploy.sh`, `nginx-valorie.conf`, `docker-compose.yml`, `docker-entrypoint.sh`, and backend preflight handling has now been cleaned. The active `/migrate` route and isolated migration placeholder files have now been removed. Active tenant/org/invite route residue and obsolete current-doc/script residue remain explicit Phase 7 follow-up work rather than allowlisted closeout exceptions.

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

## Migration Placeholder Route/Tool Cleanup - 2026-07-05

Scope performed:

- Ran focused inventory for `MigrationTool`, `migrate-data`, `cleanupData`, `DataCleanupButton`, `updateFrameworkTenants`, `/migrate`, migration placeholder wording, and migration tool wording across active frontend/backend source and migration docs.
- Confirmed the active runtime candidates were obsolete placeholders: `frontend/src/components/MigrationTool.jsx`, `frontend/src/migrate-data.js`, `frontend/src/utils/cleanupData.js`, `frontend/src/utils/DataCleanupButton.jsx`, and `frontend/src/utils/updateFrameworkTenants.js` only returned isolated/unavailable placeholder responses from the Phase 6 SDK-removal bridge.
- Removed the `/migrate` route and `MigrationTool` import from `frontend/src/App.jsx`.
- Deleted the five isolated client-side migration/cleanup placeholder files.
- Removed the unused `MigrationTool` route mock from `frontend/src/App.route.test.jsx`.

Files changed or deleted in this pass:

- `frontend/src/App.jsx`
- `frontend/src/App.route.test.jsx`
- `frontend/src/components/MigrationTool.jsx` deleted
- `frontend/src/migrate-data.js` deleted
- `frontend/src/utils/cleanupData.js` deleted
- `frontend/src/utils/DataCleanupButton.jsx` deleted
- `frontend/src/utils/updateFrameworkTenants.js` deleted
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

Verification summary:

- Post-edit active frontend scan for `MigrationTool`, `migrate-data`, `cleanupData`, `DataCleanupButton`, `updateFrameworkTenants`, and `/migrate` returned no matches.
- `Test-Path` checks for all five deleted placeholder files returned `False`.
- Focused route test passed after the expected sandbox config-read failure was rerun outside the sandbox: `1 passed`.
- Full frontend test suite passed outside the sandbox: `10 passed`, `53 passed`.
- Frontend lint passed.
- Frontend build passed outside the sandbox after the expected sandbox config-read failure: `140 modules transformed`, build completed in `7.43s`, with existing browser-data and chunk-size warnings.
- Backend syntax/tests were not run because this pass changed only frontend route/test files and migration docs.

Deferrals and non-targets:

- Tenant/org/invite route cleanup remains deferred to the later personal route-flow round. `TenantRoute`, `TenantSettings`, `InviteAccept`, `YourOrganization`, tenant route shims, organization UI, and related auth state were intentionally not changed.
- `backend_py/app/services/vectorstore/openai_legacy.py` contains a provider compatibility message mentioning a legacy migration tool. It is not a frontend migration placeholder route/tool and is preserved under the existing provider-compatibility boundary.
- Historical migration docs retain placeholder names as audit evidence under the existing `docs/migration/phases/**` allowlist.
- No Agent loop, Tool Registry, RAG, LLMWiki, Chat UI, Skill Registry, public registration, SaaS expansion, invite system, MCP marketplace, auth/session, model, or database migration behavior was changed.

## Tenant/Org/Invite Cleanup Inventory - 2026-07-06

Scope performed:

- Ran inventory-only scans for `tenant`, `tenants`, `organization`, `organizations`, `org_id`, `organization_id`, `invite`, `invitation`, `invite_token`, `X-Tenant-ID`, `tenant_id`, `default_tenant`, and `framework_tenant`.
- Covered active backend app code, frontend source, frontend tests, backend tests, current docs, historical migration docs, database models, Alembic migrations, route guards, services, obsolete helper scripts, and env/deploy/config files.
- Did not delete runtime code, did not change auth/session behavior, did not change database models or migrations, and did not add any replacement tenant/org/invite/workspace system.

Inventory table:

| Surface | References found | Classification | Recommended action |
|---|---|---|---|
| Frontend route tree | `frontend/src/App.jsx` imports `TenantRoute`, `TenantSettings`, `InviteAccept`, `YourOrganization`; mounts `/invite/:token` and `/:tenantId/*` framework routes | remove in frontend cleanup | Replace with personal routes (`/frameworks`, `/frameworks/create`, `/frameworks/:id`) guarded by `PrivateRoute`; remove invite/org/settings route mounts. |
| Frontend route guard | `frontend/src/components/TenantRoute.jsx` and `TenantRoute.test.jsx` | removed in frontend cleanup | `TenantRoute.test.jsx` was deleted in the personal-route slice. `TenantRoute.jsx` was deleted on 2026-07-07 after `rg` proved no imports, renders, or tests remained. Backend JWT ownership checks remain the authority. |
| Frontend auth/session state | `frontend/src/contexts/AuthContext.jsx` keeps `tenantId`, `joinedOrganization`, and `updateUserTenant`; `Login.jsx`, `LandingPage.jsx`, and `App.jsx` route through `/personal/frameworks` | remove in frontend cleanup | Drop tenant/org state from frontend user shape and route login/root directly to `/frameworks`; preserve backend-cookie auth, `id`, `email`, and `isSuperAdmin`. |
| Frontend route generation helpers | `frontend/src/lib/api.js` exports `getCurrentTenantId`; `CreateFramework.jsx`, `FrameworkEditor.jsx`, `FrameworkCard.jsx`, `YourFrameworks.jsx`, and `Navbar.jsx` build `/${tenantShim}/...` paths | remove in frontend cleanup | Replace URL generation with personal route helpers or literals; remove `getCurrentTenantId`. |
| Frontend API defensive identity stripping | `frontend/src/lib/api.js` `stripArtefactResourceFields` removes client-supplied resource and identity fields before artefact create/update payloads; `tenant_id` and `X-Tenant-ID` are built as `['tenant', 'id'].join('_')` and `['X', 'Tenant-ID'].join('-')`, so literal scans for the full strings miss the guard | preserve for now as a security-preserving identity-strip guard | Keep until a focused frontend API cleanup can replace tenant/header fixtures with neutral client-identity fixtures while preserving equivalent strip coverage. Do not delete as backend tenant/model cleanup; its current effect is to prevent client-supplied identity/header data from being forwarded. |
| Frontend org/invite placeholders | `TenantCreationModal.jsx`, `TenantSettings.jsx`, `InviteAccept.jsx`, `YourOrganization.jsx` | removed in frontend cleanup | Deleted on 2026-07-07 after `rg` proved no imports, renders, or tests remained. No invite/workspace flow was added. |
| Frontend org-field repair placeholder | `frontend/src/components/UpdateFrameworksButton.jsx` returns null as a Phase 7 org-field repair placeholder; `frontend/src/components/YourFrameworks.jsx` imports it and renders `<UpdateFrameworksButton />` in the active framework list | remove in frontend org placeholder cleanup | Delete the null component and the `YourFrameworks.jsx` import/render in a focused frontend org placeholder cleanup slice, alongside organization filters/actions. Do not attach this to backend tenant/model cleanup. |
| Frontend organization sharing UI | `FrameworkCard.jsx` `publishedToOrganization` display/actions and inert org publish alerts; `YourFrameworks.jsx` organization filter; `Navbar.jsx` organization menu | remove in frontend cleanup | Remove organization-sharing controls and filters; keep authenticated public library/publish behavior only. |
| Frontend tests | `App.route.test.jsx`, `TenantRoute.test.jsx`, `FrameworkEditor.test.jsx`, `FrameworkCard.test.jsx`, `Login.test.jsx`, and `api.test.js` | mixed: remove/update plus preserve negative assertions | Update route/component tests for personal routes. Preserve `api.test.js` client-identity stripping assertions until equivalent coverage no longer needs tenant-header fixtures. |
| Backend app routes and services | No `/api/tenants/*`, invite, organization router, `tenant_id`, `invite_token`, `org_id`, or `organization_id` app/model/migration hits; `backend_py/app/api/vector_sync.py` has `include_organization` | defer with reason | Keep `vector_sync.py` unchanged in this inventory pass because it is Phase 9-deferred indexing/RAG plumbing. Rename or remove only in a focused backend/vector-sync cleanup if the deferred API is retired or re-shaped. |
| Backend ownership/auth | Framework, artefact, admin, and user routes derive identity from `Depends(get_current_user_id)` or `Depends(get_current_user)` and use `creator_id`/user id ownership checks | preserve as personal-use ownership/auth concept | Preserve backend JWT-derived user ownership and admin authorization. This is not tenant/org sharing residue. |
| Backend tests | `backend_py/tests/test_main.py` asserts `X-Tenant-ID` is omitted from CORS preflight headers | preserve as personal-use ownership/auth concept | Keep as a negative assertion unless the CORS test is rewritten to prove the same invariant without the legacy header string. |
| Database models and migrations | `backend_py/app/models.py` and `backend_py/alembic/**` had no target-term hits | preserve as personal-use ownership/auth concept | No database model or migration changes needed; do not add workspaces/tenants. |
| Env/config/deploy | `.env.example`, frontend/backend env examples, Dockerfile, Compose, entrypoint, deploy script, and `nginx-framework.conf` had no target-term hits | preserve as already-clean active surface | No action in this pass. |
| Current README and obsolete backend docs/scripts | `README.md`, `backend_py/README-DIFF.md`, `backend_py/test_firebase.py`, `backend_py/test_update.py`, `backend_py/test_update_publish.py`, `backend_py/check_vector_store_attributes.py` | remove in backend/docs cleanup | Handle in Round 5: rewrite current README and delete or rewrite obsolete Firestore/OpenAI Vector Store helper material. |
| Migration docs and canonical plan | `MIGRATION_PHASES.md` and `docs/migration/phases/**` intentionally name tenant/org/invite cleanup targets and prior deferrals | historical allowlist | Preserve audit history; do not treat these as active product residue. |
| Migration skill docs | `docs/skills/migration-phase-planner/SKILL.md` and `docs/skills/migration-reviewer/SKILL.md` mention tenant-era scan/review checks | defer with reason | Keep as migration tooling references unless a later docs-tooling cleanup updates the skills. They are not runtime or user-facing product docs. |

Recommended cleanup slices:

1. Frontend personal-route slice: completed on 2026-07-06; active routes now use `/frameworks`, `/frameworks/create`, and `/frameworks/:id`, `TenantRoute` is removed from the route tree, and login/root route to `/frameworks`.
2. Frontend unmounted placeholder cleanup slice: completed on 2026-07-07; `TenantRoute.jsx`, `TenantCreationModal.jsx`, `TenantSettings.jsx`, `YourOrganization.jsx`, and `InviteAccept.jsx` were deleted after no active imports/tests remained.
3. Frontend tenant/org state cleanup slice: remove remaining `tenantId`, `joinedOrganization`, and `updateUserTenant` auth state now that route generation no longer depends on tenant shims.
4. Frontend organization-sharing UI cleanup slice: delete `UpdateFrameworksButton.jsx`; remove the `YourFrameworks.jsx` `UpdateFrameworksButton` import/render, inert "Publish to Organization" actions, and organization filters while preserving authenticated public library behavior.
5. Focused frontend API cleanup slice: preserve the `api.js` split-string identity-strip guard until equivalent neutral client-identity stripping coverage replaces the tenant/header fixtures in `api.js` and `api.test.js`.
6. Backend/vector-sync decision slice: leave `include_organization` deferred unless Phase 7 explicitly retires the Phase 9-deferred vector sync request shape; do not touch database models or migrations.
7. Round 5 docs/scripts slice: rewrite current README and remove obsolete Firebase/Firestore/OpenAI Vector Store helper docs/scripts after the active frontend route cleanup is stable.

Recommended next implementation slice:

- Implement the next focused frontend tenant/org auth-state and organization-sharing cleanup slice. Personal routes are active and unmounted placeholder files are gone, so the remaining frontend work can remove `tenantId`/`joinedOrganization` auth state, inert organization sharing controls, and `UpdateFrameworksButton.jsx` without changing route shape again.

## Frontend Personal Route Cleanup - 2026-07-06

Scope performed:

- Replaced active framework route shells from `/:tenantId/frameworks`, `/:tenantId/create`, and `/:tenantId/editor/:id` to `/frameworks`, `/frameworks/create`, and `/frameworks/:id`.
- Removed `TenantRoute` from the active route tree and wrapped `/frameworks`, `/frameworks/create`, `/frameworks/:id`, `/library`, and `/admin` with `PrivateRoute`.
- Removed active `App.jsx` imports and mounts for `TenantRoute`, `TenantSettings`, `InviteAccept`, and `YourOrganization`; the placeholder component files remain unmounted for the later org/invite placeholder cleanup slice.
- Routed `/` and successful login to `/frameworks`.
- Updated navigation in `Navbar.jsx`, `CreateFramework.jsx`, `FrameworkEditor.jsx`, `FrameworkCard.jsx`, `YourFrameworks.jsx`, `LandingPage.jsx`, and `Home.jsx` to the personal route shape.
- Removed the unused `getCurrentTenantId` route shim export and its route-shim test. The `api.js` split-string `tenant_id` / `X-Tenant-ID` identity-strip guard was preserved.
- Deleted `frontend/src/components/TenantRoute.test.jsx` because it only covered the removed route shim.

Files changed or deleted in this slice:

- `frontend/src/App.jsx`
- `frontend/src/App.route.test.jsx`
- `frontend/src/components/CreateFramework.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/FrameworkCard.test.jsx`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/FrameworkEditor.test.jsx`
- `frontend/src/components/Home.jsx`
- `frontend/src/components/LandingPage.jsx`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/Login.test.jsx`
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/TenantRoute.test.jsx` deleted
- `frontend/src/components/YourFrameworks.jsx`
- `frontend/src/lib/api.js`
- `frontend/src/lib/api.test.js`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md`
- `docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md`

Verification summary:

- Active old-route path scan returned no `/:tenantId`, `/invite/:token`, `/personal/frameworks`, `/editor/`, `getPath`, `tenantShim`, or `getCurrentTenantId` route/path hits outside the unmounted placeholder component files.
- Import checks found no active imports or JSX mounts for `TenantRoute`, `TenantSettings`, `InviteAccept`, or `YourOrganization`.
- Focused route/API tests passed outside the sandbox after the expected Vitest config-read sandbox failure: 4 files, 30 tests.
- Frontend lint passed.
- Full frontend tests passed outside the sandbox after the expected Vitest config-read sandbox failure: 9 files, 52 tests.
- Frontend build passed outside the sandbox after the expected Vite config-read sandbox failure: 136 modules transformed, build completed in 5.19s, with existing stale browser-data and chunk-size warnings.
- `git diff --check` passed before documentation updates; final whitespace check is recorded in `verification.md`.

Remaining tenant/org/invite residue after this slice:

- Unmounted placeholder files remain: `TenantRoute.jsx`, `TenantCreationModal.jsx`, `TenantSettings.jsx`, `YourOrganization.jsx`, and `InviteAccept.jsx`.
- `frontend/src/contexts/AuthContext.jsx` still retains `tenantId`, `joinedOrganization`, and `updateUserTenant`; this is deferred to the next frontend tenant/org state cleanup.
- `FrameworkCard.jsx`, `YourFrameworks.jsx`, and `frontend/src/lib/api.js` still contain organization-sharing fields and filters such as `publishedToOrganization`; this is deferred to the frontend org placeholder cleanup.
- `UpdateFrameworksButton.jsx` remains imported and rendered by `YourFrameworks.jsx` as previously documented; it is deferred to the focused org placeholder cleanup.
- `frontend/src/lib/api.js` and `frontend/src/lib/api.test.js` retain `tenant_id` / `X-Tenant-ID` only in the security-preserving identity-strip guard and negative assertions; do not remove until the focused frontend API cleanup replaces them with neutral equivalent coverage.

Boundaries honored:

- Did not change backend auth/session behavior, backend ownership checks, database models, or migrations.
- Did not remove backend ownership checks.
- Did not rewrite the `api.js` identity-strip guard.
- Did not remove `UpdateFrameworksButton.jsx`.
- Did not implement org sharing, invites, workspaces, public registration, Agent, RAG, LLMWiki, Chat UI, Tool Registry, or MCP marketplace.
- Did not rewrite README or obsolete backend helper scripts.

## Unmounted Frontend Tenant/Org/Invite Placeholder Cleanup - 2026-07-07

Scope performed:

- Ran the required pre-delete `rg` inventory for `TenantRoute`, `TenantCreationModal`, `TenantSettings`, `YourOrganization`, and `InviteAccept`.
- Confirmed component-name matches were limited to each placeholder's own source file.
- Confirmed no active imports, JSX renders, or frontend tests referenced the five placeholder component names.
- Deleted only the five confirmed-unmounted placeholder files.
- Did not update tests because no active test referenced only these removed placeholders.

Files deleted in this slice:

- `frontend/src/components/TenantRoute.jsx`
- `frontend/src/components/TenantCreationModal.jsx`
- `frontend/src/components/TenantSettings.jsx`
- `frontend/src/components/YourOrganization.jsx`
- `frontend/src/components/InviteAccept.jsx`

Verification summary:

- Post-delete component-name scan for the five deleted components returned no matches in `frontend/src`.
- `Test-Path` returned `False` for all five deleted files.
- Invite/tenant route residue scan returned no active `/:tenantId`, `/invite/:token`, `/personal/frameworks`, `/editor/`, `Tenant Settings`, `My Organization`, or deleted-component JSX route hits in `frontend/src`.
- Remaining frontend tenant/org residue is limited to the previously documented deferrals: `AuthContext.jsx` tenant/org state, `api.js` split-string identity-strip guard and `publishedToOrganization` normalization, `api.test.js` negative identity-strip assertions, `FrameworkCard.jsx` organization-sharing labels/actions, `YourFrameworks.jsx` organization filters, and `UpdateFrameworksButton.jsx`.
- Frontend lint passed.
- Full frontend tests passed on escalated rerun after the expected sandbox config-read failure: 9 files, 52 tests.
- Frontend build passed on escalated rerun after the expected sandbox config-read failure: 136 modules transformed, build completed in 6.56s, with existing stale browser-data and chunk-size warnings.
- Backend tests were not run because this slice changed only frontend placeholder files and migration docs.
- Browser smoke was not run or claimed.

Boundaries honored:

- Did not change `frontend/src/contexts/AuthContext.jsx` tenantId, joinedOrganization, or updateUserTenant state.
- Did not change `FrameworkCard.jsx` or `YourFrameworks.jsx` organization-sharing UI.
- Did not rewrite the `api.js` identity-strip guard.
- Did not change backend auth/session behavior, backend ownership checks, database models, migrations, API contracts, or deploy/config files.
- Did not implement invites, org sharing, workspaces, public registration, Agent, RAG, LLMWiki, Chat UI, Tool Registry, or MCP marketplace.
- Did not rewrite README or obsolete backend helper scripts.

Current remaining frontend tenant/org residue:

- `frontend/src/contexts/AuthContext.jsx` still retains `tenantId`, `joinedOrganization`, and `updateUserTenant`.
- `frontend/src/lib/api.js` still retains the split-string `tenant_id` / `X-Tenant-ID` identity-strip guard and `publishedToOrganization` normalization.
- `frontend/src/lib/api.test.js` still retains `tenant_id` / `X-Tenant-ID` negative assertions.
- `frontend/src/components/FrameworkCard.jsx` still retains organization-sharing labels/actions.
- `frontend/src/components/YourFrameworks.jsx` still retains organization filters and `publishedToOrganization` checks.
- `frontend/src/components/UpdateFrameworksButton.jsx` remains imported and rendered by `YourFrameworks.jsx`.

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
