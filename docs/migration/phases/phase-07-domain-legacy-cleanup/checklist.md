# Phase 07 Checklist - Domain and Legacy Cleanup

Round 0/1 implementation status: fresh inventory and domain/brand active runtime naming cleanup have evidence recorded in `phase-report.md` and `verification.md`. A requested deploy/nginx/docker naming cleanup pass was also performed on 2026-07-02. Do not mark Phase 7 complete from this document; later migration placeholder, tenant/org/invite route, obsolete docs/scripts, browser smoke, and reviewer acceptance work remain pending. Phase 7 execution relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

## Required Context

- [x] Read `MIGRATION_PHASES.md`, especially Phase 7 and the Phase 8 boundary.
- [x] Read `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Read `docs/migration/README.md`.
- [x] Read `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Read Phase 6 `checklist.md`, `phase-report.md`, and `verification.md`.
- [x] Confirm Phase 6 `checklist.md`, `phase-report.md`, and `verification.md` record Migration Reviewer closeout acceptance before starting or merging Phase 7 implementation.
- [x] Gate Phase 7 implementation if Phase 6 closeout docs do not record accepted status.
- [x] Confirm Phase 6 browser smoke remains deferred unless it has actually been run in the current environment.
- [x] Confirm Phase 7 does not reopen Phase 6 Firebase SDK, bearer/localStorage, or backend Bearer compatibility work.

## Phase Guardrails

- [x] Keep Phase 7 focused on semantic cleanup of Valorie/domain, tenant, organization, invite, migration, obsolete docs, obsolete scripts/tests, and legacy deployment naming residue.
- [x] Do not implement Agent loop, Tool Registry, Skill Registry, Chat UI, RAG, LLMWiki, MCP marketplace, public registration, OAuth, Firebase Auth, Firestore, or a SaaS tenant/org sharing model.
- [x] Do not introduce new invite, organization, workspace, or public marketplace behavior.
- [x] Do not perform broad UI redesign; route and navigation changes should support the personal-use app flow only.
- [x] Preserve personal-use auth boundaries: private routes require backend cookie-session auth and public signup remains disabled.
- [x] Do not claim browser smoke unless a browser session was actually run against a live backend/Postgres environment.
- [x] Preserve historical migration records unless an explicit owner decision allows rewriting them.
- [ ] Apply the canonical active-surface acceptance rule: runtime source, config, deploy scripts, current README/user docs, and active tests must have zero forbidden legacy-string matches, except explicitly allowlisted security/negative assertion tests.
- [x] Allowlisted historical migration records and security/negative assertion tests must be recorded in both `phase-report.md` and `verification.md`, and the allowlist must not hide active runtime/config/deploy/current-doc residue.

## Round 0 - Fresh Inventory And Boundary Confirmation

- [x] Re-read the canonical Phase 7 section in `MIGRATION_PHASES.md`.
- [x] Reconcile Phase 7 scope with the personal-use boundary and ADR-0001.
- [x] Re-read Phase 6 closeout docs and list the residue intentionally deferred to Phase 7.
- [x] Run focused scans for `valorie`, `Valorie`, `valorie.ai`, `expert.valorie.ai`, `framework-builder-55896`, `webmaster@valorie`, `UNSW`, and `ad.unsw`.
- [x] Run focused scans for `tenant`, `Tenant`, `organization`, `Organization`, `invite`, `Invite`, `MigrationTool`, `migrate-data`, `cleanupData`, and `updateFrameworkTenants`.
- [x] Classify each hit as active runtime, route/navigation, placeholder tool, backend/config/deploy, obsolete script/test, obsolete doc, migration-history record, or intentional security negative assertion.
- [x] Decide and document the verification allowlist for historical `docs/migration/phases/**` records and security/negative assertion tests before implementation changes begin.

Acceptance criteria:

- [x] The executor has a file/module inventory grouped by cleanup category.
- [x] The reviewer handoff criteria distinguish active-surface cleanup from explicitly allowlisted historical documentation and security/negative-test exceptions.
- [x] The canonical active-surface acceptance rule is reflected in `MIGRATION_PHASES.md`, `phase-report.md`, and `verification.md`.

## Round 1 - Domain, Brand, And Active Runtime Naming Cleanup

- [x] Replace active Valorie/domain hardcoding in app-visible strings and runtime config with neutral personal-use naming.
- [x] Use `APP_NAME`, `APP_BASE_DOMAIN`, and `SUPER_ADMIN_EMAIL` where runtime behavior depends on app name, allowed domain, or admin email.
- [x] Remove or replace `expert.valorie.ai` and `*.valorie.ai` production domain assumptions from frontend API base URL logic.
- [x] Remove or replace `valorie.ai` CORS origin patterns in backend startup code without weakening credentialed CORS.
- [x] Remove Valorie-branded user-facing copy from login, landing, navigation, and app chrome.
- [x] Keep admin checks backend-authoritative through `SUPER_ADMIN_EMAIL`.
- [x] Update tests that assert old Valorie or route-copy behavior.

Likely files:

- [x] `backend_py/main.py`
- [x] `.env.example`
- [x] `backend_py/.env.example`
- [x] `frontend/src/lib/api.js`
- [x] `frontend/src/components/Login.jsx`
- [x] `frontend/src/components/LandingPage.jsx`
- [x] `frontend/src/components/Navbar.jsx`
- [x] frontend tests touching API base URL, login, routes, or navigation

Acceptance criteria:

- [x] Active runtime files no longer hardcode `valorie.ai`, `expert.valorie.ai`, `webmaster@valorie`, `framework-builder-55896`, `UNSW`, or `ad.unsw`.
- [x] Backend CORS still accepts local development origins and configured production origins without wildcard credentialed access.
- [x] Frontend API base URL behavior still supports local development and configured deployment.

## Round 2 - Legacy Migration Tool And Placeholder Removal

- [ ] Delete one-time frontend migration and cleanup placeholder files left from Phase 6.
- [ ] Remove the `/migrate` route from the active route tree.
- [ ] Remove any migration/cleanup buttons or imports from active UI.
- [ ] Remove tests that only prove isolated migration placeholders render.

Likely files:

- [ ] `frontend/src/migrate-data.js`
- [ ] `frontend/src/utils/cleanupData.js`
- [ ] `frontend/src/utils/DataCleanupButton.jsx`
- [ ] `frontend/src/utils/updateFrameworkTenants.js`
- [ ] `frontend/src/components/MigrationTool.jsx`
- [ ] `frontend/src/App.jsx`
- [ ] `frontend/src/App.route.test.jsx`

Acceptance criteria:

- [ ] No active frontend route exposes migration or cleanup tooling.
- [ ] Deleted placeholders are not imported by active source or tests.
- [ ] Frontend lint/tests/build remain green.

## Round 3 - Personal Route Flow And Tenant/Org/Invite Cleanup

- [ ] Replace `/:tenantId/*` route shells with personal-use routes that do not encode tenant identity.
- [ ] Remove `TenantRoute` from the active routing path and rely on `PrivateRoute` plus backend ownership checks.
- [ ] Delete or permanently remove active imports for tenant, organization, and invite placeholder components.
- [ ] Remove `tenantId`, `joinedOrganization`, and organization access fields from frontend auth user state unless a narrowly documented compatibility test still needs them as legacy input.
- [ ] Remove `getCurrentTenantId` route/domain shim from active route generation.
- [ ] Update navigation targets in create, editor, framework cards, and framework lists to the new personal route shape.
- [ ] Remove organization sharing UI and inert "Publish to Organization" actions.
- [ ] Preserve authenticated public library behavior; do not make library anonymous.

Likely files:

- [ ] `frontend/src/App.jsx`
- [ ] `frontend/src/contexts/AuthContext.jsx`
- [ ] `frontend/src/lib/api.js`
- [ ] `frontend/src/components/TenantRoute.jsx`
- [ ] `frontend/src/components/TenantCreationModal.jsx`
- [ ] `frontend/src/components/TenantSettings.jsx`
- [ ] `frontend/src/components/YourOrganization.jsx`
- [ ] `frontend/src/components/InviteAccept.jsx`
- [ ] `frontend/src/components/Navbar.jsx`
- [ ] `frontend/src/components/Login.jsx`
- [ ] `frontend/src/components/CreateFramework.jsx`
- [ ] `frontend/src/components/FrameworkEditor.jsx`
- [ ] `frontend/src/components/FrameworkCard.jsx`
- [ ] `frontend/src/components/YourFrameworks.jsx`
- [ ] route/component tests

Acceptance criteria:

- [ ] Normal login routes to a personal framework list path without a tenant segment.
- [ ] Owner list, create, editor, save, publish/unpublish, library, admin, and logout navigation still work through personal-use routes.
- [ ] Tenant, organization, and invite route components are removed from active source.
- [ ] Backend remains the authority for framework ownership and admin access.

## Round 4 - Backend, Deploy, Env, And Nginx Legacy Naming Cleanup

- [x] Rename legacy container/image/database defaults only where they are naming residue, documenting any local volume reset implications.
- [x] Delete `nginx-valorie.conf` or replace it with a neutral deployment template only if Phase 7 owns the replacement.
- [x] Rewrite or delete `deploy.sh` so it no longer provisions Valorie domains or wildcard tenant subdomains.
- [x] Remove `X-Tenant-ID` from CORS/preflight/deploy surfaces unless a current backend contract still requires it.
- [ ] Inspect backend for tenant/org/invite route residue; delete only confirmed inert routes, and do not remove Phase 9-deferred RAG stubs by accident.
- [ ] Review `backend_py/app/api/vector_sync.py` for organization naming residue while preserving its Phase 9-deferred behavior if still needed.

Likely files:

- [x] `docker-compose.yml`
- [x] `docker-entrypoint.sh`
- [ ] `Dockerfile`
- [ ] `.env.example`
- [ ] `backend_py/.env.example`
- [ ] `backend_py/alembic.ini`
- [x] `backend_py/main.py`
- [x] `deploy.sh`
- [x] `nginx-valorie.conf` deleted and replaced by `nginx-framework.conf`
- [ ] `backend_py/app/api/vector_sync.py`

Acceptance criteria:

- [x] Deployment files no longer reference Valorie domains, Valorie container names, tenant subdomains, or obsolete nginx tenant headers.
- [x] Local development defaults remain documented and runnable, with the local Docker volume implication recorded in `phase-report.md`.
- [x] No new infrastructure stack is introduced beyond the cleanup needed for Phase 7.

## Round 5 - Obsolete Docs, Scripts, And Tests Cleanup

- [ ] Delete or rewrite obsolete Firebase-first, Firestore-first, OpenAI Vector Store migration, and customer deployment docs.
- [ ] Rewrite `README.md` to describe the current personal-use app state without inflated test/pass-rate claims.
- [ ] Delete obsolete top-level backend helper scripts that are not pytest tests and are not current admin/deploy tooling.
- [ ] Move any still-useful script into `backend_py/scripts/` only after rewriting it for the current backend/JWT/Postgres/DeepSeek contracts.
- [ ] Keep real pytest tests under `backend_py/tests/`; update or delete tests that only cover removed route shims.
- [ ] Preserve intentional provider compatibility files such as guarded legacy vectorstore code unless a later phase owns their removal.

Likely files:

- [ ] `README.md`
- [ ] `Project-Startup-and-Operation-Flow.md`
- [ ] `firebaseDoc.md`
- [ ] `backend_py/README-DIFF.md`
- [ ] `docs/CN_DEPLOY.md`
- [ ] `backend_py/test_firebase.py`
- [ ] `backend_py/test_cloud_llm.py`
- [ ] `backend_py/test_update.py`
- [ ] `backend_py/test_update_publish.py`
- [ ] `backend_py/test_vec_base.py`
- [ ] `backend_py/check_versions.py`
- [ ] `backend_py/check_vector_store_attributes.py`
- [ ] `backend_py/diagnose_env.py`
- [ ] frontend/backend tests affected by deleted routes or docs

Acceptance criteria:

- [ ] Obsolete docs no longer instruct users to use Firebase, Firestore, tenant invites, Valorie domains, or OpenAI Vector Store sync as current behavior.
- [ ] Obsolete helper scripts are deleted or rewritten into current `scripts/` tooling.
- [ ] `README.md` accurately describes current capabilities and deferred browser smoke status.

## Round 6 - Verification, Documentation Closeout, And Reviewer Handoff

- [ ] Run all Phase 7 static scans and record exact commands/results in `verification.md`.
- [ ] Run frontend lint/tests/build and record exact outputs.
- [ ] Run focused backend tests and full backend tests if backend/config files changed.
- [ ] Run browser smoke only if Docker/Postgres/backend/frontend and seeded credentials are available.
- [ ] If browser smoke cannot run, record the exact blocker and do not claim browser coverage.
- [ ] Update `phase-report.md` with changed/removed/rewritten file lists and known deferrals.
- [ ] Update this checklist with evidence-backed task status only after implementation.
- [ ] Prepare reviewer handoff with scope, non-goals, residual allowed matches, verification evidence, and browser-smoke status.

Acceptance criteria:

- [ ] Active-surface forbidden scans pass: runtime source, config, deploy scripts, current README/user docs, and active tests have zero forbidden legacy-string matches, except explicitly allowlisted security/negative assertion tests.
- [ ] Lint/tests/build/backend tests pass or have documented, non-hidden blockers.
- [ ] The reviewer can see exactly which historical docs or negative tests still contain legacy strings and why.
- [ ] Phase 7 is not marked complete until reviewer acceptance.

## Explicit Non-Goals

- [ ] No Agent loop or Tool Registry.
- [ ] No RAG indexing, retrieval, or citations.
- [ ] No LLMWiki.
- [ ] No Chat UI or Skill Registry.
- [ ] No MCP marketplace.
- [ ] No public registration.
- [ ] No SaaS tenant, organization sharing, workspace sharing, or invite model.
- [ ] No new invite system.
- [ ] No broad UI redesign.
- [ ] No browser smoke claim unless actually run.

## Verification Checklist

- [x] Active-surface Valorie/domain/customer string scan.
- [x] Active tenant/org/invite/migration route scan.
- [x] Obsolete script/test/doc scan.
- [x] Deploy/nginx/docker legacy naming scan.
- [x] `docker compose config`.
- [x] Frontend `npm run lint`.
- [ ] Frontend `npm test`.
- [x] Frontend `npm run build`.
- [x] Backend focused pytest for changed app surfaces.
- [ ] Backend full pytest if backend app/config changed.
- [x] `git diff --check`.
- [ ] Browser smoke with login/personal routes/framework/library/admin/logout only if local environment is available.

## Reviewer Handoff Criteria

- [ ] Phase 7 report lists every file changed, deleted, or rewritten.
- [ ] Phase 7 report lists all remaining allowed legacy-string matches and excludes no active runtime/config/deploy/current-doc residue silently.
- [ ] Verification includes exact commands and outputs.
- [ ] Browser smoke status is explicit: run with results, or deferred with exact environment blocker.
- [ ] Personal-use boundary remains enforced.
- [ ] No future-phase features were introduced.
- [ ] Phase 7 is left pending reviewer acceptance, not self-completed.
