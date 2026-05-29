# Migration README

This directory records the migration from the legacy customer project to a personal AI Agent project.

Each Phase must have an independent folder. Each Phase folder must contain at least:

- `phase-report.md`
- `checklist.md`
- `verification.md`

When a later AI Agent takes over development, it should read these files first:

1. `PROJECT_AUDIT_AND_MIGRATION_PLAN.md`
2. `MIGRATION_PHASES.md`
3. `docs/migration/README.md`
4. The current Phase `phase-report.md` and `verification.md`

Phase 0 locks the Auth strategy to option A: self-hosted backend JWT, allowlist, and no public registration. Firebase Auth and Firebase ID Token are not part of the new project route.

