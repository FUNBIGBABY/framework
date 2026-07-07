# Phase 07 Verification - Domain and Legacy Cleanup

Round 0/1 implementation status: this document defines the verification contract, records initial planning scans, and records Round 0/1 implementation verification. A requested deploy/nginx/docker naming cleanup pass was verified on 2026-07-02. Migration placeholder route/tool cleanup was verified on 2026-07-05. Frontend personal-route cleanup was verified on 2026-07-06. Unmounted frontend tenant/org/invite placeholder cleanup was verified on 2026-07-07. It does not mark Phase 7 complete. Phase 7 execution relies on the corrected Phase 6 closeout docs recording Migration Reviewer acceptance.

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
- `backend_py/tests/test_main.py`: retains `https://expert.valorie.ai` and `X-Tenant-ID` only as intentional negative assertions proving the old Valorie production origin is no longer accepted by backend CORS and the legacy tenant header is no longer advertised by backend preflight handling.
- `frontend/src/lib/api.test.js`: retains `tenant_id` and `X-Tenant-ID` only as intentional negative assertions proving frontend request payload/header helpers strip client-supplied identity fields.

These allowlist entries do not cover active runtime/config/deploy/current-doc residue. The deploy/nginx/docker naming residue previously present in `deploy.sh`, `nginx-valorie.conf`, `docker-compose.yml`, `docker-entrypoint.sh`, and backend preflight handling has now been cleaned. The active `/migrate` route and isolated migration placeholder files have now been removed. Active tenant/org/invite route residue and obsolete current-doc/script residue remain explicit Phase 7 follow-up work rather than allowlisted closeout exceptions.

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

## Requested Deploy/Nginx/Docker Naming Cleanup Verification - 2026-07-02

### Baseline Working Tree And Commit

Command:

```powershell
git status --short
```

Outcome before this pass:

```text
No stdout. Working tree was clean.
```

Command:

```powershell
git log -5 --oneline
```

Outcome:

```text
1d489d3 Complete Phase 7 Round 0/1 domain cleanup
ea32cbf Fix Phase 6 closeout docs and Phase 7 planning
27679f8 Complete Phase 6 frontend de-Firebase closeout
68a03e3 Implement Phase 6 Round 5 artefact wiring
3179837 Implement Phase 6 Round 4 admin REST wiring
```

### Initial Focused Deploy Legacy Scan

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|expert\.valorie\.ai|valorie\.ai|nginx-valorie|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" deploy.sh nginx-valorie.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py -g "!.git"
```

Outcome:

```text
Exit 0. Active deployment/config matches were found in `docker-entrypoint.sh`, `docker-compose.yml`, `deploy.sh`, and `nginx-valorie.conf`.
Key matches included `Starting Valorie Framework Builder`, `valorie-db`, `valorie-app`, `valorie-framework-builder:latest`, `POSTGRES_DB`/`POSTGRES_USER`/`DATABASE_URL` defaults using `valorie`, `nginx-valorie.conf`, `expert.valorie.ai`, `*.valorie.ai`, and wildcard Valorie nginx server names.
```

Command:

```powershell
rg -n --hidden -S "tenant|Tenant|X-Tenant-ID|organization|Organization|invite|Invite|server_name|ssl_certificate|container_name|image:|POSTGRES_DB|POSTGRES_USER|DATABASE_URL" deploy.sh nginx-valorie.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py
```

Outcome:

```text
Exit 0. Active deployment/config matches included backend preflight `X-Tenant-ID`, wildcard tenant nginx `server_name` entries, `proxy_set_header X-Tenant-ID $tenant`, Valorie container/image/database defaults, and neutral env-example database defaults from Round 0/1.
```

### Backend Contract Check For Tenant Header

Command:

```powershell
rg -n --hidden -S "X-Tenant-ID|tenant_id|tenantId|include_organization|organization" backend_py/app backend_py/tests docker-compose.yml docker-entrypoint.sh deploy.sh nginx-valorie.conf .env.example backend_py/.env.example -g "!backend_py/.venv"
```

Outcome:

```text
nginx-valorie.conf:77:        proxy_set_header X-Tenant-ID $tenant;
backend_py/app\api\vector_sync.py:19:    include_organization: bool = True
```

Interpretation: no active backend route consumes `X-Tenant-ID`; the remaining backend app hit is `include_organization` in the Phase 9-deferred vector sync request shape, which this pass did not change.

### Post-Edit Active Deploy Legacy Scan

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|expert\.valorie\.ai|valorie\.ai|nginx-valorie|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py backend_py/tests/test_main.py -g "!.git"
```

Outcome:

```text
backend_py/tests/test_main.py:29:    assert not main.is_valid_origin("https://expert.valorie.ai")
```

Interpretation: no active deploy/config files in the command contain Valorie/customer deployment naming. The remaining match is an allowlisted negative CORS assertion.

Command:

```powershell
rg -n --hidden -S "X-Tenant-ID|nginx-valorie|server_name ~|\*\.valorie|tenant subdomain|valorie-db|valorie-app|valorie-framework-builder" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh backend_py/main.py backend_py/tests/test_main.py
```

Outcome:

```text
The only match was the allowlisted negative preflight assertion in
`backend_py/tests/test_main.py`: `assert "X-Tenant-ID" not in allowed_headers`.
The exact line number is intentionally omitted because it is not part of the
acceptance evidence.
```

Interpretation: no active deploy/config files in the command contain legacy tenant nginx/header naming. The remaining match is an allowlisted negative preflight assertion.

### Docker Compose Config

Command:

```powershell
docker compose config
```

Outcome:

```text
Exit 0. Rendered config included `container_name: framework-app`, `container_name: framework-db`, `image: framework-builder:latest`, `POSTGRES_DB: framework`, `POSTGRES_USER: framework`, `DATABASE_URL: postgresql+psycopg://framework:change-me@db:5432/framework`, `APP_NAME: Personal AI Framework Studio`, `FRONTEND_URL: http://localhost:5173`, and `APP_BASE_DOMAIN: ""`.
Warnings:
time="2026-07-02T21:25:19+08:00" level=warning msg="The \"JWT_SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-07-02T21:25:19+08:00" level=warning msg="The \"DEEPSEEK_API_KEY\" variable is not set. Defaulting to a blank string."
time="2026-07-02T21:25:19+08:00" level=warning msg="C:\\Users\\micha\\Desktop\\project\\framework\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
```

### Backend Focused Tests

Initial meaningful run after adding a preflight assertion:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q tests/test_main.py
```

Outcome:

```text
1 failed, 3 passed, 3 warnings in 10.23s.
Failure: `TestClient(main.app)` raised `TypeError: Client.__init__() got an unexpected keyword argument 'app'` due the current Starlette/httpx versions. The test was rewritten to call `CustomCORSMiddleware.dispatch()` directly instead of using `TestClient`.
```

Corrected command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q tests/test_main.py
```

Outcome:

```text
4 passed, 3 warnings in 9.92s.
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

### Shell And Nginx Config Validators

Command:

```powershell
Get-Command bash -All -ErrorAction SilentlyContinue | Select-Object Source,CommandType
```

Outcome:

```text
Source                       CommandType
------                       -----------
C:\WINDOWS\system32\bash.exe Application
```

Command:

```powershell
bash -n deploy.sh
```

Outcome:

```text
Exit 1. Windows launched the WSL `bash.exe` shim and failed before reading `deploy.sh` because WSL is not installed/configured in this environment. The terminal rendered the failure as mojibake, but it included WSL guidance for `wsl.exe --list --online` and `wsl.exe --install <Distro>`.
```

Command:

```powershell
Get-Command nginx -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
```

Outcome:

```text
No stdout. Command exited 1.
```

Nginx syntax validation result: not run because `nginx` is unavailable on PATH in this environment.

### Final Post-Documentation Scans And Whitespace Check

Command:

```powershell
rg -n --hidden -S "valorie|Valorie|expert\.valorie\.ai|valorie\.ai|nginx-valorie|framework-builder-55896|webmaster@valorie|UNSW|ad\.unsw" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh Dockerfile .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py -g "!.git"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n --hidden -S "X-Tenant-ID|nginx-valorie|server_name ~|\*\.valorie|tenant subdomain|valorie-db|valorie-app|valorie-framework-builder|ssl_certificate" deploy.sh nginx-framework.conf docker-compose.yml docker-entrypoint.sh backend_py/main.py
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path -LiteralPath nginx-valorie.conf
```

Outcome:

```text
False
```

Command:

```powershell
Test-Path -LiteralPath nginx-framework.conf
```

Outcome:

```text
True
```

Command:

```powershell
git diff --check
```

Outcome:

```text
No stdout. Command exited 0.
```

Command:

```powershell
git status --short
```

Outcome:

```text
 M backend_py/main.py
 M backend_py/tests/test_main.py
 M deploy.sh
 M docker-compose.yml
 M docker-entrypoint.sh
 M docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md
 D nginx-valorie.conf
?? nginx-framework.conf
```

### Browser Smoke

Browser smoke was not run and is not claimed. This pass only changed deploy/config files and backend preflight handling; no live Docker/Postgres/frontend/seeded browser-smoke environment was started.

## Migration Placeholder Route/Tool Cleanup Verification - 2026-07-05

### Baseline Working Tree

Command:

```powershell
git status --short
```

Outcome before this pass:

```text
No stdout. Working tree was clean.
```

### Focused Placeholder Inventory

Command:

```powershell
rg -n --hidden -S "MigrationTool|migrate-data|cleanupData|DataCleanupButton|updateFrameworkTenants|/migrate|migration placeholder|data migration|cleanup data|migration tool" frontend/src backend_py docs README.md -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv"
```

Outcome:

```text
Exit 0. Active frontend matches were found in:
frontend/src\App.jsx:16:import MigrationTool from './components/MigrationTool'
frontend/src\App.jsx:66:        <Route path="/migrate" element={<MigrationTool />} />
frontend/src\App.route.test.jsx:39:vi.mock('./components/MigrationTool', () => ({
frontend/src\migrate-data.js:2:  'Legacy client-side migration tooling is isolated for Phase 6 SDK removal.'
frontend/src\components\MigrationTool.jsx:1:function MigrationTool() {
frontend/src\components\MigrationTool.jsx:18:export default MigrationTool
frontend/src\utils\cleanupData.js:4:export async function cleanupData() {
frontend/src\utils\DataCleanupButton.jsx:1:function DataCleanupButton() {
frontend/src\utils\DataCleanupButton.jsx:14:export default DataCleanupButton

The same scan also matched historical migration docs under `docs/migration/phases/**`,
which remain allowlisted audit records. `backend_py/app/services/vectorstore/openai_legacy.py`
matched only the phrase "legacy migration tool" inside provider compatibility code; it
is not a frontend migration placeholder route/tool and was not edited.
```

Candidate classification:

- Deleted obsolete active placeholders: `frontend/src/components/MigrationTool.jsx`, `frontend/src/migrate-data.js`, `frontend/src/utils/cleanupData.js`, `frontend/src/utils/DataCleanupButton.jsx`, and `frontend/src/utils/updateFrameworkTenants.js`.
- Removed active route/import: `frontend/src/App.jsx` `/migrate` route and `MigrationTool` import.
- Removed active-test placeholder mock: `frontend/src/App.route.test.jsx` `MigrationTool` mock.
- Deferred/non-target: tenant/org/invite route shells and `backend_py/app/services/vectorstore/openai_legacy.py` provider compatibility text.

### Post-Edit Placeholder Scan

Command:

```powershell
rg -n --hidden -S "MigrationTool|migrate-data|cleanupData|DataCleanupButton|updateFrameworkTenants|/migrate" frontend/src -g "!frontend/dist"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path frontend\src\migrate-data.js; Test-Path frontend\src\utils\cleanupData.js; Test-Path frontend\src\utils\DataCleanupButton.jsx; Test-Path frontend\src\utils\updateFrameworkTenants.js; Test-Path frontend\src\components\MigrationTool.jsx
```

Outcome:

```text
False
False
False
False
False
```

### Focused Frontend Route Test

Initial sandboxed command:

```powershell
cd frontend
npm test -- App.route.test.jsx
```

Sandboxed outcome:

```text
Failed before tests: esbuild could not read/resolve `frontend/vitest.config.js`
because the sandbox denied reading directory "../../../..".
```

Escalated rerun command:

```powershell
cd frontend
npm test -- App.route.test.jsx
```

Outcome:

```text
1 test file passed, 1 test passed.
Warning: baseline-browser-mapping data is over two months old.
```

### Full Frontend Tests

Command:

```powershell
cd frontend
npm test
```

Outcome:

```text
10 test files passed, 53 tests passed.
Warnings/notices: baseline-browser-mapping data over two months old;
Browserslist/caniuse-lite data 9 months old.
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
Failed before build: esbuild could not read/resolve `frontend/vite.config.js`
because the sandbox denied reading directory "../../../..".
```

Escalated rerun command:

```powershell
cd frontend
npm run build
```

Outcome:

```text
Build passed. Vite transformed 140 modules and produced `dist/index.html`,
`dist/assets/index-DfLzCzBj.css`, and `dist/assets/index-D53k77nA.js`.
Warnings: baseline-browser-mapping data over two months old; browserslist/caniuse-lite
data 9 months old; one chunk larger than 500 kB after minification.
```

### Skipped Checks

- Backend syntax and backend tests: not run because this pass changed only frontend route/test files plus migration docs.
- Browser smoke: not run because this pass only removed inactive frontend placeholder tooling, and the prior Docker/Postgres/seeded-credential blocker remains unresolved in this environment.

### Final Post-Documentation Scans And Whitespace Check

Command:

```powershell
rg -n --hidden -S "MigrationTool|migrate-data|cleanupData|DataCleanupButton|updateFrameworkTenants|/migrate" frontend/src backend_py/app -g "!frontend/dist" -g "!backend_py/.venv"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path frontend\src\migrate-data.js; Test-Path frontend\src\utils\cleanupData.js; Test-Path frontend\src\utils\DataCleanupButton.jsx; Test-Path frontend\src\utils\updateFrameworkTenants.js; Test-Path frontend\src\components\MigrationTool.jsx
```

Outcome:

```text
False
False
False
False
False
```

Command:

```powershell
git diff --check
```

Outcome:

```text
No stdout. Command exited 0.
```

Command:

```powershell
git status --short
```

Outcome:

```text
 M docs/migration/phases/phase-07-domain-legacy-cleanup/checklist.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/phase-report.md
 M docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md
 M frontend/src/App.jsx
 M frontend/src/App.route.test.jsx
 D frontend/src/components/MigrationTool.jsx
 D frontend/src/migrate-data.js
 D frontend/src/utils/DataCleanupButton.jsx
 D frontend/src/utils/cleanupData.js
 D frontend/src/utils/updateFrameworkTenants.js
```

## Tenant/Org/Invite Cleanup Inventory Verification - 2026-07-06

Scope: inventory-only pass. No runtime code deletion, backend/frontend tests, database model edits, Alembic migration edits, auth/session behavior changes, or replacement tenant/org/invite/workspace behavior were performed.

### Baseline Working Tree

Command:

```powershell
git status --short
```

Outcome:

```text
No stdout. Working tree was clean before this inventory pass.
```

### Active Frontend Source Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" frontend/src -g "!**/*.test.*" -g "!frontend/dist"
```

Outcome summary:

```text
15 active frontend source files, 72 total matches.

File counts:
- frontend/src/App.jsx: 9
- frontend/src/components/CreateFramework.jsx: 4
- frontend/src/components/FrameworkCard.jsx: 3
- frontend/src/components/FrameworkEditor.jsx: 5
- frontend/src/components/InviteAccept.jsx: 1
- frontend/src/components/LandingPage.jsx: 2
- frontend/src/contexts/AuthContext.jsx: 4
- frontend/src/components/Login.jsx: 1
- frontend/src/lib/api.js: 1
- frontend/src/components/Navbar.jsx: 19
- frontend/src/components/TenantRoute.jsx: 14
- frontend/src/components/TenantSettings.jsx: 1
- frontend/src/components/UpdateFrameworksButton.jsx: 1
- frontend/src/components/YourFrameworks.jsx: 6
- frontend/src/components/YourOrganization.jsx: 1
```

Interpretation: active frontend cleanup remains. The matches are route shells, route guards, user-state compatibility fields, route-generation helpers, inert org-sharing UI, and isolated org/invite/tenant placeholders.

### Frontend API Split-String Identity-Strip Scan

Command:

```powershell
rg -n --hidden -F "tenant_id" frontend\src\lib\api.js
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n --hidden -F "X-Tenant-ID" frontend\src\lib\api.js
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
rg -n --hidden -S "stripArtefactResourceFields|\['tenant', 'id'\]|\['X', 'Tenant-ID'\]" frontend\src\lib\api.js
```

Outcome:

```text
frontend\src\lib\api.js:180:function stripArtefactResourceFields(artefactData = {}) {
frontend\src\lib\api.js:187:    ['tenant', 'id'].join('_'),
frontend\src\lib\api.js:188:    ['X', 'Tenant-ID'].join('-'),
frontend\src\lib\api.js:236:    const contentJson = stripArtefactResourceFields(artefactData)
```

Interpretation: literal full-string scans missed the `api.js` `tenant_id` and `X-Tenant-ID` handling because the active guard constructs those names from split strings. The inventory now documents this as a security-preserving identity-strip guard that prevents client-supplied identity/header data from being forwarded in artefact payloads; it is preserved for now and assigned only to a focused future frontend API cleanup that keeps equivalent strip coverage.

### UpdateFrameworksButton Import/Render Scan

Command:

```powershell
rg -n --hidden -S "UpdateFrameworksButton|YourFrameworks" frontend\src\components\UpdateFrameworksButton.jsx frontend\src\components\YourFrameworks.jsx frontend\src\App.jsx
```

Outcome:

```text
frontend\src\App.jsx:12:import YourFrameworks from './components/YourFrameworks'
frontend\src\App.jsx:71:              <YourFrameworks />
frontend\src\components\YourFrameworks.jsx:5:import UpdateFrameworksButton from './UpdateFrameworksButton'
frontend\src\components\YourFrameworks.jsx:8:function YourFrameworks() {
frontend\src\components\YourFrameworks.jsx:130:        <UpdateFrameworksButton />
frontend\src\components\YourFrameworks.jsx:313:export default YourFrameworks
frontend\src\components\UpdateFrameworksButton.jsx:1:function UpdateFrameworksButton() {
frontend\src\components\UpdateFrameworksButton.jsx:6:export default UpdateFrameworksButton
```

Interpretation: `UpdateFrameworksButton.jsx` is active source residue because `YourFrameworks.jsx` imports and renders it in the active framework list, even though the component currently returns null. The inventory now assigns it to a focused frontend org placeholder cleanup, not backend tenant/model cleanup.

### Frontend Test Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" frontend/src -g "**/*.test.*" -g "!frontend/dist"
```

Outcome summary:

```text
6 frontend test files, 34 total matches.

File counts:
- frontend/src/lib/api.test.js: 20
- frontend/src/App.route.test.jsx: 6
- frontend/src/components/TenantRoute.test.jsx: 3
- frontend/src/components/FrameworkEditor.test.jsx: 2
- frontend/src/components/FrameworkCard.test.jsx: 1
- frontend/src/components/Login.test.jsx: 2
```

Interpretation: route/component tests need frontend cleanup updates. `frontend/src/lib/api.test.js` also contains intentional negative assertions proving frontend helpers strip client-supplied `tenant_id` and `X-Tenant-ID`; keep equivalent coverage unless rewritten.

### Backend App, Services, Models, And Migrations Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py/app/models.py backend_py/app/db.py backend_py/app/api backend_py/app/services backend_py/alembic -g "!backend_py/.venv"
```

Outcome summary:

```text
1 backend app file, 1 total match:
- backend_py/app/api/vector_sync.py: 1
```

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py/app/models.py backend_py/alembic
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no tenant/org/invite residue was found in the active database model or Alembic migration files. The single backend app match is `include_organization` in `backend_py/app/api/vector_sync.py`, which remains deferred because that route is Phase 9-deferred indexing/RAG plumbing.

### Backend Tenant/Invite Router Absence Scan

Command:

```powershell
rg -n --hidden -S "/api/tenants|tenants/|tenant_members|invites|invite_token|organization_id|org_id" backend_py/app backend_py/alembic backend_py/tests -g "!backend_py/.venv"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no active backend tenant/invite router, tenant-member schema, invite token field, organization id field, or org id field was found.

### Backend Ownership/Auth Preservation Scan

Command:

```powershell
rg -n --hidden -S "Depends\(get_current_user_id\)|Depends\(get_current_user\)|current_user_id|owner|creator_id|user_id" backend_py/app/api/frameworks_crud.py backend_py/app/api/frameworks_public.py backend_py/app/api/artefacts.py backend_py/app/api/admin_users.py backend_py/app/api/users.py
```

Outcome summary:

```text
Matches show current framework, artefact, admin, and user routes derive identity from JWT-backed dependencies and enforce ownership through backend user id / creator_id checks.
```

Interpretation: backend personal-use ownership/auth concepts should be preserved and are not classified as tenant/org/invite residue.

### Backend Test And Obsolete Helper Scan

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py/app/api/vector_sync.py backend_py/tests/test_main.py
```

Outcome summary:

```text
backend_py/tests/test_main.py has 2 matches, both in the negative preflight assertion that `X-Tenant-ID` is not advertised.
backend_py/app/api/vector_sync.py has 1 match: `include_organization`.
```

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" backend_py -g "!backend_py/.venv" -g "!backend_py/app/**" -g "!backend_py/tests/**" -g "!backend_py/alembic/**" -g "!backend_py/scripts/**"
```

Outcome summary:

```text
5 obsolete backend doc/helper files, 26 total matches.

File counts:
- backend_py/README-DIFF.md: 5
- backend_py/test_update.py: 1
- backend_py/test_update_publish.py: 11
- backend_py/test_firebase.py: 7
- backend_py/check_vector_store_attributes.py: 2
```

Interpretation: top-level backend helper scripts and obsolete backend docs remain Round 5 cleanup material, not active backend app behavior.

### Env, Config, And Deploy Scan

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" .env.example frontend/.env.example backend_py/.env.example Dockerfile docker-compose.yml docker-entrypoint.sh deploy.sh nginx-framework.conf
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: active env/config/deploy files are clean for the requested tenant/org/invite terms.

### Current And Historical Docs Scan

Command:

```powershell
rg --count-matches --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" MIGRATION_PHASES.md README.md docs -g "!docs/migration/phases/phase-07-domain-legacy-cleanup/verification.md"
```

Outcome summary:

```text
20 files, 382 total matches.

Current docs/tooling:
- README.md: 1
- docs/skills/migration-reviewer/SKILL.md: 1
- docs/skills/migration-phase-planner/SKILL.md: 1

Canonical/historical records:
- MIGRATION_PHASES.md: 12
- docs/migration/phases/**: 367
```

Interpretation: `README.md` remains Round 5 current-doc cleanup. `MIGRATION_PHASES.md` and `docs/migration/phases/**` are historical/canonical allowlist records. `docs/skills/**` are migration tooling references and are deferred unless a later docs-tooling cleanup updates them.

Command:

```powershell
rg -n --hidden -S "tenant|tenants|organization|organizations|org_id|organization_id|invite|invitation|invite_token|X-Tenant-ID|tenant_id|default_tenant|framework_tenant" MIGRATION_PHASES.md README.md docs/PERSONAL_USE_BOUNDARY.md docs/migration/README.md docs/migration/decisions/ADR-0001-auth-strategy.md
```

Outcome summary:

```text
README.md has one current-doc match: "Legacy Multi-Tenant Compatibility".
MIGRATION_PHASES.md has canonical cleanup-target matches.
docs/PERSONAL_USE_BOUNDARY.md, docs/migration/README.md, and ADR-0001 had no matches for this term set.
```

### Specific Hidden-Identifier Scan

Command:

```powershell
rg -n --hidden -S "default_tenant|framework_tenant|invite_token|organization_id|org_id" . -g "!node_modules" -g "!frontend/node_modules" -g "!frontend/dist" -g "!backend_py/.venv" -g "!.git"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no `default_tenant`, `framework_tenant`, `invite_token`, `organization_id`, or `org_id` residue was found in the scanned workspace.

### Skipped Checks

- Backend tests: not run because this pass changed only migration documentation.
- Frontend tests: not run because this pass changed only migration documentation.
- Browser smoke: not run and not claimed; this was an inventory-only documentation pass.

### Post-Documentation Whitespace Check

Command:

```powershell
git diff --check
```

Outcome:

```text
No stdout. Command exited 0.
```

## Frontend Personal Route Cleanup Verification - 2026-07-06

Scope: frontend personal-route cleanup only. Backend auth/session behavior, backend ownership checks, database models, migrations, README, obsolete backend helper scripts, `UpdateFrameworksButton.jsx`, and the `api.js` split-string identity-strip guard were not changed.

### Active Route Residue Scan

Command:

```powershell
rg -n 'TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept|/:tenantId|/invite/:token|/personal/frameworks|/editor/|getPath\(|tenantShim|getCurrentTenantId' frontend\src
```

Outcome:

```text
frontend\src\components\InviteAccept.jsx:1:function InviteAccept() {
frontend\src\components\InviteAccept.jsx:17:export default InviteAccept
frontend\src\components\TenantRoute.jsx:5: * TenantRoute - Tenant Route Protection Component (Path Mode - Simplified Version)
frontend\src\components\TenantRoute.jsx:11:function TenantRoute({ children }) {
frontend\src\components\TenantRoute.jsx:92:export default TenantRoute
frontend\src\components\YourOrganization.jsx:1:function YourOrganization() {
frontend\src\components\YourOrganization.jsx:18:export default YourOrganization
frontend\src\components\TenantSettings.jsx:1:function TenantSettings() {
frontend\src\components\TenantSettings.jsx:17:export default TenantSettings
frontend\src\components\TenantCreationModal.jsx:1:function TenantCreationModal() {
frontend\src\components\TenantCreationModal.jsx:5:export default TenantCreationModal
```

Interpretation: no active old route paths, route helpers, or active route imports remain. The remaining matches are unmounted placeholder component files deferred to the frontend org/invite placeholder cleanup slice.

Command:

```powershell
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/' frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: active frontend source and tests no longer define or assert the removed tenant/invite/personal-shim route paths.

### Removed Placeholder Import Scan

Command:

```powershell
rg -n "from './components/(TenantRoute|TenantSettings|InviteAccept|YourOrganization)'|from './(TenantRoute|TenantSettings|InviteAccept|YourOrganization)'|<TenantRoute|<TenantSettings|<InviteAccept|<YourOrganization" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: `App.jsx` no longer imports or mounts `TenantRoute`, `TenantSettings`, `InviteAccept`, or `YourOrganization`.

Command:

```powershell
rg -n "getCurrentTenantId" frontend\src -g "!frontend/src/lib/api.js" -g "!frontend/src/lib/api.test.js"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no component or active route-generation code imports the removed legacy route shim. The shim was also removed from `api.js` and `api.test.js`.

### Remaining Tenant/Org/Invite Residue Scan

Command:

```powershell
rg -n 'tenant|Tenant|organization|Organization|invite|Invite|joinedOrganization|tenantId|publishedToOrganization|Publish to Organization|Tenant Settings|My Organization|X-Tenant-ID|tenant_id' frontend\src -g '!frontend/src/components/TenantRoute.jsx' -g '!frontend/src/components/TenantCreationModal.jsx' -g '!frontend/src/components/TenantSettings.jsx' -g '!frontend/src/components/YourOrganization.jsx' -g '!frontend/src/components/InviteAccept.jsx'
```

Outcome summary:

```text
frontend\src\contexts\AuthContext.jsx retains tenantId, joinedOrganization, and updateUserTenant.
frontend\src\lib\api.js retains split-string tenant_id / X-Tenant-ID identity-strip guard lines and publishedToOrganization normalization.
frontend\src\lib\api.test.js retains tenant_id / X-Tenant-ID negative assertions.
frontend\src\components\FrameworkCard.jsx retains organization sharing labels/actions.
frontend\src\components\YourFrameworks.jsx retains organization filters and publishedToOrganization checks.
frontend\src\components\UpdateFrameworksButton.jsx remains as the documented org-field repair placeholder.
```

Interpretation: remaining matches are the previously documented deferrals: frontend auth-state cleanup, frontend org placeholder/sharing cleanup, and focused API identity-strip guard cleanup. They are not active tenant route shells.

### Focused Route/API Tests

Initial sandboxed command:

```powershell
cd frontend
npm test -- src/App.route.test.jsx src/components/Login.test.jsx src/components/FrameworkEditor.test.jsx src/lib/api.test.js
```

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read ../../../.. and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
cd frontend
npm test -- src/App.route.test.jsx src/components/Login.test.jsx src/components/FrameworkEditor.test.jsx src/lib/api.test.js
```

Escalated rerun result:

```text
4 test files passed.
30 tests passed.
Duration 5.16s.
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Lint

Command:

```powershell
cd frontend
npm run lint
```

Result:

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

Exit code: `0`.

### Full Frontend Tests

Initial sandboxed command:

```powershell
cd frontend
npm test
```

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read ../../../.. and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
cd frontend
npm test
```

Escalated rerun result:

```text
9 test files passed.
52 tests passed.
Duration 4.06s.
```

Warnings/output: existing stdout from `PublishModal.test.jsx` and `Login.test.jsx`; existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Build

Initial sandboxed command:

```powershell
cd frontend
npm run build
```

Initial result:

```text
Failed before build compilation: esbuild/Vite could not read ../../../.. and could not resolve frontend\vite.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
cd frontend
npm run build
```

Escalated rerun result:

```text
vite v7.1.9 building for production...
136 modules transformed.
dist/index.html                 0.48 kB | gzip:   0.31 kB
dist/assets/index-DfLzCzBj.css 38.87 kB | gzip:   7.06 kB
dist/assets/index-BZMVfgS5.js  851.64 kB | gzip: 257.11 kB
built in 5.19s
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings; existing chunk larger than 500 kB after minification warning.

### Skipped Checks

- Backend tests: not run because this slice changed only frontend route/navigation/test files and migration docs.
- Browser smoke: not run and not claimed; Docker/Postgres/seeded local environment availability remains the blocker recorded earlier in Phase 6 and Phase 7 docs.

### Post-Documentation Rerun

Commands:

```powershell
rg -n 'TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept|/:tenantId|/invite/:token|/personal/frameworks|/editor/|getPath\(|tenantShim|getCurrentTenantId' frontend\src
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/' frontend\src
git diff --check
```

Results:

```text
The first scan still reports only the unmounted placeholder component files: InviteAccept.jsx, TenantCreationModal.jsx, TenantSettings.jsx, TenantRoute.jsx, and YourOrganization.jsx.
The active old-route path scan returned no stdout; `rg` exited 1.
`git diff --check` returned no stdout and exited 0.
```

## Unmounted Frontend Tenant/Org/Invite Placeholder Cleanup Verification - 2026-07-07

Scope: delete only confirmed-unmounted frontend tenant/org/invite placeholder files. Backend auth/session behavior, database models, migrations, ownership checks, API contracts, `AuthContext.jsx` tenant/org state, `FrameworkCard.jsx`/`YourFrameworks.jsx` organization-sharing UI, `UpdateFrameworksButton.jsx`, and the `api.js` split-string identity-strip guard were not changed.

### Baseline Working Tree

Command:

```powershell
git status --short
```

Outcome:

```text
No stdout. Working tree was clean before this placeholder cleanup slice.
```

### Pre-Delete Placeholder Inventory

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src
```

Outcome:

```text
frontend\src\components\InviteAccept.jsx:1:function InviteAccept() {
frontend\src\components\InviteAccept.jsx:17:export default InviteAccept
frontend\src\components\TenantCreationModal.jsx:1:function TenantCreationModal() {
frontend\src\components\TenantCreationModal.jsx:5:export default TenantCreationModal
frontend\src\components\TenantRoute.jsx:5: * TenantRoute - Tenant Route Protection Component (Path Mode - Simplified Version)
frontend\src\components\TenantRoute.jsx:11:function TenantRoute({ children }) {
frontend\src\components\TenantRoute.jsx:92:export default TenantRoute
frontend\src\components\TenantSettings.jsx:1:function TenantSettings() {
frontend\src\components\TenantSettings.jsx:17:export default TenantSettings
frontend\src\components\YourOrganization.jsx:1:function YourOrganization() {
frontend\src\components\YourOrganization.jsx:18:export default YourOrganization
```

Interpretation: each placeholder name appeared only inside its own component file.

Command:

```powershell
rg -n "from .*TenantRoute|from .*TenantCreationModal|from .*TenantSettings|from .*YourOrganization|from .*InviteAccept|<TenantRoute|<TenantCreationModal|<TenantSettings|<YourOrganization|<InviteAccept" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no active imports or JSX renders remained for the five placeholder components.

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src -g "**/*.test.*"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no frontend test referenced the five placeholder components.

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src -g "!frontend/src/components/TenantRoute.jsx" -g "!frontend/src/components/TenantCreationModal.jsx" -g "!frontend/src/components/TenantSettings.jsx" -g "!frontend/src/components/YourOrganization.jsx" -g "!frontend/src/components/InviteAccept.jsx"
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: excluding the five candidate files left no active source or test references.

Command:

```powershell
Test-Path frontend\src\components\TenantRoute.jsx; Test-Path frontend\src\components\TenantCreationModal.jsx; Test-Path frontend\src\components\TenantSettings.jsx; Test-Path frontend\src\components\YourOrganization.jsx; Test-Path frontend\src\components\InviteAccept.jsx
```

Outcome:

```text
True
True
True
True
True
```

### Deleted Files

- `frontend/src/components/TenantRoute.jsx`
- `frontend/src/components/TenantCreationModal.jsx`
- `frontend/src/components/TenantSettings.jsx`
- `frontend/src/components/YourOrganization.jsx`
- `frontend/src/components/InviteAccept.jsx`

No tests were updated or deleted because no test referenced only these removed placeholders.

### Post-Delete Placeholder Scans

Command:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Command:

```powershell
Test-Path frontend\src\components\TenantRoute.jsx; Test-Path frontend\src\components\TenantCreationModal.jsx; Test-Path frontend\src\components\TenantSettings.jsx; Test-Path frontend\src\components\YourOrganization.jsx; Test-Path frontend\src\components\InviteAccept.jsx
```

Outcome:

```text
False
False
False
False
False
```

### Invite/Tenant Route Residue Scan

Command:

```powershell
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/|Tenant Settings|My Organization|<Invite|<YourOrganization|<TenantSettings|<TenantRoute' frontend\src
```

Outcome:

```text
No stdout. `rg` exited 1.
```

Interpretation: no active tenant or invite route paths, old personal-route shim paths, or deleted placeholder JSX route mounts remain in `frontend/src`.

### Remaining Frontend Tenant/Org Residue Scan

Command:

```powershell
rg -n "tenant|Tenant|organization|Organization|invite|Invite|joinedOrganization|tenantId|publishedToOrganization|Publish to Organization|X-Tenant-ID|tenant_id" frontend\src -g "!**/*.test.*"
```

Outcome:

```text
frontend\src\contexts\AuthContext.jsx:24:    tenantId: existingUser?.tenantId || null,
frontend\src\contexts\AuthContext.jsx:25:    joinedOrganization: existingUser?.joinedOrganization || null,
frontend\src\contexts\AuthContext.jsx:125:  const updateUserTenant = async (tenantId, reload = false) => {
frontend\src\contexts\AuthContext.jsx:132:      tenantId,
frontend\src\contexts\AuthContext.jsx:162:    updateUserTenant,
frontend\src\lib\api.js:177:    ['tenant', 'id'].join('_'),
frontend\src\lib\api.js:178:    ['X', 'Tenant-ID'].join('-'),
frontend\src\lib\api.js:385:    publishedToOrganization: Boolean(framework.publishedToOrganization),
frontend\src\components\FrameworkCard.jsx:25:  const isShared = Boolean(framework.publishedToOrganization)
frontend\src\components\FrameworkCard.jsx:102:    alert('Organization sharing is not available in this migration round.')
frontend\src\components\FrameworkCard.jsx:107:    alert('Organization sharing is not available in this migration round.')
frontend\src\components\FrameworkCard.jsx:389:                <span>Unpublish from Organization</span>
frontend\src\components\FrameworkCard.jsx:396:                <span>Publish to Organization</span>
frontend\src\components\YourFrameworks.jsx:57:        return frameworks.filter(f => !f.isPublic && !f.publishedToOrganization)
frontend\src\components\YourFrameworks.jsx:60:      case 'organization':
frontend\src\components\YourFrameworks.jsx:61:        return frameworks.filter(f => f.publishedToOrganization)
frontend\src\components\YourFrameworks.jsx:162:                      f => !f.isPublic && !f.publishedToOrganization
frontend\src\components\YourFrameworks.jsx:171:                <option value="organization">
frontend\src\components\YourFrameworks.jsx:172:                  Published to Organization (
frontend\src\components\YourFrameworks.jsx:173:                  {frameworks.filter(f => f.publishedToOrganization).length})
frontend\src\components\UpdateFrameworksButton.jsx:2:  // Phase 7 owns the old organization-field repair path.
```

Interpretation: remaining matches are the explicitly deferred frontend auth-state, API identity-strip guard/published-org normalization, organization-sharing UI, organization filters, and `UpdateFrameworksButton.jsx` residue. This slice intentionally did not change them.

### Frontend Lint

Command:

```powershell
npm run lint
```

Working directory: `frontend`

Outcome:

```text
> frontend@0.0.0 lint
> eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0
```

Exit code: `0`.

### Full Frontend Tests

Initial sandboxed command:

```powershell
npm test
```

Working directory: `frontend`

Initial result:

```text
Failed before tests ran: esbuild/Vitest could not read "../../../.." and could not resolve frontend\vitest.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm test
```

Working directory: `frontend`

Escalated rerun result:

```text
9 test files passed.
52 tests passed.
Duration 6.90s.
```

Warnings/output: existing stdout from `PublishModal.test.jsx` and `Login.test.jsx`; existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings.

### Frontend Build

Initial sandboxed command:

```powershell
npm run build
```

Working directory: `frontend`

Initial result:

```text
Failed before build compilation: esbuild/Vite could not read "../../../.." and could not resolve frontend\vite.config.js inside the sandbox.
```

Escalated rerun command:

```powershell
npm run build
```

Working directory: `frontend`

Escalated rerun result:

```text
vite v7.1.9 building for production...
136 modules transformed.
dist/index.html                 0.48 kB | gzip:   0.31 kB
dist/assets/index-DfLzCzBj.css  38.87 kB | gzip:   7.06 kB
dist/assets/index-BZMVfgS5.js   851.64 kB | gzip: 257.11 kB
built in 6.56s
```

Warnings: existing stale `baseline-browser-mapping` and Browserslist/caniuse data warnings; existing chunk larger than 500 kB after minification warning.

### Skipped Checks

- Backend tests: not run because this slice changed only frontend placeholder files and migration docs.
- Browser smoke: not run and not claimed; Docker/Postgres/seeded local environment availability remains the blocker recorded earlier in Phase 6 and Phase 7 docs.

### Post-Documentation Rerun

Commands:

```powershell
rg -n "TenantRoute|TenantCreationModal|TenantSettings|YourOrganization|InviteAccept" frontend\src
rg -n 'path="/:tenantId|path="/invite|/:tenantId|/invite/:token|/personal/frameworks|/editor/|Tenant Settings|My Organization|<Invite|<YourOrganization|<TenantSettings|<TenantRoute' frontend\src
git diff --check
```

Results:

```text
The deleted-component scan returned no stdout; `rg` exited 1.
The active old-route path scan returned no stdout; `rg` exited 1.
`git diff --check` returned no stdout and exited 0.
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
rg -n "valorie|Valorie|expert\.valorie\.ai|tenant|X-Tenant-ID|nginx-valorie" Dockerfile docker-compose.yml docker-entrypoint.sh deploy.sh nginx-framework.conf .env.example backend_py/.env.example backend_py/alembic.ini backend_py/main.py backend_py/app
Test-Path nginx-valorie.conf
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
