# Phase 03 Verification - DeepSeek V4

## Current Reviewer Transcription - 2026-07-13

- `review_id`: `MR-2EC4192-20260713-01`
- `verdict`: `pending`
- `reviewed_commit`: `e902205f198540cc7a3abcc6b802ef285f45554f`, as represented at reviewed HEAD `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`
- `accepted_commit`: absent
- Missing evidence: authorized real `DeepSeekProvider.tool_call()` smoke against the official endpoint.
- `owners`: LLM Provider Owner for readiness; Migration Verification Owner for execution.
- `triggers`: authorized key; reachable official endpoint; non-dev/non-dry-run configuration; reviewed candidate; rerun after base URL, model, thinking policy, SDK/default transport, or provider call-path changes.
- This transcription did not run the real DeepSeek smoke and does not claim it passed.

## Governance Reconciliation - 2026-07-10

- Current ledger verdict: `pending`.
- Provider-level response preservation evidence is Phase 3 evidence.
- Real DeepSeek API smoke remains `not run`; no pass is claimed and this corrective remediation did not use an API key.
- Phase 8 owns a future continuing active-run replay contract: once a thinking-mode assistant tool-call message exists, every applicable subsequent provider request within that active run, including requests triggered by later user interactions, must replay it with the full required `reasoning_content`; every replay serialization must keep assistant `content` non-null (a missing raw value becomes `""` only at that boundary); regressions must span beyond the immediately following request; and full reasoning remains short-lived active-run state that must not enter long-term logs. Phase 3 preserves the raw provider response and does not implement or claim this future behavior.

### Real-smoke evidence template (not run)

LLM Provider Owner is responsible for readiness; when an authorized environment
becomes available, Migration Verification Owner executes the smoke and records:

- named reviewer/verifier and RFC 3339 date;
- full reviewed commit;
- `LLM_PROVIDER=deepseek`, official endpoint host `api.deepseek.com` over HTTPS, selected model/thinking mode, `ENV`/`dry_run=false`, and legacy path disabled;
- the opt-in `scripts/smoke_deepseek_thinking_tool_call.py` command, which calls
  `DeepSeekProvider.tool_call()` with thinking enabled and a supplied
  `tool_choice="auto"` that the provider must omit from the outbound request;
- sanitized provider response/tool-call identifiers and, when the SDK exposes it, the separately labelled SDK request identifier;
- status/result and error summary without API key, full prompt, or full reasoning content.

Trigger: an authorized key, reachable official endpoint, non-dev/non-dry-run
configuration, and a reviewed candidate; rerun before Phase 3 final re-review
and after a change to DeepSeek base URL, model, thinking policy, SDK/default
transport, or provider call path.

## Syntax Check

Command:

```powershell
python -m py_compile backend_py\app\services\llm\deepseek.py backend_py\app\services\llm\factory.py backend_py\app\services\llm\model_policy.py backend_py\app\api\generation.py backend_py\app\api\frameworks_shared.py backend_py\diagnose_env.py
```

Result: passed with exit code `0`.

## Backend Pytest

Command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest -q
```

Result after the Phase 1-3 review fixes: `55 passed`, with 3 existing Pydantic deprecation warnings.

## Reasoning Content Scope

Phase 3 verification covers provider-level preservation only. The regression in `backend_py/tests/test_deepseek_provider.py` confirms `DeepSeekProvider.tool_call()` returns raw `content` (including `None`), `reasoning_content`, `tool_calls`, and exposed response/request identifiers from one response.

DeepSeek V4 thinking-mode requests omit `tool_choice`, including when a caller
supplies it explicitly or through `extra_body`; unrelated `extra_body` fields
and the required thinking block survive. Non-thinking requests retain the prior
forwarding behavior. The focused regressions cover these branches and preserve
the existing response-field assertions. This follows DeepSeek's official
[V4 agent integration compatibility guidance](https://api-docs.deepseek.com/quick_start/agent_integrations/oh_my_pi/),
which states that thinking mode rejects `tool_choice`.

Agent-loop replay was not implemented or tested in Phase 3 because it is Phase 8 scope. Future Phase 8 active-run regressions must span beyond the immediately following request and prove that every applicable subsequent provider request within that active run, including requests triggered by later user interactions, replays the thinking-mode assistant tool-call message with its full required `reasoning_content`. They must also prove that assistant `content` is non-null at every replay serialization (a missing raw value becomes `""` only at that boundary). Full reasoning remains short-lived active-run state and must not be written to long-term logs. No Phase 3 verification claims these future behaviors are complete, and the raw provider response remains unchanged.

Current corrective-provider verification (2026-07-13):

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_material_owner_authorization.py tests\test_deepseek_provider.py tests\test_provider_abstractions.py -q
```

Result: `50 passed`, with existing deprecation warnings. The full backend suite passed `128` tests. The real DeepSeek smoke remained explicitly `not run`.

Transcription note (review event `MR-2EC4192-20260713-01`): the `50` focused / `128` backend results above belong to an earlier corrective run and remain unchanged as historical evidence. At the exact reviewed HEAD `2ec41926ab6b9910e7b05f60839ba24c8b5cb236`, the Reviewer recorded focused backend `52 passed` and complete backend `130 passed`. This documentation transcription did not rerun either test command and does not replace the earlier result.

Latest review-fix targeted command:

```powershell
cd backend_py
.\.venv\Scripts\python.exe -m pytest tests\test_auth_hardening.py tests\test_deepseek_provider.py tests\test_provider_abstractions.py -q
```

Result on 2026-05-31:

```text
37 passed, 3 warnings in 4.26s
```

Warnings are the existing Pydantic v2 deprecation warnings in `backend_py/app/api/users.py`.

## Frontend Tests

Command:

```powershell
cd frontend
npm test -- --configLoader runner
```

Result: `13 passed`.

Note: Vitest printed a stale `baseline-browser-mapping` data warning.

## Real DeepSeek API Smoke

The smoke path intentionally exercises `DeepSeekProvider.tool_call()`; a
`generate-from-text` or `generate_json()` result is not evidence for this
tool-call contract. It is opt-in because it sends a real external API request:

```powershell
cd backend_py
$env:RUN_REAL_DEEPSEEK_TOOL_CALL_SMOKE='true'
$env:DEEPSEEK_API_KEY='<authorized-key>'
.\.venv\Scripts\python.exe scripts\smoke_deepseek_thinking_tool_call.py
```

Before provider construction, the script calls `urllib.request.getproxies()` and
rejects any non-empty `http`, `https`, or `all` entry without printing its value.
Those are the entries used by the default httpx/OpenAI transport, including
environment and Windows/macOS system sources when returned. Before any provider
request, it also rejects non-HTTPS endpoints and any host other than
`api.deepseek.com`, so localhost and mocks cannot qualify. It passes
`reasoning=True` and `tool_choice="auto"`, requires at least one returned tool
call and preserved `reasoning_content`, and prints only the official host,
selected model, sanitized provider response/tool-call identifiers, an optional
separately labelled SDK request identifier, reasoning presence, and tool-call
count. A tool-call ID is never labelled as an HTTP request ID. Record a pass only
with an authorized key and retained, sanitized evidence.

Command status:

```powershell
if ($env:DEEPSEEK_API_KEY) { 'DEEPSEEK_API_KEY=SET' } else { 'DEEPSEEK_API_KEY=NOT SET' }
```

Result:

```text
DEEPSEEK_API_KEY=NOT SET
```

Result: not run. The execution environment did not provide `DEEPSEEK_API_KEY`, so this verification does not claim a real DeepSeek API smoke passed.

## China Deploy Note

`docs/CN_DEPLOY.md` now records the DeepSeek deployment boundary: `DEEPSEEK_BASE_URL=https://api.deepseek.com`, no `/v1` suffix, and no committed API key.

## Frontend Build

Command:

```powershell
cd frontend
npm run build -- --configLoader runner
```

Result: build passed.

Notes: Vite printed existing stale browser-data warnings and a chunk-size warning for the current frontend bundle.

## Frontend Preview Smoke

Command:

```powershell
cd frontend
npm run preview -- --host 127.0.0.1 --configLoader runner
```

Smoke command:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:4173/ -TimeoutSec 10
```

Result: preview served the built app and returned HTTP `200 OK`.

## Legacy GCP Endpoint Scan

Command:

```powershell
rg -n "34\.87\.13\.228" backend_py frontend docker-compose.yml docker-entrypoint.sh .env.example backend_py\.env.example
```

Result: no matches. `rg` exited `1`, which means no matching text was found in the checked runtime paths.

## API Direct OpenAI/Legacy LLM Scan

Command:

```powershell
rg -n "from openai import OpenAI|openai\.OpenAI\(|client\.chat|call_openai_framework|llm_global|resolve_api_settings|gpt-4o" backend_py\app\api
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

## Frontend/API Legacy Model Scan

Command:

```powershell
rg -n "gpt-4o" frontend\src backend_py\app\api
```

Result: no matches. `rg` exited `1`, which means no matching text was found.

## Allowed Vendor SDK Scan

Command:

```powershell
rg -n "from openai import OpenAI" backend_py\app\services backend_py\llm_global.py backend_py\llm_local.py
```

Result: matches only in provider implementation files:

```text
backend_py\app\services\llm\openai_legacy.py
backend_py\app\services\llm\deepseek.py
backend_py\app\services\vectorstore\openai_legacy.py
```

Interpretation: vendor SDK construction remains isolated to provider implementations.

## Legacy Local/Ollama Scan

Command:

```powershell
rg -n "LLM_TYPE|LOCAL_LLM_URL|LOCAL_LLM_API_KEY|34\.87\.13\.228|127\.0\.0\.1:11434" backend_py\app backend_py\llm_local.py backend_py\diagnose_env.py docker-compose.yml docker-entrypoint.sh .env.example backend_py\.env.example
```

Result: matches only in `backend_py\llm_local.py` comments/code for `LLM_TYPE` and `OLLAMA_BASE_URL`. There were no matches for the old GCP IP, `LOCAL_LLM_URL`, `LOCAL_LLM_API_KEY`, or `127.0.0.1:11434` in the checked runtime paths.

## API Legacy Local Call Sites

Command:

```powershell
rg -n "process_with_local_llm\(" backend_py\app\api
```

Result: remaining call sites are explicit local/legacy branches:

```text
backend_py\app\api\generation.py:209
backend_py\app\api\generation.py:448
backend_py\app\api\generation.py:556
backend_py\app\api\frameworks_shared.py:511
backend_py\app\api\ai_ops.py:35
```

Interpretation: `process_with_local_llm()` calls `_require_legacy_llm_enabled()` before importing `llm_local`, so these branches return `503` unless `ENABLE_LEGACY_LLM=true`.

## Residual Legacy Inventory

Reviewed residual Firebase/OpenAI/GCP mentions outside the Phase 3 core runtime. They remain in old frontend Firebase code, old docs, Dockerfile Firebase build args, and top-level legacy helper scripts. These are already assigned to Phase 6/7 in `MIGRATION_PHASES.md` and are not imported by `backend_py/app/api` provider paths.
