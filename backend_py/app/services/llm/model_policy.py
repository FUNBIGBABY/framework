from __future__ import annotations

import os
from typing import Optional


OPENAI_LEGACY_PROVIDERS = {"openai", "openai_legacy"}
OPENAI_LEGACY_MODEL_PREFIXES = (
    "gpt-4o",
    "gpt-4",
    "gpt-3.5-turbo",
)


def get_configured_llm_provider_name(provider_name: Optional[str] = None) -> str:
    """Return the effective LLM provider name without constructing a provider."""

    return (provider_name or os.getenv("LLM_PROVIDER") or "deepseek").strip().lower()


def sanitize_model_for_provider(
    model: Optional[str],
    *,
    provider_name: Optional[str] = None,
) -> Optional[str]:
    """Drop legacy OpenAI model names for non-OpenAI providers.

    This keeps old frontends or API clients from accidentally passing `gpt-*`
    model names into the default DeepSeek provider. The legacy OpenAI provider
    remains allowed to receive these names.
    """

    if model is None:
        return None

    normalized_model = str(model).strip()
    if not normalized_model:
        return None

    selected_provider = get_configured_llm_provider_name(provider_name)
    if selected_provider in OPENAI_LEGACY_PROVIDERS:
        return normalized_model

    lowered_model = normalized_model.lower()
    if lowered_model.startswith(OPENAI_LEGACY_MODEL_PREFIXES):
        return None

    return normalized_model
