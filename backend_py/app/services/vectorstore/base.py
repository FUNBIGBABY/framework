from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from typing import Any, Optional


class VectorStoreProviderError(RuntimeError):
    """Base error for vector store provider failures."""


class VectorStoreProviderDisabledError(VectorStoreProviderError):
    """Raised when a legacy vector store provider is disabled."""


class VectorStoreProviderConfigurationError(VectorStoreProviderError):
    """Raised when selected vector store config is incomplete."""


class VectorStoreProvider(ABC):
    """Abstract vector storage interface.

    Embedding generation deliberately lives outside this interface.
    """

    name: str

    @abstractmethod
    def upsert_vectors(
        self,
        namespace: str,
        chunks_with_vectors: Iterable[Mapping[str, Any]],
    ) -> None:
        """Insert or update vectorized chunks in a namespace."""

    @abstractmethod
    def search_by_vector(
        self,
        namespace: str,
        vector: list[float],
        k: int = 5,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        """Search a namespace by vector and optional filters."""

    @abstractmethod
    def delete(
        self,
        namespace: str,
        ids: Optional[Iterable[str] | str] = None,
        filters: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Delete vectors by ids or filters."""
