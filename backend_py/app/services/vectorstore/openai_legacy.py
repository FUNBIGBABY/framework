from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from typing import Any, Optional

from .base import (
    VectorStoreProvider,
    VectorStoreProviderConfigurationError,
    VectorStoreProviderDisabledError,
)


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class OpenAIVectorStoreLegacyProvider(VectorStoreProvider):
    """Legacy OpenAI Vector Store compatibility provider.

    This is intentionally disabled by default and should only be used for old
    migration/sync utilities, not as the core RAG path.
    """

    name = "openai_legacy"

    def __init__(
        self,
        *,
        enabled: Optional[bool] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.enabled = (
            _env_flag("OPENAI_VECTOR_STORE_ENABLED", False)
            if enabled is None
            else enabled
        )
        self.api_key = (
            api_key
            if api_key is not None
            else os.getenv("OPENAI_VECTOR_STORE_API_KEY") or os.getenv("OPENAI_API_KEY")
        )

    def ensure_enabled(self) -> None:
        if not self.enabled:
            raise VectorStoreProviderDisabledError(
                "OpenAI Vector Store legacy provider is disabled. Set "
                "OPENAI_VECTOR_STORE_ENABLED=true only for explicit legacy migration tasks."
            )
        if not self.api_key:
            raise VectorStoreProviderConfigurationError(
                "OpenAI Vector Store legacy provider is enabled, but no "
                "OPENAI_VECTOR_STORE_API_KEY or OPENAI_API_KEY is configured."
            )

    def _ensure_enabled(self) -> None:
        self.ensure_enabled()

    def _client(self):
        self._ensure_enabled()
        from openai import OpenAI

        return OpenAI(api_key=self.api_key)

    @staticmethod
    def _vector_store_api(client: Any) -> Any:
        try:
            return client.vector_stores
        except AttributeError:
            return client.beta.vector_stores

    def upload_json(
        self,
        *,
        vector_store_id: str,
        filename: str,
        content: str,
        attributes: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        """Upload a JSON payload to an existing OpenAI Vector Store."""

        import io

        client = self._client()
        vector_store_api = self._vector_store_api(client)
        payload = io.BytesIO(content.encode("utf-8"))
        payload.name = filename

        try:
            file_obj = client.files.create(file=payload, purpose="assistants")
            try:
                return vector_store_api.files.create(
                    vector_store_id=vector_store_id,
                    file_id=file_obj.id,
                    attributes=dict(attributes or {}),
                )
            except TypeError:
                return vector_store_api.files.create(
                    vector_store_id=vector_store_id,
                    file_id=file_obj.id,
                )
        except Exception:
            payload.seek(0)
            return vector_store_api.files.upload(
                vector_store_id=vector_store_id,
                file=payload,
            )

    def upsert_vectors(
        self,
        namespace: str,
        chunks_with_vectors: Iterable[Mapping[str, Any]],
    ) -> None:
        self._ensure_enabled()
        raise NotImplementedError(
            "OpenAIVectorStoreLegacyProvider does not implement provider-native vector upsert. "
            "It is retained only for legacy file-based migration utilities."
        )

    def search_by_vector(
        self,
        namespace: str,
        vector: list[float],
        k: int = 5,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        self._ensure_enabled()
        raise NotImplementedError(
            "OpenAIVectorStoreLegacyProvider does not implement provider-native vector search. "
            "Use PgVectorProvider after Phase 4."
        )

    def delete(
        self,
        namespace: str,
        ids: Optional[Iterable[str] | str] = None,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self._ensure_enabled()
        raise NotImplementedError(
            "OpenAIVectorStoreLegacyProvider delete support is deferred to a legacy migration tool."
        )
