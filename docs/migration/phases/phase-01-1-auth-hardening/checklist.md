# Phase 01.1 Checklist - Auth Hardening

- [x] Require JWT on framework export endpoints
- [x] Require JWT on regenerate / ai-merge / ai-fill endpoints
- [x] Require JWT on legacy vector sync / push endpoints
- [x] Require JWT on email and username availability checks
- [x] Make seed_admin fail fast on existing-user password mismatch
- [x] Add explicit seed admin password reset env
- [x] Update stale password hash comment
- [x] Clean stale no-auth docstrings in framework AI endpoints
- [x] Add minimal unauthenticated endpoint integration tests
- [x] Record frontend Firebase user_id compatibility debt for Phase 6
- [x] Require JWT on private materials upload/read/ingest endpoints while leaving `/materials/ping` public
- [x] Bridge frontend login to backend `/api/users/login` and save the returned JWT for Bearer requests
- [x] Route direct protected frontend framework API calls through the shared backend-JWT Bearer helper
- [x] Allow backend-JWT-only framework list sessions by making Firebase `user_id` query compatibility optional
- [x] Disable public frontend signup route/link and remove Firebase public signup as a new-project entry
- [x] Keep refresh/httpOnly cookie strategy marked as Phase 6 compatibility debt, not complete
- [x] Keep Phase 2+ work untouched
- [x] Record verification commands and results
