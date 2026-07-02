# Phase 07 Verification - Domain and Legacy Cleanup

Planning status: documentation only. This document defines the verification contract and records initial planning scans. It does not verify Phase 7 implementation and does not mark Phase 7 complete. Phase 7 planning relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

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

- Phase 6 closeout is recorded as accepted by Migration Reviewer in the Phase 6 checklist, report, and verification docs.
- Round 6 closeout commit: `27679f8 Complete Phase 6 frontend de-Firebase closeout`.
- Browser smoke remains deferred because Docker/Postgres/seeded local environment was unavailable; this document must not convert that deferral into a run result.

## Allowlist Record

No Phase 7 implementation allowlist has been populated yet. Before Phase 7 can close, any retained historical migration-record matches or intentional security/negative assertion test matches must be listed here and in `phase-report.md` with file paths, matched terms, and rationale.

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
rg -n "valorie|Valorie|expert\.valorie\.ai|tenant|X-Tenant-ID|nginx-valorie" Dockerfile docker-compose.yml docker-entrypoint.sh deploy.sh nginx-valorie.conf .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py backend_py/app
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
