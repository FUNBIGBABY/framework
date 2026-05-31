from io import BytesIO
import os
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-for-provider-abstractions-32-chars")

import pytest
from fastapi import HTTPException, UploadFile

from app.api import frameworks_shared, generation
from app.services.embedding import EmbeddingProvider, get_embedding_provider
from app.services.llm import LLMProviderConfigurationError, get_llm_provider
from app.services.llm.deepseek import DeepSeekProvider
from app.services.llm.model_policy import sanitize_model_for_provider
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
        name = "deepseek"

        def generate_json(self, messages, **kwargs):
            captured["messages"] = messages
            captured["kwargs"] = kwargs
            return {"metadata": {"title": "Provider Result"}, "steps": []}

    monkeypatch.setattr(frameworks_shared, "get_llm_provider", lambda: FakeProvider())

    result = frameworks_shared.process_with_global_llm(
        {"title": "Provider Input"},
        model="gpt-4o",
    )

    assert result["metadata"]["title"] == "Provider Result"
    assert "Provider Input" in captured["messages"][1]["content"]
    assert captured["kwargs"]["model"] is None
    assert captured["kwargs"]["reasoning"] is False


def test_framework_generation_can_request_deepseek_reasoning(monkeypatch):
    captured = {}

    class FakeProvider:
        name = "deepseek"

        def generate_json(self, messages, **kwargs):
            captured["kwargs"] = kwargs
            return {"metadata": {"title": "Deep Result"}, "steps": []}

    monkeypatch.setattr(frameworks_shared, "get_llm_provider", lambda: FakeProvider())

    result = frameworks_shared.process_with_global_llm(
        {"title": "Provider Input"},
        reasoning=True,
    )

    assert result["metadata"]["title"] == "Deep Result"
    assert captured["kwargs"]["reasoning"] is True


def test_legacy_openai_models_are_preserved_for_openai_legacy_provider():
    assert (
        sanitize_model_for_provider("gpt-4o", provider_name="openai_legacy") == "gpt-4o"
    )
    assert sanitize_model_for_provider("deepseek-v4-flash") == "deepseek-v4-flash"


def test_legacy_local_path_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("ENABLE_LEGACY_LLM", raising=False)

    with pytest.raises(HTTPException) as exc:
        frameworks_shared.process_with_local_llm("hello")

    assert exc.value.status_code == 503
    assert "ENABLE_LEGACY_LLM=true" in exc.value.detail


@pytest.mark.asyncio
async def test_generate_from_file_default_path_avoids_legacy_local(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("process_with_local_llm should not run by default")

    captured = {}

    def fake_global(metadata, model=None, use_mock=False, reasoning=False):
        captured["metadata"] = metadata
        captured["model"] = model
        captured["use_mock"] = use_mock
        captured["reasoning"] = reasoning
        return {"metadata": {"title": metadata["title"]}, "steps": []}

    def fake_save_framework_to_db(framework_data, metadata_dict, creator_id, db):
        return SimpleNamespace(id="fw_test")

    monkeypatch.setattr(generation, "process_with_local_llm", fail_if_called)
    monkeypatch.setattr(generation, "process_with_global_llm", fake_global)
    monkeypatch.setattr(generation, "save_framework_to_db", fake_save_framework_to_db)

    upload = UploadFile(
        filename="roadmap.txt",
        file=BytesIO(b"Roadmap Plan\nStep one\nStep two"),
    )

    response = await generation.generate_from_file(
        upload,
        use_global_llm=True,
        user_id="user-1",
        db=object(),
    )

    assert response.success is True
    assert response.framework_id == "fw_test"
    assert captured["metadata"]["title"] == "Roadmap Plan"
    assert captured["metadata"]["extra"]["processing_mode"] == "direct_file_metadata"
    assert captured["use_mock"] is False
    assert captured["reasoning"] is False


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


def test_frontend_and_api_have_no_openai_default_model_name():
    repo_root = Path(__file__).resolve().parents[2]
    checked_roots = [
        repo_root / "frontend" / "src",
        repo_root / "backend_py" / "app" / "api",
    ]

    offenders = []
    for root in checked_roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in {".js", ".jsx", ".py"}:
                if "gpt-4o" in path.read_text(encoding="utf-8"):
                    offenders.append(str(path.relative_to(repo_root)))

    assert offenders == []
