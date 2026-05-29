# Phase 01 Checklist - Auth Baseline

- [x] Read Phase 0 documents and ADR-0001
- [x] Upgrade password hashing to Argon2id
- [x] Keep legacy SHA-256+salt hash compatibility verification
- [x] Automatically rehash legacy hashes after successful login
- [x] Disable public registration by default
- [x] Add ALLOWED_EMAILS allowlist check
- [x] Add administrator seed script
- [x] Block user_id from Body / Query / Form on private endpoints
- [x] Add or confirm get_current_user shared dependency
- [x] Reserve or document refresh token / httpOnly cookie strategy
- [x] Add Phase 1 verification commands
- [x] Do not touch Phase 2+ content
