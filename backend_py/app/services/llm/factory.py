from __future__ import annotations

import os
from typing import Optional

from .base import LLMProvider
from .deepseek import DeepSeekProvider
from .openai_legacy import OpenAILegacyProvider


def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    """Return the configured LLM provider without making network calls."""

    selected = (provider_name or os.getenv("LLM_PROVIDER") or "deepseek").strip().lower()
    providers = {
        "deepseek": DeepSeekProvider,
        "openai_legacy": OpenAILegacyProvider,
        "openai": OpenAILegacyProvider,
    }

    provider_cls = providers.get(selected)
    if provider_cls is None:
        supported = ", ".join(sorted(providers))
        raise ValueError(f"Unknown LLM_PROVIDER '{selected}'. Supported providers: {supported}")

    return provider_cls()
