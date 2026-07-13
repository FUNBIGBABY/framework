# Phase 07 Checklist - Domain and Legacy Cleanup

## Governance Reconciliation - 2026-07-10

- [x] Record current verdict as `pending`.
- [x] Record `fa97afd2de0fd9dea66fe86a519f440285717552` as a pushed candidate only, not an accepted closeout/commit.
- [x] Keep browser smoke as `not run`, not passed. Historical blocker: unavailable Docker Desktop Linux engine plus no live Postgres/pgvector, migrated schema, running backend/frontend, or seeded credentials. Current additional static blocker: the Dockerfile's Node 18 builder is incompatible with the locked Vite 7.1.9 / React Router 7.9.3 engine requirements.
- [x] Assign Container Runtime Owner to the build blocker, triggered by a separately reviewed compatible runtime candidate. Assign Migration Verification Owner to browser smoke, triggered after that correction and the complete authorized environment are available, before a release relying on these flows, or as an explicit later reviewer condition.
- [x] Record that missing browser smoke is not automatically a blocker and that a named reviewer may use `accepted_with_documented_deferral` with explicit conditions/owner/trigger; `conditions=none` is not required.
- [ ] Obtain the named reviewer verdict and append it to `docs/migration/REVIEW_LEDGER.md`.
- [ ] Keep Phase 8 planning blocked until that ledger verdict is `accepted` or `accepted_with_documented_deferral`; do not implement Phase 8 before its planning package is reviewed.

Materials ownership is a P1 remediation, not reviewer-attention-only. The remediation leaves pre-existing rows ownerless without arbitrary backfill or deletion and quarantines them from authenticated retrieval. Security Owner + Backend Owner must approve a verified legacy-owner mapping or other explicit disposition before Phase 7 acceptance or any multi-user/production use; ownerless-row unquarantine remains blocked until then. The legacy `vector_sync` HTTP 501 shells are quarantined deferred compatibility surfaces, not parity; Phase 9 RAG Replacement Owner owns any future replacement without implementation in this correction.

- [x] Dormant legacy/security cleanup: repository-wide import, mount, and dynamic-discovery scans found `backend_py/app/api/test.py` unreferenced and unmounted, so the unauthenticated duplicate `/materials` router was deleted. This records removal of a dormant reactivation risk, not a claim that the router was currently reachable; `app.api.materials` remains the sole application router defining that prefix.

Round 0/1 implementation status: fresh inventory and domain/brand active runtime naming cleanup have evidence recorded in `phase-report.md` and `verification.md`. A requested deploy/nginx/docker naming cleanup pass was performed on 2026-07-02. Migration placeholder route/tool cleanup was performed on 2026-07-05. A frontend personal-route cleanup slice was performed on 2026-07-06. An unmounted frontend tenant/org/invite placeholder cleanup slice was performed on 2026-07-07. A frontend organization-sharing UI residue cleanup slice was performed on 2026-07-07. A frontend AuthContext tenant/org state cleanup slice was performed on 2026-07-08. A frontend API request-normalization cleanup slice was performed on 2026-07-08. Obsolete current docs/scripts cleanup was performed on 2026-07-09. Do not mark Phase 7 complete from this document: the review verdict remains pending. Browser smoke is not run, but that absence is not automatically a blocker. Historical Phase 7 execution relied on the Phase 6 accepted-with-deferral handoff that is now superseded for current audit status by `P6-DEFIREBASE-CORRECTION-01`; the historical execution evidence remains unchanged.

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
- [x] Apply the canonical active-surface acceptance rule: runtime source, config, deploy scripts, current README/user docs, and active tests must have zero forbidden legacy-string matches, except explicitly allowlisted security/negative assertion tests.
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

- [x] Delete one-time frontend migration and cleanup placeholder files left from Phase 6.
- [x] Remove the `/migrate` route from the active route tree.
- [x] Remove any migration/cleanup buttons or imports from active UI.
- [x] Remove tests that only prove isolated migration placeholders render.

Likely files:

- [x] `frontend/src/migrate-data.js`
- [x] `frontend/src/utils/cleanupData.js`
- [x] `frontend/src/utils/DataCleanupButton.jsx`
- [x] `frontend/src/utils/updateFrameworkTenants.js`
- [x] `frontend/src/components/MigrationTool.jsx`
- [x] `frontend/src/App.jsx`
- [x] `frontend/src/App.route.test.jsx`

Acceptance criteria:

- [x] No active frontend route exposes migration or cleanup tooling.
- [x] Deleted placeholders are not imported by active source or tests.
- [x] Frontend lint/tests/build remain green.

## Round 3 - Personal Route Flow And Tenant/Org/Invite Cleanup

- [x] Inventory-only pass on 2026-07-06 classified tenant/org/invite references across backend, frontend, tests, docs, database models, migrations, schemas, route guards, services, and env/config; no runtime code, auth/session behavior, models, or migrations were changed.
- [x] Docs-only inventory repair on 2026-07-06 documented the `frontend/src/lib/api.js` split-string identity-strip guard and the `UpdateFrameworksButton.jsx` active import/render path; no runtime implementation or cleanup began.
- [x] Replace `/:tenantId/*` route shells with personal-use routes that do not encode tenant identity.
- [x] Remove `TenantRoute` from the active routing path and rely on `PrivateRoute` plus backend ownership checks.
- [x] Delete or permanently remove active imports for tenant, organization, and invite placeholder components.
- [x] Delete confirmed-unmounted tenant, organization, and invite placeholder component files.
- [x] Remove `tenantId`, `joinedOrganization`, and organization access fields from frontend auth user state unless a narrowly documented compatibility test still needs them as legacy input.
- [x] Remove `getCurrentTenantId` route/domain shim from active route generation.
- [x] Update navigation targets in create, editor, framework cards, and framework lists to the new personal route shape.
- [x] Remove organization sharing UI and inert "Publish to Organization" actions.
- [x] Delete the null `UpdateFrameworksButton.jsx` org-field repair placeholder and remove its active import/render path.
- [x] Remove obsolete `publishedToOrganization` normalization from `frontend/src/lib/api.js`.
- [x] Replace the `api.js` split-string `tenant_id` / `X-Tenant-ID` artefact guard with a neutral client-owned identity-field stripper that preserves defense-in-depth without retaining tenant/header fixtures in runtime code.
- [x] Preserve authenticated public library behavior; do not make library anonymous.

Likely files:

- [x] `frontend/src/App.jsx`
- [x] `frontend/src/contexts/AuthContext.jsx`
- [x] `frontend/src/lib/api.js`
- [x] `frontend/src/components/TenantRoute.jsx`
- [x] `frontend/src/components/TenantCreationModal.jsx`
- [x] `frontend/src/components/TenantSettings.jsx`
- [x] `frontend/src/components/YourOrganization.jsx`
- [x] `frontend/src/components/InviteAccept.jsx`
- [x] `frontend/src/components/Navbar.jsx`
- [x] `frontend/src/components/Login.jsx`
- [x] `frontend/src/components/CreateFramework.jsx`
- [x] `frontend/src/components/FrameworkEditor.jsx`
- [x] `frontend/src/components/FrameworkCard.jsx`
- [x] `frontend/src/components/YourFrameworks.jsx`
- [x] `frontend/src/components/UpdateFrameworksButton.jsx` deleted
- [x] route/component tests
- [x] `frontend/src/contexts/AuthContext.test.jsx`

Acceptance criteria:

- [x] Normal login routes to a personal framework list path without a tenant segment.
- [x] Owner list, create, editor, save, publish/unpublish, library, admin, and logout navigation still work through personal-use routes.
- [x] Tenant, organization, and invite route components are removed from active source.
- [x] Backend remains the authority for framework ownership and admin access.

## Round 4 - Backend, Deploy, Env, And Nginx Legacy Naming Cleanup

- [x] Rename legacy container/image/database defaults only where they are naming residue, documenting any local volume reset implications.
- [x] Delete `nginx-valorie.conf` or replace it with a neutral deployment template only if Phase 7 owns the replacement.
- [x] Rewrite or delete `deploy.sh` so it no longer provisions Valorie domains or wildcard tenant subdomains.
- [x] Remove `X-Tenant-ID` from CORS/preflight/deploy surfaces unless a current backend contract still requires it.
- [x] Inspect backend for tenant/org/invite route residue; delete only confirmed inert routes, and do not remove Phase 9-deferred RAG stubs by accident.
- [x] Review `backend_py/app/api/vector_sync.py` for organization naming residue while preserving its Phase 9-deferred behavior if still needed.

Likely files:

- [x] `docker-compose.yml`
- [x] `docker-entrypoint.sh`
- [x] `Dockerfile` inspected; no Phase 7 naming change needed in Round 4/5.
- [x] `.env.example`
- [x] `backend_py/.env.example`
- [x] `backend_py/alembic.ini`
- [x] `backend_py/main.py`
- [x] `deploy.sh`
- [x] `nginx-valorie.conf` deleted and replaced by `nginx-framework.conf`
- [x] `backend_py/app/api/vector_sync.py` reviewed and preserved as Phase 9-deferred RAG/indexing stub.

Acceptance criteria:

- [x] Deployment files no longer reference Valorie domains, Valorie container names, tenant subdomains, or obsolete nginx tenant headers.
- [x] Local development defaults remain documented and runnable, with the local Docker volume implication recorded in `phase-report.md`.
- [x] No new infrastructure stack is introduced beyond the cleanup needed for Phase 7.

## Round 5 - Obsolete Docs, Scripts, And Tests Cleanup

- [x] Delete or rewrite obsolete Firebase-first, Firestore-first, OpenAI Vector Store migration, and customer deployment docs.
- [x] Rewrite `README.md` to describe the current personal-use app state without inflated test/pass-rate claims.
- [x] Delete obsolete top-level backend helper scripts that are not pytest tests and are not current admin/deploy tooling.
- [x] Move any still-useful script into `backend_py/scripts/` only after rewriting it for the current backend/JWT/Postgres/DeepSeek contracts; no moved script was needed in this slice.
- [x] Keep real pytest tests under `backend_py/tests/`; update or delete tests that only cover removed route shims.
- [x] Preserve intentional provider compatibility files such as guarded legacy vectorstore code unless a later phase owns their removal.

Likely files:

- [x] `README.md`
- [x] `Project-Startup-and-Operation-Flow.md` deleted
- [x] `firebaseDoc.md` deleted
- [x] `backend_py/README-DIFF.md` deleted
- [x] `docs/CN_DEPLOY.md` inspected and preserved as current DeepSeek deployment note
- [x] `backend_py/test_firebase.py` deleted
- [x] `backend_py/test_cloud_llm.py` deleted
- [x] `backend_py/test_update.py` deleted
- [x] `backend_py/test_update_publish.py` deleted
- [x] `backend_py/test_vec_base.py` deleted
- [x] `backend_py/check_versions.py` deleted
- [x] `backend_py/check_vector_store_attributes.py` deleted
- [x] `backend_py/diagnose_env.py` inspected and preserved as current DeepSeek/provider env diagnostic
- [x] frontend/backend tests affected by deleted routes or docs; no maintained tests required changes in this slice

Acceptance criteria:

- [x] Obsolete docs no longer instruct users to use Firebase, Firestore, tenant invites, Valorie domains, or OpenAI Vector Store sync as current behavior.
- [x] Obsolete helper scripts are deleted or rewritten into current `scripts/` tooling.
- [x] `README.md` accurately describes current capabilities and deferred browser smoke status.

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
- [x] Frontend `npm test`.
- [x] Frontend `npm run build`.
- [x] Focused AuthContext/auth-state tests.
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
- [ ] The ledger entry names the reviewer/date and records `accepted` or `accepted_with_documented_deferral`; any deferral states exact conditions, owner, and trigger.
- [ ] Phase 8 planning gate remains closed until that ledger record exists; no `conditions=none` requirement is imposed.
