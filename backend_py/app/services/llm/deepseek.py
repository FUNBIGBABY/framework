from __future__ import annotations

import json
import os
import re
from collections.abc import Iterable, Mapping
from typing import Any, Optional

from openai import OpenAI

from .base import LLMProvider, LLMProviderConfigurationError, LLMProviderError


_INEFFECTIVE_THINKING_PARAMS = {
    "temperature",
    "top_p",
    "presence_penalty",
    "frequency_penalty",
}


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off", "disabled"}


def _get_value(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump(exclude_none=True))
    if isinstance(value, Mapping):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


class DeepSeekProvider(LLMProvider):
    """OpenAI-compatible provider for DeepSeek V4."""

    name = "deepseek"

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
        reasoning_model: Optional[str] = None,
        thinking_mode: Optional[bool] = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("DEEPSEEK_API_KEY")

        configured_base_url = base_url or os.getenv(
            "DEEPSEEK_BASE_URL", "https://api.deepseek.com"
        )
        self.base_url = configured_base_url.rstrip("/")
        if self.base_url.endswith("/v1"):
            raise LLMProviderConfigurationError(
                "DEEPSEEK_BASE_URL must be https://api.deepseek.com without a /v1 suffix."
            )

        self.default_model = default_model or os.getenv(
            "DEEPSEEK_MODEL_DEFAULT", "deepseek-v4-flash"
        )
        self.reasoning_model = reasoning_model or os.getenv(
            "DEEPSEEK_MODEL_REASONING", "deepseek-v4-pro"
        )
        self.thinking_enabled_by_default = (
            thinking_mode
            if thinking_mode is not None
            else _env_bool("DEEPSEEK_THINKING_MODE", False)
        )

    def _client(self, *, timeout: Optional[float] = None) -> OpenAI:
        if not self.api_key:
            raise LLMProviderConfigurationError(
                "DeepSeekProvider is selected, but DEEPSEEK_API_KEY is not configured."
            )

        kwargs: dict[str, Any] = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "max_retries": 2,
        }
        if timeout is not None:
            kwargs["timeout"] = timeout
        try:
            return OpenAI(**kwargs)
        except Exception as exc:
            raise LLMProviderError(
                f"DeepSeek client initialization failed: {self._safe_error_message(exc)}"
            ) from exc

    def _safe_error_message(self, exc: Exception) -> str:
        message = str(exc) or exc.__class__.__name__
        if self.api_key:
            message = message.replace(self.api_key, "[redacted]")
        return message

    def _reasoning_enabled(self, reasoning: Optional[bool]) -> bool:
        if reasoning is None:
            return self.thinking_enabled_by_default
        return bool(reasoning)

    def _select_model(self, model: Optional[str], reasoning: Optional[bool]) -> str:
        if reasoning is True:
            return self.reasoning_model
        if model:
            return model
        return self.default_model

    def _thinking_extra_body(
        self,
        *,
        existing: Optional[Mapping[str, Any]],
        reasoning_enabled: bool,
    ) -> Optional[dict[str, Any]]:
        extra_body = dict(existing or {})

        extra_body["thinking"] = {
            "type": "enabled" if reasoning_enabled else "disabled"
        }

        return extra_body or None

    def _build_request(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str],
        temperature: Optional[float],
        json_mode: bool = False,
        stream: bool = False,
        tools: Optional[Iterable[Mapping[str, Any]]] = None,
        tool_choice: Any = None,
        **kwargs: Any,
    ) -> tuple[OpenAI, dict[str, Any]]:
        timeout = kwargs.pop("timeout", None)
        max_tokens = kwargs.pop("max_tokens", None)
        reasoning = kwargs.pop("reasoning", None)
        reasoning_effort = kwargs.pop("reasoning_effort", None)
        extra_body = kwargs.pop("extra_body", None)

        reasoning_enabled = self._reasoning_enabled(reasoning)
        request: dict[str, Any] = {
            "model": self._select_model(model, reasoning),
            "messages": list(messages),
        }

        if max_tokens is not None:
            request["max_tokens"] = max_tokens
        if stream:
            request["stream"] = True
        if json_mode:
            request["response_format"] = {"type": "json_object"}
        if tools is not None:
            request["tools"] = list(tools)
        if tool_choice is not None:
            request["tool_choice"] = tool_choice
        if reasoning_enabled and (reasoning is True or reasoning_effort):
            request["reasoning_effort"] = reasoning_effort or "high"

        passthrough = dict(kwargs)
        if reasoning_enabled:
            for key in _INEFFECTIVE_THINKING_PARAMS:
                passthrough.pop(key, None)
        elif temperature is not None:
            request["temperature"] = temperature

        request.update(passthrough)

        thinking_extra_body = self._thinking_extra_body(
            existing=extra_body,
            reasoning_enabled=reasoning_enabled,
        )
        if thinking_extra_body is not None:
            request["extra_body"] = thinking_extra_body

        return self._client(timeout=timeout), request

    def _create_completion(self, request: Mapping[str, Any]) -> Any:
        try:
            client = request["_client"]
            payload = {key: value for key, value in request.items() if key != "_client"}
            return client.chat.completions.create(**payload)
        except LLMProviderConfigurationError:
            raise
        except Exception as exc:
            raise LLMProviderError(
                f"DeepSeek request failed: {self._safe_error_message(exc)}"
            ) from exc

    def _message_from_response(self, response: Any) -> Any:
        choices = _get_value(response, "choices", [])
        if not choices:
            raise LLMProviderError("DeepSeek response did not include choices.")
        return _get_value(choices[0], "message")

    def chat(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        client, request = self._build_request(
            messages,
            model=model,
            temperature=temperature,
            **kwargs,
        )
        response = self._create_completion({"_client": client, **request})
        message = self._message_from_response(response)
        return (_get_value(message, "content") or "").strip()

    def stream(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Iterable[str]:
        client, request = self._build_request(
            messages,
            model=model,
            temperature=temperature,
            stream=True,
            **kwargs,
        )

        try:
            chunks = client.chat.completions.create(**request)
            for chunk in chunks:
                choices = _get_value(chunk, "choices", [])
                if not choices:
                    continue
                delta = _get_value(choices[0], "delta")
                content = _get_value(delta, "content")
                if content:
                    yield content
        except LLMProviderConfigurationError:
            raise
        except Exception as exc:
            raise LLMProviderError(
                f"DeepSeek stream failed: {self._safe_error_message(exc)}"
            ) from exc

    def tool_call(
        self,
        messages: Iterable[Mapping[str, Any]],
        tools: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        tool_choice: Any = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        client, request = self._build_request(
            messages,
            model=model,
            temperature=kwargs.pop("temperature", None),
            tools=tools,
            tool_choice=tool_choice,
            **kwargs,
        )
        response = self._create_completion({"_client": client, **request})
        message = self._message_from_response(response)
        data = _jsonable(message)
        if not isinstance(data, Mapping):
            data = {}

        return {
            "role": data.get("role", _get_value(message, "role", "assistant")),
            "content": data.get("content", _get_value(message, "content")),
            "reasoning_content": data.get(
                "reasoning_content", _get_value(message, "reasoning_content")
            ),
            "tool_calls": data.get("tool_calls", _get_value(message, "tool_calls")),
        }

    def generate_json(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> Any:
        client, request = self._build_request(
            messages,
            model=model,
            temperature=temperature,
            json_mode=True,
            **kwargs,
        )
        response = self._create_completion({"_client": client, **request})
        message = self._message_from_response(response)
        text = (_get_value(message, "content") or "").strip()
        return self._parse_json_response(text)

    @staticmethod
    def _parse_json_response(text: str) -> Any:
        cleaned = text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            raise LLMProviderError("DeepSeek returned invalid JSON.") from exc
