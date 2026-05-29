from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from typing import Any, Optional

from .base import LLMProvider, LLMProviderConfigurationError


class DeepSeekProvider(LLMProvider):
    """Phase 2 stub for the future DeepSeek V4 implementation."""

    name = "deepseek"

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
        reasoning_model: Optional[str] = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.default_model = default_model or os.getenv(
            "DEEPSEEK_MODEL_DEFAULT", "deepseek-v4-flash"
        )
        self.reasoning_model = reasoning_model or os.getenv(
            "DEEPSEEK_MODEL_REASONING", "deepseek-v4-pro"
        )

    def _raise_phase2_stub(self) -> None:
        if not self.api_key:
            raise LLMProviderConfigurationError(
                "DeepSeekProvider is selected, but DEEPSEEK_API_KEY is not configured. "
                "Phase 2 only wires the provider interface; real DeepSeek API calls are "
                "deferred to Phase 3."
            )
        raise NotImplementedError(
            "DeepSeekProvider is a Phase 2 stub. Real DeepSeek V4 integration is deferred to Phase 3."
        )

    def chat(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        self._raise_phase2_stub()

    def stream(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Iterable[str]:
        self._raise_phase2_stub()

    def tool_call(
        self,
        messages: Iterable[Mapping[str, Any]],
        tools: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        tool_choice: Any = None,
        **kwargs: Any,
    ) -> Any:
        self._raise_phase2_stub()

    def generate_json(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Any:
        self._raise_phase2_stub()
