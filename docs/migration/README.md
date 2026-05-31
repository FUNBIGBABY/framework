# Migration README

This directory records the migration from the legacy customer project to a personal AI Agent project.

Each Phase must have an independent folder. Each Phase folder must contain at least:

- `phase-report.md`
- `checklist.md`
- `verification.md`

When a later AI Agent takes over development, it should read these files first:

1. `MIGRATION_PHASES.md`
2. `docs/migration/README.md`
3. `docs/migration/decisions/*.md`
4. The current Phase `checklist.md`, `phase-report.md`, and `verification.md`

Archived audit notes may exist under `docs/`, but they are reference material only. `MIGRATION_PHASES.md` is the canonical migration plan.

Phase 0 locks the Auth strategy to option A: self-hosted backend JWT, allowlist, and no public registration. Firebase Auth and Firebase ID Token are not part of the new project route.

User creation for the migration route remains script/admin controlled: use `backend_py/scripts/seed_admin.py` for the current administrator account, and add future users through admin-only backend user management when that exists. Public frontend signup is disabled.
