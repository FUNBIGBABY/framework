from __future__ import annotations

import os

from .base import EmbeddingProvider


class BGELocalEmbeddingProvider(EmbeddingProvider):
    """Phase 2 stub for local BGE embeddings."""

    name = "bge_local"

    def __init__(self, *, dim: int | None = None) -> None:
        configured_dim = dim or int(os.getenv("EMBEDDING_DIM") or "1024")
        super().__init__(dim=configured_dim)
        self.model = os.getenv("EMBEDDING_MODEL", "bge-m3")

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError(
            "BGELocalEmbeddingProvider is a Phase 2 stub. Local model loading is deferred to Phase 9."
        )
