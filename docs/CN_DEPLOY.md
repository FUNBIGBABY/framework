# China Deployment Notes

## DeepSeek

- Set `LLM_PROVIDER=deepseek`.
- Set `DEEPSEEK_BASE_URL=https://api.deepseek.com`.
- Do not append `/v1`; the provider adds the OpenAI-compatible path through the SDK.
- Set `DEEPSEEK_API_KEY` in the deployment environment or secret manager. Do not commit it.

## Smoke Status

Real DeepSeek API smoke was not run during the Phase 1-3 review fix because `DEEPSEEK_API_KEY` was not present in the verification environment.

When a key is available, run a minimal provider smoke from the backend environment and record the exact command/result in `docs/migration/phases/phase-03-deepseek-v4/verification.md`.
