# Phase 00 Checklist - Security & Auth Decision

- [x] Delete Firebase admin SDK JSON private key from the working tree.
- [x] Update `.gitignore` with secret and key-file rules.
- [x] Move JWT signing secret to `JWT_SECRET_KEY`.
- [x] Remove LLM API key fallback from source.
- [x] Create `.env.example` with required placeholder variables.
- [x] Create `docs/PERSONAL_USE_BOUNDARY.md`.
- [x] Create `docs/migration/decisions/ADR-0001-auth-strategy.md`.
- [x] Run secret and hardcode grep checks.
- [x] Disable legacy GCP/Ollama LLM defaults before Phase 3.
- [x] Remove old Cloud LLM health check from Docker entrypoint.
- [x] Verify `llm_local.LLMClient()` fails fast unless `ENABLE_LEGACY_LLM=true`.
- [x] Record manual action: customer must revoke the exposed GCP key.
- [x] Record whether git history should be rebuilt.
