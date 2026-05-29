from __future__ import annotations

import json
import os
import re
from collections.abc import Iterable, Mapping
from typing import Any, Optional

from .base import LLMProvider, LLMProviderConfigurationError


class OpenAILegacyProvider(LLMProvider):
    """Compatibility provider for old OpenAI-backed flows."""

    name = "openai_legacy"

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        self.base_url = base_url if base_url is not None else os.getenv("OPENAI_BASE_URL")
        self.default_model = default_model or os.getenv("OPENAI_MODEL", "gpt-4o")

    def _client(self, *, timeout: Optional[float] = None):
        if not self.api_key:
            raise LLMProviderConfigurationError(
                "OpenAILegacyProvider is selected, but OPENAI_API_KEY is not configured."
            )

        from openai import OpenAI

        kwargs: dict[str, Any] = {
            "api_key": self.api_key,
            "max_retries": 2,
        }
        if self.base_url:
            kwargs["base_url"] = self.base_url
        if timeout is not None:
            kwargs["timeout"] = timeout
        return OpenAI(**kwargs)

    def chat(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        timeout = kwargs.pop("timeout", None)
        client = self._client(timeout=timeout)
        request: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": list(messages),
        }
        if temperature is not None:
            request["temperature"] = temperature
        request.update(kwargs)
        response = client.chat.completions.create(**request)
        return (response.choices[0].message.content or "").strip()

    def stream(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Iterable[str]:
        timeout = kwargs.pop("timeout", None)
        client = self._client(timeout=timeout)
        request: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": list(messages),
            "stream": True,
        }
        if temperature is not None:
            request["temperature"] = temperature
        request.update(kwargs)
        for chunk in client.chat.completions.create(**request):
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def tool_call(
        self,
        messages: Iterable[Mapping[str, Any]],
        tools: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        tool_choice: Any = None,
        **kwargs: Any,
    ) -> Any:
        timeout = kwargs.pop("timeout", None)
        client = self._client(timeout=timeout)
        request: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": list(messages),
            "tools": list(tools),
        }
        if tool_choice is not None:
            request["tool_choice"] = tool_choice
        request.update(kwargs)
        return client.chat.completions.create(**request)

    def generate_json(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Any:
        text = self.chat(
            messages,
            model=model,
            temperature=temperature,
            **kwargs,
        )
        return self._parse_json_response(text)

    @staticmethod
    def _parse_json_response(text: str) -> Any:
        cleaned = text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
            if match:
                return json.loads(match.group(1))
            raise
