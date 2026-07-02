# Phase 07 Plan - Domain and Legacy Cleanup

Planning status: documentation only. This plan does not implement backend, frontend, test, migration, deployment, or documentation cleanup, and it does not mark Phase 7 complete. Phase 7 planning relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

## Recommended Plan

Phase 7 should clean the semantic residue intentionally left after Phase 6: Valorie/domain naming, tenant/org/invite route shells, one-time migration placeholders, obsolete docs, obsolete helper scripts/tests, and legacy deployment naming. The recommended sequence is six implementation rounds after a fresh inventory round:

1. Round 0: fresh inventory and boundary confirmation.
2. Round 1: domain, brand, and active runtime naming cleanup.
3. Round 2: legacy migration tool and placeholder removal.
4. Round 3: personal route flow and tenant/org/invite cleanup.
5. Round 4: backend, deploy, env, and nginx legacy naming cleanup.
6. Round 5: obsolete docs, scripts, and tests cleanup.
7. Round 6: verification, documentation closeout, and reviewer handoff.

This sequence removes visible naming and config residue first, then deletes isolated migration placeholders, then changes the route model once the cleanup surface is clear. Scripts/docs/deploy cleanup comes after the active runtime routes are stable so verification can distinguish broken current behavior from intentionally deleted legacy material.

## Sources And Current Facts

Required source documents read for this planning package and required before Phase 7 implementation:

- `MIGRATION_PHASES.md`
- `docs/PERSONAL_USE_BOUNDARY.md`
- `docs/migration/README.md`
- `docs/migration/decisions/ADR-0001-auth-strategy.md`
- `docs/migration/phases/phase-06-frontend-defirebase/checklist.md`
- `docs/migration/phases/phase-06-frontend-defirebase/phase-report.md`
- `docs/migration/phases/phase-06-frontend-defirebase/verification.md`

Phase 6 status basis for this plan:

- Phase 6 closeout is recorded as accepted by Migration Reviewer in Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
- Round 6 closeout was committed and pushed as `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- Firebase SDK/package/frontend runtime dependency has been removed.
- Frontend Bearer/localStorage auth path has been removed.
- Backend temporary Bearer compatibility has been removed.
- Browser smoke remains deferred unless a later executor actually runs it.
- Phase 7 semantic cleanup was intentionally not folded into Phase 6.
- If Phase 6 closeout docs do not record accepted status in a future checkout, Phase 7 implementation is gated until that documentation contradiction is corrected.

For Phase 7 implementation, Phase 6 `checklist.md` is required context alongside Phase 6 `phase-report.md` and `verification.md`; do not treat the report/verification pair alone as sufficient.

Focused planning scans found current Phase 7 residue in these areas:

- Active Valorie/domain strings in `.env.example`, `backend_py/.env.example`, `backend_py/alembic.ini`, `backend_py/main.py`, `frontend/src/lib/api.js`, `frontend/src/components/LandingPage.jsx`, `frontend/src/components/Login.jsx`, `frontend/src/components/Navbar.jsx`, `docker-compose.yml`, `docker-entrypoint.sh`, `deploy.sh`, and `nginx-valorie.conf`.
- Route and UI residue in `frontend/src/App.jsx`, `frontend/src/components/TenantRoute.jsx`, `TenantCreationModal.jsx`, `TenantSettings.jsx`, `YourOrganization.jsx`, `InviteAccept.jsx`, `MigrationTool.jsx`, `Navbar.jsx`, `CreateFramework.jsx`, `FrameworkEditor.jsx`, `FrameworkCard.jsx`, `YourFrameworks.jsx`, and related tests.
- Phase 6 isolated placeholders in `frontend/src/migrate-data.js`, `frontend/src/utils/cleanupData.js`, `frontend/src/utils/DataCleanupButton.jsx`, and `frontend/src/utils/updateFrameworkTenants.js`.
- Obsolete helper scripts and docs in `backend_py/test_firebase.py`, `backend_py/test_cloud_llm.py`, `backend_py/test_update.py`, `backend_py/test_update_publish.py`, `backend_py/test_vec_base.py`, `backend_py/check_versions.py`, `backend_py/check_vector_store_attributes.py`, `backend_py/diagnose_env.py`, `backend_py/README-DIFF.md`, `Project-Startup-and-Operation-Flow.md`, and `firebaseDoc.md`.
- Backend app scan did not find a current `/api/tenants/*` router, but did find organization naming residue in the Phase 9-deferred `backend_py/app/api/vector_sync.py` request shape.

## Canonical Active-Surface Acceptance

`MIGRATION_PHASES.md` now resolves the earlier zero-match conflict by requiring active-surface zero matches instead of unconditional repo-wide zero matches for strings such as `valorie.ai`, `framework-builder-55896`, `webmaster@valorie`, `UNSW`, and `ad.unsw`.

Canonical Phase 7 acceptance uses these scan tiers:

- Active surfaces are runtime source, config, deploy scripts, current README/user docs, and active tests.
- Active-surface scans must reach zero forbidden legacy-string matches, except explicitly allowlisted security/negative assertion tests.
- Historical migration records under `docs/migration/phases/**` may retain legacy strings only with an explicit allowlist.
- The allowlist must be recorded in both `verification.md` and `phase-report.md`.
- The allowlist must not hide active runtime/config/deploy/current-doc residue.

Do not claim literal repo-wide zero matches as the Phase 7 acceptance target. Do not rewrite historical migration records unless the owner explicitly asks for that cleanup.

## Scope

Phase 7 owns:

- Valorie/domain/app-name cleanup in active runtime, config, deploy scripts, and user-visible UI.
- Tenant/org/invite/migration residue cleanup in the personal-use frontend flow.
- Deletion of one-time migration tools and inert placeholders isolated during Phase 6.
- Obsolete docs cleanup or rewrite so current docs no longer describe Firebase/Firestore/tenant invite flows as live behavior.
- Obsolete top-level helper script/test cleanup, with useful tools rewritten into current `backend_py/scripts/` only when needed.
- Env/deploy/nginx naming cleanup where it is legacy-domain residue.
- Route cleanup for personal-use app flow.
- Verification docs and reviewer handoff for all cleanup decisions.

## Explicit Non-Goals

- No Agent loop or Tool Registry.
- No RAG indexing, retrieval, or citations.
- No LLMWiki.
- No Chat UI or Skill Registry.
- No MCP marketplace.
- No public registration.
- No SaaS tenant/org sharing model.
- No workspace sharing replacement for tenants.
- No new invite system.
- No broad UI redesign.
- No Firebase Auth, Firestore, Firebase ID token, or new Firebase project.
- No browser smoke claim unless actually run.

## Cleanup Inventory Strategy

Round 0 should produce a classification table before code changes. Each match should land in exactly one category:

- Active runtime: source imported into the app or backend request path.
- Active route/navigation: route definitions, navigation helpers, URL generation, auth redirect, or tests for those routes.
- Placeholder tool: Phase 6 isolated migration/cleanup modules and components.
- Config/deploy: env examples, Docker, nginx, CORS, image names, container names, DB names, or deployment scripts.
- Obsolete script/test: root or backend helper files outside the maintained pytest suite.
- Current docs: README or deployment docs that users may reasonably follow.
- Historical migration docs: prior phase evidence that should usually be preserved.
- Intentional negative assertion: tests that keep legacy terms only to prove the frontend does not send them as authority.

Suggested inventory scans:

```powershell
rg -n --hidden -S "valorie|Valorie|valorie\.ai|expert\.valorie\.ai|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" . -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" -g "!.git"
rg -n --hidden -S "tenant|Tenant|organization|Organization|invite|Invite|MigrationTool|migrate-data|cleanupData|updateFrameworkTenants" frontend/src backend_py docs README.md Dockerfile docker-compose.yml .env.example -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv"
rg --files -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" | rg -i "firebase|Project-Startup|README-DIFF|deploy|nginx|test_|check_|diagnose|migrate|cleanup|tenant|organization|invite"
```

## Round 0 - Fresh Inventory And Boundary Confirmation

Objective: refresh the Phase 7 cleanup inventory after Phase 6 acceptance and avoid accidental future-phase work.

Tasks:

- Re-read the required context.
- Re-run the inventory scans.
- Classify active runtime, config, deploy, current-doc, active-test, script/test, and historical matches.
- Decide and record the allowlist policy for historical migration docs and security/negative assertion tests in both `phase-report.md` and `verification.md`.
- Update Phase 7 docs with any newly discovered files before Round 1 begins.

Stop point:

- Stop before code deletion or route rewrites if the allowlist policy is unresolved.

## Round 1 - Domain, Brand, And Active Runtime Naming Cleanup

Objective: remove Valorie/customer domain assumptions from current runtime behavior and app-visible copy without changing the route model yet.

Likely files:

- `backend_py/main.py`
- `.env.example`
- `backend_py/.env.example`
- `backend_py/alembic.ini`
- `frontend/src/lib/api.js`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/LandingPage.jsx`
- `frontend/src/components/Navbar.jsx`
- frontend API/base-url and UI tests

Implementation boundaries:

- Runtime CORS should derive configured production origins from `APP_BASE_DOMAIN` or a dedicated explicit origin setting, while keeping localhost and `127.0.0.1` development origins.
- Do not weaken cookie/CORS policy by using wildcard credentialed origins.
- `APP_NAME` should drive app title/copy where practical.
- `SUPER_ADMIN_EMAIL` remains the backend admin identity boundary.
- Do not delete tenant routes in this round unless needed to remove hardcoded Valorie domain copy.

Acceptance:

- Active runtime/config files no longer hardcode Valorie domains or customer-specific strings.
- Local development behavior remains intact.
- Frontend lint/tests/build pass for touched surfaces.

## Round 2 - Legacy Migration Tool And Placeholder Removal

Objective: delete one-time client migration and cleanup tools that Phase 6 isolated only to remove Firebase SDK dependency.

Likely files:

- `frontend/src/migrate-data.js`
- `frontend/src/utils/cleanupData.js`
- `frontend/src/utils/DataCleanupButton.jsx`
- `frontend/src/utils/updateFrameworkTenants.js`
- `frontend/src/components/MigrationTool.jsx`
- `frontend/src/App.jsx`
- `frontend/src/App.route.test.jsx`

Implementation boundaries:

- Delete the route and imports for `/migrate`.
- Delete placeholder components/modules instead of preserving feature flags.
- Do not add replacement migration UI.

Acceptance:

- Active source has no migration-tool route or imports.
- Placeholder files are deleted.
- Route tests no longer mock or expect the migration route.

## Round 3 - Personal Route Flow And Tenant/Org/Invite Cleanup

Objective: remove the SaaS-era tenant/org/invite route model and use a personal-use app route shape.

Recommended route shape:

- `/frameworks`
- `/frameworks/create`
- `/frameworks/:id`
- `/library`
- `/admin`
- `/login`

Likely files:

- `frontend/src/App.jsx`
- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/lib/api.js`
- `frontend/src/components/TenantRoute.jsx`
- `frontend/src/components/TenantCreationModal.jsx`
- `frontend/src/components/TenantSettings.jsx`
- `frontend/src/components/YourOrganization.jsx`
- `frontend/src/components/InviteAccept.jsx`
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/Login.jsx`
- `frontend/src/components/CreateFramework.jsx`
- `frontend/src/components/FrameworkEditor.jsx`
- `frontend/src/components/FrameworkCard.jsx`
- `frontend/src/components/YourFrameworks.jsx`
- route/component tests

Implementation boundaries:

- Use `PrivateRoute` for frontend route gating and continue relying on backend framework ownership checks.
- Remove `TenantRoute` rather than rewriting it into a second private-route abstraction.
- Remove `tenantId`, `joinedOrganization`, organization menus, and inert organization-sharing actions from active UI.
- Do not add `workspaces` as a replacement. Future multi-person collaboration, if needed, belongs to a later clean design.
- Keep authenticated public library behavior exactly authenticated.

Acceptance:

- Backend-cookie login routes to `/frameworks`.
- Create/editor/list navigation uses personal routes.
- Tenant, organization, and invite placeholder components are deleted or no longer active.
- Frontend tests cover the new personal route flow.

## Round 4 - Backend, Deploy, Env, And Nginx Legacy Naming Cleanup

Objective: clean legacy deployment and backend naming residue while keeping current local development runnable.

Likely files:

- `docker-compose.yml`
- `docker-entrypoint.sh`
- `Dockerfile`
- `.env.example`
- `backend_py/.env.example`
- `backend_py/alembic.ini`
- `backend_py/main.py`
- `deploy.sh`
- `nginx-valorie.conf`
- `backend_py/app/api/vector_sync.py`

Implementation boundaries:

- Rename legacy image/container/db defaults only after documenting local volume implications.
- Delete `nginx-valorie.conf` or replace it with a neutral template; do not keep Valorie wildcard tenant config.
- Rewrite or delete `deploy.sh`; do not keep certbot instructions for `expert.valorie.ai` or `*.valorie.ai`.
- Remove `X-Tenant-ID` from CORS/preflight and nginx surfaces unless a current backend contract still proves it is necessary.
- Preserve Phase 9-deferred RAG/indexing behavior if a route is still intentionally deferred; only remove organization naming residue that is clearly legacy.

Acceptance:

- Deployment/config files no longer name Valorie or tenant subdomains.
- Backend startup and local dev config remain coherent.
- Backend tests pass if backend code changes.

## Round 5 - Obsolete Docs, Scripts, And Tests Cleanup

Objective: remove or rewrite obsolete user-facing docs and helper files so current users are not pointed at Firebase/Firestore/OpenAI Vector Store/tenant-invite flows.

Likely files:

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

Implementation boundaries:

- Delete obsolete docs rather than preserving them as current instructions.
- Rewrite `README.md` to describe the actual current app state and current verification status; remove inflated test/pass-rate claims.
- Keep `backend_py/tests/**` as the maintained pytest suite.
- Only migrate helper scripts into `backend_py/scripts/` if they are rewritten for current backend/JWT/Postgres/DeepSeek behavior.
- Do not remove guarded provider compatibility files such as `backend_py/app/services/vectorstore/openai_legacy.py` unless a later phase explicitly owns that cleanup.

Acceptance:

- Current docs no longer instruct users to use Firebase, Firestore, tenant invites, Valorie domains, or OpenAI Vector Store sync as live behavior.
- Obsolete helper scripts are deleted or rewritten into maintained script form.
- Test suite still passes.

## Round 6 - Verification, Documentation Closeout, And Reviewer Handoff

Objective: prove the cleanup, document exact evidence, and hand off for review without self-accepting Phase 7.

Required verification:

- Active-surface forbidden string scans for runtime source, config, deploy scripts, current README/user docs, and active tests.
- Active tenant/org/invite/migration route scans.
- Obsolete docs/scripts scans.
- Frontend lint/tests/build.
- Focused backend tests for changed backend/config surfaces.
- Full backend tests when backend app code changes.
- `git diff --check`.
- Browser smoke only when the local backend/Postgres/frontend/seeded-account environment exists.

Closeout rules:

- If Docker/Postgres/seeded credentials are unavailable, record the blocker and leave browser smoke unchecked.
- Do not mark Phase 7 complete before reviewer acceptance.
- List remaining allowed legacy matches explicitly in both `phase-report.md` and `verification.md`.

## Security Risks

- CORS/cookie auth regression: replacing Valorie domain patterns must not permit wildcard credentialed origins.
- CSRF origin checks depend on correct origin classification; app-domain config should be tested with localhost and configured production origins.
- Tenant route removal must not create anonymous access or rely on frontend-only ownership checks.
- Obsolete script deletion must not remove real pytest coverage from `backend_py/tests/**`.
- Docs cleanup must not erase historical security evidence unless explicitly approved.

## Compatibility Risks

- Route changes may break old deep links such as `/{tenantId}/frameworks`; if redirect compatibility is retained temporarily, it must be documented as legacy route compatibility and not a tenant model.
- Removing `getCurrentTenantId` and `tenantId` user state touches several components and tests at once.
- Renaming database defaults or Docker container names can affect existing local volumes and developer scripts.
- `backend_py/alembic.ini` and env examples may still use `valorie` as a sample database name; changing defaults may require updated docs and smoke commands.
- Organization naming in `vector_sync.py` may overlap with Phase 9-deferred indexing stubs; do not delete RAG deferral behavior by string matching.

## Testing Strategy

Minimum frontend verification:

```powershell
cd frontend
npm run lint
npm test
npm run build
```

Minimum backend verification when backend code/config changes:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Suggested focused frontend coverage:

- Login redirects to `/frameworks`.
- Root redirects authenticated users to `/frameworks`.
- Private framework routes require login.
- Framework list create/editor navigation uses personal routes.
- Library remains authenticated.
- Admin route remains backend-authorized.
- Deleted migration, tenant settings, organization, and invite routes are absent or redirect predictably.
- API base URL local/prod behavior uses configured app domain instead of Valorie hardcoding.

Suggested static scans are listed in `verification.md`.

## Verification Checklist

- Active Valorie/domain/customer strings absent from runtime/config/deploy/current README/user docs and active tests, except explicitly allowlisted security/negative assertion tests.
- Active tenant/org/invite/migration route residue absent from frontend runtime.
- Obsolete one-time migration placeholders deleted.
- Obsolete helper scripts deleted or rewritten into maintained scripts.
- README/current docs reflect personal-use backend-JWT/Postgres/DeepSeek direction.
- Frontend lint/tests/build pass.
- Backend tests pass when backend changed.
- Browser smoke status is truthful.
- `phase-report.md`, `verification.md`, and `checklist.md` are updated after implementation.

## Reviewer Handoff Criteria

The reviewer should receive:

- Changed/deleted/rewritten file list grouped by round.
- Inventory classification and final forbidden-scan results.
- Explicit list of remaining allowed matches, especially historical migration docs and security/negative assertion tests, recorded in both `phase-report.md` and `verification.md`.
- Route map before/after for personal-use frontend flow.
- CORS/domain config summary.
- Script/doc deletion rationale.
- Exact frontend lint/test/build outputs.
- Exact backend test outputs when applicable.
- Browser smoke result or explicit blocker.
- Confirmation that no Agent, RAG, LLMWiki, Chat UI, MCP, public registration, tenant/org sharing model, or invite system was added.

## Suggested Executor Prompt For Phase 7 Round 1 Only

```text
Use $migration-phase-executor.

Project:
C:\Users\micha\Desktop\project\framework

Task:
Implement Phase 7 Round 1 only: domain, brand, and active runtime naming cleanup. Do not implement Rounds 2-6. Do not perform code review.

Read first:
- MIGRATION_PHASES.md
- docs/PERSONAL_USE_BOUNDARY.md
- docs/migration/README.md
- docs/migration/decisions/ADR-0001-auth-strategy.md
- docs/migration/phases/phase-06-frontend-defirebase/checklist.md
- docs/migration/phases/phase-06-frontend-defirebase/phase-report.md
- docs/migration/phases/phase-06-frontend-defirebase/verification.md
- docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md
- docs/migration/phases/phase-07-domain-legacy-cleanup/phase-plan.md
- docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md
- docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md

Phase 6 gate:
- Before implementation, verify Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance, browser smoke deferred due unavailable Docker/Postgres/seeded local environment, and Round 6 closeout commit `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- If Phase 6 docs do not record accepted closeout status, stop Phase 7 implementation and correct Phase 6 closeout docs first.

Round 1 scope:
- Replace active Valorie/domain hardcoding in runtime config and app-visible copy.
- Use APP_NAME, APP_BASE_DOMAIN, and SUPER_ADMIN_EMAIL where runtime behavior depends on app name, allowed production domain, or admin identity.
- Remove expert.valorie.ai and *.valorie.ai assumptions from frontend API base URL logic.
- Remove valorie.ai CORS origin patterns from backend startup code without weakening credentialed CORS.
- Remove Valorie-branded user-facing copy from login, landing, navigation, and app chrome.
- Update env examples as needed so backend and frontend deployment configuration is explicit.
- Update focused tests for the changed active runtime and app-visible behavior.

Round 1 non-goals:
- Do not delete /migrate, tenant, organization, invite, or placeholder routes yet.
- Do not remove TenantRoute, tenantId route shims, getCurrentTenantId, or organization sharing UI yet unless a Valorie-domain string cannot otherwise be removed safely.
- Do not rewrite README or obsolete docs yet.
- Do not delete backend helper scripts yet.
- Do not rename Docker containers/images/database defaults yet unless required for an active Valorie string touched in this round.
- Do not implement Agent, Tool Registry, RAG, LLMWiki, Chat UI, Skill Registry, MCP, public registration, SaaS tenant/org sharing, or new invites.
- Do not claim browser smoke unless actually run.

Acceptance:
- Active runtime/config files touched in Round 1 no longer hardcode valorie.ai, expert.valorie.ai, webmaster@valorie, framework-builder-55896, UNSW, or ad.unsw.
- Backend CORS still permits localhost/127.0.0.1 development origins and only configured production origins for credentialed requests.
- Frontend API base URL behavior still supports local development and configured deployment.
- Frontend lint/tests/build pass for the touched frontend surfaces.
- Focused backend tests pass if backend startup/CORS code changes.
- Update Phase 7 checklist, phase-report, and verification with exact commands/results, but do not mark Phase 7 complete.
```
