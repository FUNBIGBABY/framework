# Phase 03 Verification - DeepSeek V4

## Governance Reconciliation - 2026-07-10

- Current ledger verdict: `pending`.
- Provider-level response preservation evidence is Phase 3 evidence.
- Real DeepSeek API smoke remains `not run`; no pass is claimed and this docs-only repair did not use an API key.
- Active-run next-round `reasoning_content` carry-back is owned and verified by Phase 8. It is not a Phase 3 acceptance item that must be implemented before Phase 8 planning.

### Real-smoke evidence template (not run)

When an authorized environment becomes available, Migration Verification Owner records:

- named reviewer/verifier and RFC 3339 date;
- full reviewed commit;
- `LLM_PROVIDER=deepseek`, sanitized base URL, selected model/thinking mode, `ENV`/`dry_run=false`, and legacy path disabled;
- the authenticated `/api/frameworks/generate-from-text` request surface used;
- non-mock proof and a sanitized request/trace identifier;
- status/result and error summary without API key, full prompt, or full reasoning content.

Trigger: before Phase 3 final re-review and after a change to DeepSeek base URL, model, thinking policy, SDK, or provider call path.

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

Phase 3 verification covers provider-level preservation only. The regression in `backend_py/tests/test_deepseek_provider.py` confirms `DeepSeekProvider.tool_call()` returns `reasoning_content` and `tool_calls` from one response.

Next-round carry-back of short-lived `reasoning_content` into a subsequent Agent-loop request was not implemented or tested in Phase 3 because the Agent loop is Phase 8 scope. No Phase 3 verification claims that carry-back is complete.

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
