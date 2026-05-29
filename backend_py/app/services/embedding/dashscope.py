from __future__ import annotations

import os

from .base import EmbeddingProvider


class DashScopeEmbeddingProvider(EmbeddingProvider):
    """Phase 2 stub for Alibaba DashScope embeddings."""

    name = "dashscope"

    def __init__(self, *, dim: int | None = None) -> None:
        configured_dim = dim or int(os.getenv("EMBEDDING_DIM") or "1024")
        super().__init__(dim=configured_dim)
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError(
            "DashScopeEmbeddingProvider is a Phase 2 stub. Real embedding calls are deferred to Phase 9."
        )
