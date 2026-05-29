from __future__ import annotations

import os
from typing import Optional

from .base import VectorStoreProvider
from .openai_legacy import OpenAIVectorStoreLegacyProvider
from .pgvector import PgVectorProvider


def get_vectorstore_provider(provider_name: Optional[str] = None) -> VectorStoreProvider:
    """Return the configured vector store provider without making network calls."""

    selected = (
        provider_name or os.getenv("VECTORSTORE_PROVIDER") or "pgvector"
    ).strip().lower()
    providers = {
        "pgvector": PgVectorProvider,
        "openai_legacy": OpenAIVectorStoreLegacyProvider,
        "openai": OpenAIVectorStoreLegacyProvider,
    }

    provider_cls = providers.get(selected)
    if provider_cls is None:
        supported = ", ".join(sorted(providers))
        raise ValueError(
            f"Unknown VECTORSTORE_PROVIDER '{selected}'. Supported providers: {supported}"
        )

    return provider_cls()
