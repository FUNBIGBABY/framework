from __future__ import annotations

import os
from typing import Optional

from .base import EmbeddingProvider
from .bge_local import BGELocalEmbeddingProvider
from .dashscope import DashScopeEmbeddingProvider


def get_embedding_provider(provider_name: Optional[str] = None) -> EmbeddingProvider:
    """Return the configured embedding provider without making network calls."""

    selected = (
        provider_name or os.getenv("EMBEDDING_PROVIDER") or "dashscope"
    ).strip().lower()
    providers = {
        "dashscope": DashScopeEmbeddingProvider,
        "bge_local": BGELocalEmbeddingProvider,
        "bge": BGELocalEmbeddingProvider,
        "local": BGELocalEmbeddingProvider,
    }

    provider_cls = providers.get(selected)
    if provider_cls is None:
        supported = ", ".join(sorted(providers))
        raise ValueError(
            f"Unknown EMBEDDING_PROVIDER '{selected}'. Supported providers: {supported}"
        )

    return provider_cls()
