# Phase 07 Verification - Domain and Legacy Cleanup

Round 0/1 implementation status: this document defines the verification contract, records initial planning scans, and now records Round 0/1 implementation verification. It does not mark Phase 7 complete. Phase 7 execution relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

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
- `backend_py/tests/test_main.py`: retains `https://expert.valorie.ai` only as an intentional negative assertion proving the old Valorie production origin is no longer accepted by backend CORS.
- `frontend/src/lib/api.test.js`: retains `tenant_id` and `X-Tenant-ID` only as intentional negative assertions proving frontend request payload/header helpers strip client-supplied identity fields.

These allowlist entries do not cover active runtime/config/deploy/current-doc residue. Active deploy residue in `deploy.sh` and `nginx-valorie.conf`, and active tenant/org/invite/migration route residue, remain explicit Phase 7 follow-up work rather than allowlisted closeout exceptions.

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
