# Phase 03 Report - DeepSeek V4

## Governance Reconciliation - 2026-07-10

The historical implementation and offline/provider test evidence below are retained. They do not establish final reviewer acceptance. The current ledger verdict is `pending` because the real DeepSeek smoke is still `not run`. Provider response preservation belongs to Phase 3. Phase 8 owns a future continuing active-run replay contract: every applicable subsequent provider request within that active run, including requests triggered by later user interactions, must retain the full required `reasoning_content` on the thinking-mode assistant tool-call message; every replay serialization must keep assistant `content` non-null; regressions must span beyond the immediately following request; and full reasoning must not enter long-term logs. Phase 3 does not implement or claim that behavior, and it is not a pre-Phase-8 implementation condition.

## Scope

Phase 3 switches the default LLM path from legacy OpenAI/GCP/Ollama assumptions to the DeepSeek provider created in Phase 2. It does not implement pgvector, RAG, Agent, LLMWiki, Postgres migration, or the frontend Firebase removal phases.

## DeepSeek Provider

- `backend_py/app/services/llm/deepseek.py` now contains a real OpenAI-compatible DeepSeek bridge.
- `DEEPSEEK_BASE_URL` defaults to `https://api.deepseek.com`; provider construction rejects values ending in `/v1`.
- `DEEPSEEK_MODEL_DEFAULT` defaults to `deepseek-v4-flash`.
- `DEEPSEEK_MODEL_REASONING` defaults to `deepseek-v4-pro`.
- `DEEPSEEK_THINKING_MODE=false` keeps fast mode non-thinking by default.
- `generate_json()` sends JSON response format; normal `chat()`, `stream()`, and `tool_call()` do not.
- Deep mode passes `reasoning=True`, enables thinking, selects the reasoning model, and strips sampling controls that are ineffective while thinking is enabled.
- Thinking mode omits a supplied `tool_choice`, including one placed in
  `extra_body`, which DeepSeek V4 rejects for tool calls; unrelated
  `extra_body` fields survive and non-thinking mode keeps prior behavior.
- `tool_call()` returns the raw `content` (including `None`), `reasoning_content`, and `tool_calls` from a single provider response, plus provider/SDK identifiers when exposed.
- `backend_py/scripts/smoke_deepseek_thinking_tool_call.py` is an opt-in real
  provider smoke that directly calls `tool_call()`, accepts only the official
  `https://api.deepseek.com` endpoint and, before provider construction, rejects
  any non-empty `http`, `https`, or `all` proxy entry returned by
  `urllib.request.getproxies()`. Those are the proxy entries used by the default
  httpx/OpenAI transport, including environment and Windows/macOS system sources
  when returned; proxy values are never reported. The smoke reports only
  sanitized host, model, response/request or tool-call identifiers, reasoning
  presence, and tool count. It has not been run against the real API in this
  environment.
- Phase 3 does not implement Agent-loop replay. In future Phase 8 behavior, once a thinking-mode assistant tool-call message exists, every applicable subsequent provider request within that active run, including requests triggered by later user interactions, must replay that message with its full required `reasoning_content`. At every replay serialization, assistant `content` must be non-null (normalize a missing raw value to `""` only at that boundary), and regressions must span beyond the immediately following request. Full reasoning remains short-lived active-run state and must stay out of long-term logs. The provider's raw single-response `content` behavior remains unchanged.

## Generation Path

- `process_with_global_llm()` invokes `get_llm_provider().generate_json()` and sanitizes legacy OpenAI model names before provider calls.
- Text, single-file, and multi-file generation accept a `reasoning` flag.
- The frontend `CreateFramework.jsx` now exposes a compact Fast/Deep mode control.
- Fast mode keeps `reasoning=false`; Deep mode sends `reasoning=true` to the backend.
- `regenerate`, `ai-merge`, and `ai-fill` already route higher-difficulty work through provider calls with `reasoning=True`.

## Legacy Isolation

- Core API modules under `backend_py/app/api` no longer construct OpenAI clients or call `llm_global`.
- `OpenAILegacyProvider` remains available only when `LLM_PROVIDER=openai_legacy` or `openai` is explicitly selected.
- `OpenAIVectorStoreLegacyProvider` remains disabled by default through `OPENAI_VECTOR_STORE_ENABLED=false`.
- `llm_local.py` still exists for legacy metadata extraction, but every API entry point reaches it only through `process_with_local_llm()`, which fails unless `ENABLE_LEGACY_LLM=true`.
- `llm_global.py` still has legacy function names for CLI compatibility, but API routes do not import or call it.
- `backend_py/diagnose_env.py` was rewritten to diagnose the DeepSeek/provider setup and no longer points to the old GCP Cloud LLM endpoint.

## Phase 1-3 Review

- Phase 1/1.1 auth guardrails remain covered by backend tests. High-cost generation, export, AI ops, and vector sync routes still require JWT dependencies added in prior phases.
- Phase 2 provider boundaries remain intact: business API code calls local provider abstractions, not vendor SDK clients.
- Phase 3 DeepSeek wiring is complete for the current framework generation surface.
- Real DeepSeek API smoke was not run in this environment because `DEEPSEEK_API_KEY` was not set; no real API-call pass is claimed.
- Remaining Firebase, tenant, old deploy documentation, and top-level legacy test-script cleanup are intentionally downstream Phase 6/7 work, not Phase 3 blockers.
- Root `README.md` now points readers to `MIGRATION_PHASES.md` and `docs/migration/README.md` as the canonical execution entry, and labels OpenAI/Firebase descriptions as legacy compatibility or Phase 6/7 cleanup.
- The continuing full-reasoning/non-null-content replay contract and its multi-request regressions are intentionally downstream Phase 8 work, not a Phase 3 completion or implementation claim; full reasoning remains short-lived active-run state and must not be written to long-term logs.

## Changed Files

- `backend_py/app/services/llm/deepseek.py`
- `backend_py/app/api/frameworks_shared.py`
- `backend_py/app/api/generation.py`
- `backend_py/tests/test_deepseek_provider.py`
- `backend_py/tests/test_provider_abstractions.py`
- `backend_py/scripts/smoke_deepseek_thinking_tool_call.py`
- `frontend/src/lib/api.js`
- `frontend/src/components/CreateFramework.jsx`
- `backend_py/diagnose_env.py`
- `.env.example`
- `backend_py/.env.example`
- `docker-compose.yml`
- `docs/migration/phases/phase-02-provider-abstraction/*`
- `docs/migration/phases/phase-03-deepseek-v4/*`
- `docs/CN_DEPLOY.md`
- `README.md`
- `docs/migration/README.md`

## Known Residuals

- `backend_py/llm_local.py` still contains `LLM_TYPE` and Ollama compatibility code behind `ENABLE_LEGACY_LLM=true`.
- Standalone legacy helper scripts and old docs still mention Firebase/OpenAI/GCP. `MIGRATION_PHASES.md` Phase 7 already says these should be deleted or moved into scripts after the frontend/backend Firebase removal work lands. Root `README.md` has been corrected and is no longer a legacy primary entry.
- Frontend Firebase Auth and Firestore data persistence are not removed in this phase.
- Real DeepSeek API smoke remains pending until `DEEPSEEK_API_KEY` is available in the verification environment.
- Agent-loop replay remains deferred to Phase 8. Current tests verify raw provider response preservation only; they do not claim full `reasoning_content` replay across every applicable later provider request, non-null assistant `content` at each replay serialization, the required beyond-first-replay regression coverage, or long-term-log handling.
- The build still emits size and stale browser-data warnings; these are pre-existing frontend maintenance items, not Phase 3 provider blockers.

## Handoff

- Phase 4 can proceed with Postgres/pgvector without changing the LLM provider surface.
- Phase 5 should replace legacy vector sync with `EmbeddingProvider` plus `VectorStoreProvider`.
- Phase 6/7 should remove Firebase, tenant-era plumbing, old docs, and top-level legacy scripts.
- Phase 8 can use `LLMProvider.stream()` and `LLMProvider.tool_call()` for Agent SSE/tool loops, but must implement and regression-test the future continuing replay boundary described above across more than the first subsequent request, without changing Phase 3's raw provider-response behavior or persisting full reasoning in long-term logs.
