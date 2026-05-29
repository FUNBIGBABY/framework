from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingProviderError(RuntimeError):
    """Base error for embedding provider failures."""


class EmbeddingProvider(ABC):
    """Abstract interface for embedding providers."""

    name: str

    def __init__(self, *, dim: int) -> None:
        self.dim = dim

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of text strings."""
