from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from typing import Any, Optional


class LLMProviderError(RuntimeError):
    """Base error for LLM provider failures."""


class LLMProviderConfigurationError(LLMProviderError):
    """Raised when a provider is selected but required config is missing."""


class LLMProviderDisabledError(LLMProviderError):
    """Raised when a legacy provider is intentionally disabled."""


class LLMProvider(ABC):
    """Abstract interface for all large-language-model providers."""

    name: str

    @abstractmethod
    def chat(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        """Return a complete chat response as text."""

    @abstractmethod
    def stream(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Iterable[str]:
        """Yield a streaming chat response as text chunks."""

    @abstractmethod
    def tool_call(
        self,
        messages: Iterable[Mapping[str, Any]],
        tools: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        tool_choice: Any = None,
        **kwargs: Any,
    ) -> Any:
        """Run a tool-capable chat request."""

    @abstractmethod
    def generate_json(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Any:
        """Return a parsed JSON value from an LLM response."""
