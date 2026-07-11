# Phase 03 Checklist - DeepSeek V4

## Governance Reconciliation - 2026-07-10

- Current ledger verdict: `pending`.
- Real DeepSeek smoke remains `not run`; this docs-only repair does not call the DeepSeek API.
- Phase 3 owns provider-level preservation of `reasoning_content` and `tool_calls` from one response.
- Active-run next-round `reasoning_content` carry-back is the formal Phase 8 implementation/verification responsibility. It is not a Phase 3 completion claim and is not a prerequisite that must already be implemented before Phase 8 planning.
- LLM Provider Owner owns readiness; Migration Verification Owner runs the real smoke when an authorized API key, reachable endpoint, non-dev/non-dry-run config, and reviewed candidate are available.

- [x] Keep `LLM_PROVIDER=deepseek` as the default provider.
- [x] Configure DeepSeek with `DEEPSEEK_BASE_URL=https://api.deepseek.com` and reject a `/v1` suffix.
- [x] Implement real `DeepSeekProvider.chat()`, `stream()`, `tool_call()`, and `generate_json()`.
- [x] Use `response_format={"type":"json_object"}` only for `generate_json()`.
- [x] Send `extra_body.thinking.type=disabled` for fast mode by default.
- [x] Route explicit reasoning/deep mode to `deepseek-v4-pro` with thinking enabled.
- [x] Preserve `reasoning_content` and tool calls from a single DeepSeek tool-call response.
- [x] Assign next-round Agent-loop `reasoning_content` carry-back to Phase 8 implementation/verification, because Phase 3 does not implement the Agent loop; do not use it as a circular pre-Phase-8 gate.
- [x] Remove frontend/API hard-coded `gpt-4o` defaults.
- [x] Add the frontend Fast/Deep mode control and pass `reasoning=true` to generation APIs only for Deep mode.
- [x] Keep legacy local/Ollama metadata extraction behind `ENABLE_LEGACY_LLM=true`.
- [x] Replace the old GCP Cloud LLM environment diagnostic with a DeepSeek/provider diagnostic.
- [x] Keep OpenAI LLM and OpenAI Vector Store as explicit legacy providers only, not default runtime paths.
- [x] Record Phase 1-3 residual legacy paths and downstream deferrals.
- [x] Update Phase 2 docs so `DeepSeekProvider` is no longer described as a current stub.
- [x] Update root `README.md` to point to the canonical migration docs and label OpenAI/Firebase descriptions as legacy compatibility.
- [x] Run backend pytest, frontend tests, frontend build, and legacy path scans.
- [ ] Run real DeepSeek API smoke with `DEEPSEEK_API_KEY` (not run in this environment; key unavailable).

## Explicit Deferrals

- Frontend Firebase and tenant-era `user_id` compatibility remain deferred to Phase 6/7.
- Top-level legacy helper scripts such as `backend_py/test_cloud_llm.py`, `test_vec_base.py`, and `README-DIFF.md` remain scheduled for Phase 7 deletion or script-folder quarantine.
- `PgVectorProvider`, embedding providers, and object store providers remain Phase 2 stubs until Phase 4/9/12.
- Agent-loop carry-back of short-lived `reasoning_content` into the next tool-call request belongs to Phase 8 implementation/verification. Phase 3 only preserves provider response fields and does not claim a carry-back regression; the missing Phase 8 behavior is not a prerequisite that Phase 3 must implement before Phase 8 planning.
