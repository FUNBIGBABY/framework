from pathlib import Path

import pytest

from app.api import frameworks_shared
from app.services.embedding import EmbeddingProvider, get_embedding_provider
from app.services.llm import LLMProviderConfigurationError, get_llm_provider
from app.services.llm.deepseek import DeepSeekProvider
from app.services.objectstore import get_objectstore_provider
from app.services.objectstore.minio import MinioObjectStoreProvider
from app.services.vectorstore import (
    VectorStoreProviderDisabledError,
    get_vectorstore_provider,
)
from app.services.vectorstore.openai_legacy import OpenAIVectorStoreLegacyProvider
from app.services.vectorstore.pgvector import PgVectorProvider


def test_llm_factory_defaults_to_deepseek(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    provider = get_llm_provider()

    assert isinstance(provider, DeepSeekProvider)
    assert provider.name == "deepseek"


def test_llm_factory_unknown_provider_has_clear_error():
    with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
        get_llm_provider("not-a-provider")


def test_deepseek_stub_defers_runtime_failure_until_call(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    provider = get_llm_provider("deepseek")

    with pytest.raises(LLMProviderConfigurationError, match="DEEPSEEK_API_KEY"):
        provider.chat([{"role": "user", "content": "hello"}])


def test_pgvector_stub_methods_raise_clear_not_implemented():
    provider = get_vectorstore_provider("pgvector")

    assert isinstance(provider, PgVectorProvider)
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        provider.search_by_vector("frameworks", [0.1, 0.2, 0.3])


def test_openai_vector_store_legacy_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("OPENAI_VECTOR_STORE_ENABLED", raising=False)

    provider = get_vectorstore_provider("openai_legacy")

    assert isinstance(provider, OpenAIVectorStoreLegacyProvider)
    assert provider.enabled is False
    with pytest.raises(VectorStoreProviderDisabledError, match="disabled"):
        provider.upsert_vectors("frameworks", [])


def test_embedding_provider_exposes_dim(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "dashscope")
    monkeypatch.setenv("EMBEDDING_DIM", "1536")

    provider = get_embedding_provider()

    assert isinstance(provider, EmbeddingProvider)
    assert provider.dim == 1536
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        provider.embed(["hello"])


def test_objectstore_default_provider_is_stub(monkeypatch):
    monkeypatch.delenv("OBJECT_STORE_PROVIDER", raising=False)

    provider = get_objectstore_provider()

    assert isinstance(provider, MinioObjectStoreProvider)
    with pytest.raises(NotImplementedError, match="Phase 2 stub"):
        provider.put("example.txt", b"hello", "text/plain")


def test_framework_generation_uses_llm_provider(monkeypatch):
    captured = {}

    class FakeProvider:
        def generate_json(self, messages, **kwargs):
            captured["messages"] = messages
            captured["kwargs"] = kwargs
            return {"metadata": {"title": "Provider Result"}, "steps": []}

    monkeypatch.setattr(frameworks_shared, "get_llm_provider", lambda: FakeProvider())

    result = frameworks_shared.process_with_global_llm({"title": "Provider Input"})

    assert result["metadata"]["title"] == "Provider Result"
    assert "Provider Input" in captured["messages"][1]["content"]
    assert captured["kwargs"]["model"] is None


def test_api_layer_has_no_legacy_llm_call_gates():
    api_dir = Path(__file__).resolve().parents[1] / "app" / "api"
    forbidden_patterns = [
        "from openai import OpenAI",
        "openai.OpenAI(",
        "client.chat",
        "call_openai_framework",
        "llm_global",
        "resolve_api_settings",
        "gpt-4o",
    ]

    offenders = []
    for path in api_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            if pattern in text:
                offenders.append(f"{path.name}: {pattern}")

    assert offenders == []
