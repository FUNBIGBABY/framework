# Phase 03 Checklist - DeepSeek V4

## Governance Reconciliation - 2026-07-10

- Current ledger verdict: `pending`.
- Real DeepSeek smoke remains `not run`; this corrective remediation does not call the DeepSeek API.
- Phase 3 owns provider-level preservation of `reasoning_content` and `tool_calls` from one response.
- Phase 8 owns a future active-run replay contract: once a thinking-mode assistant tool-call message exists, every applicable subsequent provider request within that active run, including requests triggered by later user interactions, must replay that message with its full provider-required `reasoning_content`. At every replay serialization, assistant `content` must be non-null (normalize a missing raw value to `""` only at that boundary). Phase 8 regressions must span beyond the immediately following request. Full reasoning remains short-lived active-run state and must not enter long-term logs. Phase 3 preserves the raw single-response fields, including a missing `content`, and does not implement or claim this future behavior; the handoff is not a pre-Phase-8 implementation prerequisite.
- LLM Provider Owner owns readiness; Migration Verification Owner runs the real smoke when an authorized API key, reachable endpoint, non-dev/non-dry-run config, and reviewed candidate are available.

- [x] Keep `LLM_PROVIDER=deepseek` as the default provider.
- [x] Configure DeepSeek with `DEEPSEEK_BASE_URL=https://api.deepseek.com` and reject a `/v1` suffix.
- [x] Implement real `DeepSeekProvider.chat()`, `stream()`, `tool_call()`, and `generate_json()`.
- [x] Use `response_format={"type":"json_object"}` only for `generate_json()`.
- [x] Send `extra_body.thinking.type=disabled` for fast mode by default.
- [x] Route explicit reasoning/deep mode to `deepseek-v4-pro` with thinking enabled.
- [x] Omit caller-supplied `tool_choice` in thinking mode from both the explicit
  argument and `extra_body`, while preserving unrelated `extra_body` fields and
  forwarding in non-thinking mode.
- [x] Preserve `reasoning_content` and tool calls from a single DeepSeek tool-call response.
- [x] Add an opt-in real-provider smoke path that directly exercises
  `DeepSeekProvider.tool_call()`, rejects non-official/non-HTTPS endpoints, and
  rejects, before provider construction, any non-empty `http`, `https`, or `all`
  proxy entry returned by `urllib.request.getproxies()` without emitting its
  value, while otherwise emitting only sanitized provenance;
  do not use generation or JSON calls as proof.
- [x] Assign the future full-reasoning/non-null-content active-run replay contract and multi-request regressions to Phase 8 implementation/verification, because Phase 3 does not implement the Agent loop; do not use it as a circular pre-Phase-8 gate or claim it is already implemented.
- [x] Remove frontend/API hard-coded `gpt-4o` defaults.
- [x] Add the frontend Fast/Deep mode control and pass `reasoning=true` to generation APIs only for Deep mode.
- [x] Keep legacy local/Ollama metadata extraction behind `ENABLE_LEGACY_LLM=true`.
- [x] Replace the old GCP Cloud LLM environment diagnostic with a DeepSeek/provider diagnostic.
- [x] Keep OpenAI LLM and OpenAI Vector Store as explicit legacy providers only, not default runtime paths.
- [x] Record Phase 1-3 residual legacy paths and downstream deferrals.
- [x] Update Phase 2 docs so `DeepSeekProvider` is no longer described as a current stub.
- [x] Update root `README.md` to point to the canonical migration docs and label OpenAI/Firebase descriptions as legacy compatibility.
- [x] Run backend pytest, frontend tests, frontend build, and legacy path scans.
- [ ] Run the real DeepSeek thinking-mode `tool_call()` smoke with an authorized
  `DEEPSEEK_API_KEY` (not run in this environment; key unavailable).

## Explicit Deferrals

- Frontend Firebase and tenant-era `user_id` compatibility remain deferred to Phase 6/7.
- Top-level legacy helper scripts such as `backend_py/test_cloud_llm.py`, `test_vec_base.py`, and `README-DIFF.md` remain scheduled for Phase 7 deletion or script-folder quarantine.
- `PgVectorProvider`, embedding providers, and object store providers remain Phase 2 stubs until Phase 4/9/12.
- Agent-loop replay belongs to future Phase 8 implementation/verification. Once a thinking-mode assistant tool-call message exists, every applicable subsequent provider request within that active run, including requests triggered by later user interactions, must replay that message with its full required `reasoning_content`; at every replay serialization, assistant `content` must be non-null (normalize a missing raw value to `""` only at that boundary). Regressions must span beyond the immediately following request. Full reasoning remains short-lived active-run state and must not enter long-term logs. Phase 3 only preserves raw provider response fields and does not implement or claim these replay behaviors; they are not prerequisites that Phase 3 must implement before Phase 8 planning.
