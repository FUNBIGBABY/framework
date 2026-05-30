# Phase 02 Report - Provider Abstraction

## Scope

Phase 2 introduces backend Provider interfaces so future business code can depend on local abstractions instead of external SDK clients. This phase does not connect real DeepSeek, pgvector, DashScope, OSS, MinIO, S3, Agent, RAG, LLMWiki, or frontend Firebase migration work.

## Provider Abstractions Added

- `backend_py/app/services/llm/`
  - `LLMProvider` defines `chat`, `stream`, `tool_call`, and `generate_json`.
  - `DeepSeekProvider` is the default factory target and is a Phase 2 stub.
  - `OpenAILegacyProvider` is retained only for compatibility and is not default.
- `backend_py/app/services/vectorstore/`
  - `VectorStoreProvider` defines `upsert_vectors`, `search_by_vector`, and `delete`.
  - `PgVectorProvider` is a Phase 2 stub for Phase 4 pgvector wiring.
  - `OpenAIVectorStoreLegacyProvider` is disabled by default through `OPENAI_VECTOR_STORE_ENABLED=false`.
- `backend_py/app/services/embedding/`
  - `EmbeddingProvider` defines `dim` and `embed(texts)`.
  - DashScope and BGE local providers expose dimensions and raise clear Phase 2 stub errors.
- `backend_py/app/services/objectstore/`
  - `ObjectStoreProvider` defines `put`, `get`, `delete`, and `presigned_url`.
  - MinIO, OSS, and S3 providers are Phase 2 stubs.

## Real Implementations vs Stubs

- Real enough for compatibility: `OpenAILegacyProvider` and `OpenAIVectorStoreLegacyProvider` contain legacy SDK bridges, but neither is the default core path.
- Stub only: `DeepSeekProvider`, `PgVectorProvider`, `DashScopeEmbeddingProvider`, `BGELocalEmbeddingProvider`, `MinioObjectStoreProvider`, `OSSObjectStoreProvider`, and `S3ObjectStoreProvider`.
- Missing API keys do not fail during import or factory construction. Selected providers raise clear runtime errors only when called.

## frameworks.py Split

`backend_py/app/api/frameworks.py` is now an aggregate router that includes:

- `generation.py`
- `frameworks_crud.py`
- `exports.py`
- `ai_ops.py`
- `vector_sync.py`
- Shared schemas and helpers in `frameworks_shared.py`

The public route prefix remains `/api/frameworks`, and the Phase 1.1 JWT dependencies remain on export, regenerate, AI merge/fill, sync, and push endpoints.

Direct OpenAI client construction was removed from `backend_py/app/api`. Legacy vector sync now goes through the disabled-by-default legacy vector provider.

## Phase 2.1 Cleanup

After review, the core generation path was tightened so Phase 3 can switch providers cleanly:

- `process_with_global_llm()` now calls `get_llm_provider().generate_json()` instead of `llm_global.call_openai_framework`.
- `ai-merge` and `ai-fill` no longer decide real-vs-mock behavior from `OPENAI_API_KEY`; the configured provider now owns configuration readiness.
- API-layer calls no longer hard-code `gpt-4o`; provider defaults are used unless a caller supplies a model.
- The old local/Ollama metadata path now fails behind `ENABLE_LEGACY_LLM=true` instead of being silently available.
- A regression test scans `backend_py/app/api` for legacy LLM call gates.

## Phase 2.2 Provider Readiness Cleanup

This cleanup removes the remaining provider readiness blockers before Phase 3:

- `frontend/src/lib/api.js` and `frontend/src/components/CreateFramework.jsx` no longer default to or send `gpt-4o`; empty model values are omitted from request bodies and query strings.
- `backend_py/app/services/llm/model_policy.py` sanitizes legacy OpenAI model names (`gpt-4o`, `gpt-4`, `gpt-3.5-turbo`) for non-OpenAI providers so default DeepSeek can use its own model defaults.
- `process_with_global_llm()` applies the model policy immediately before provider invocation.
- `generate-from-file` now uses deterministic metadata extraction by default: filename/first line title, keyword hints, section previews, source files, source count, and `processing_mode=direct_file_metadata`.
- `generate-from-file`, `generate-from-files`, and regenerate local mode still keep the legacy local/Ollama path only when explicitly selected, and it remains guarded by `ENABLE_LEGACY_LLM=true`.
- No real DeepSeek, OpenAI, Ollama, GCP, DashScope, pgvector, RAG, Agent, LLMWiki, or frontend Firebase migration work was added.

## Configuration

Updated `.env.example` and `backend_py/.env.example` with:

- `LLM_PROVIDER`
- `DEEPSEEK_*`
- `VECTORSTORE_PROVIDER`
- `OPENAI_VECTOR_STORE_ENABLED`
- `OPENAI_VECTOR_STORE_*`
- `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL`, `EMBEDDING_DIM`
- `OBJECT_STORE_PROVIDER` and object store placeholders

## Tests Added

Added `backend_py/tests/test_provider_abstractions.py` covering:

- Default LLM provider selection
- Unknown provider errors
- DeepSeek runtime configuration error
- pgvector stub behavior
- OpenAI Vector Store legacy default disabled state
- readable `EmbeddingProvider.dim`
- Object store stub behavior
- Phase 2.2 model sanitization and frontend/API `gpt-4o` scans
- Default file upload path avoiding legacy local/Ollama
- Legacy local/Ollama default 503 guard

## Handoff

- Phase 3: implement real DeepSeek V4 in `DeepSeekProvider` and move remaining legacy LLM generation paths behind `LLMProvider`.
- Phase 3: implement `DeepSeekProvider.generate_json()` and rely on provider defaults when sanitized model is `None`.
- Phase 3/5: remove or further downgrade the guarded legacy local/Ollama metadata path after DeepSeek generation is live.
- Phase 4: implement `PgVectorProvider` with SQLAlchemy and pgvector tables; use `EmbeddingProvider.dim` for vector column sizing.
- Phase 8: Agent orchestration can target `LLMProvider.tool_call` without importing vendor SDKs in API code.
- Phase 9: RAG indexing should call `EmbeddingProvider.embed` first, then `VectorStoreProvider.upsert_vectors`; retrieval should call embedding first, then `search_by_vector`.
