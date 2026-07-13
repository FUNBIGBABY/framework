"""Opt-in real DeepSeek V4 thinking-mode tool-call smoke.

This script intentionally calls ``DeepSeekProvider.tool_call()``. It does not
print the API key, prompt, model reasoning, or tool arguments.

Required env:
- RUN_REAL_DEEPSEEK_TOOL_CALL_SMOKE=true
- DEEPSEEK_API_KEY
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib import request as urllib_request
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.llm.deepseek import DeepSeekProvider  # noqa: E402


_OFFICIAL_ENDPOINT_HOST = "api.deepseek.com"
_SAFE_EVIDENCE_VALUE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_DEFAULT_TRANSPORT_PROXY_SCHEMES = ("http", "https", "all")


def _require_opt_in() -> None:
    enabled = os.getenv("RUN_REAL_DEEPSEEK_TOOL_CALL_SMOKE", "false")
    if enabled.strip().lower() not in {"1", "true", "yes", "on"}:
        raise SystemExit(
            "Not run: set RUN_REAL_DEEPSEEK_TOOL_CALL_SMOKE=true to authorize "
            "a real DeepSeek API request."
        )
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise SystemExit("Not run: DEEPSEEK_API_KEY is not configured.")


def _official_endpoint_host(base_url: str) -> str:
    parsed = urlsplit(base_url)
    try:
        port = parsed.port
    except ValueError as exc:
        raise SystemExit(
            "Not run: the real DeepSeek smoke requires the official HTTPS endpoint."
        ) from exc

    if (
        parsed.scheme.lower() != "https"
        or parsed.hostname != _OFFICIAL_ENDPOINT_HOST
        or port not in {None, 443}
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise SystemExit(
            "Not run: the real DeepSeek smoke requires the official HTTPS endpoint."
        )
    return _OFFICIAL_ENDPOINT_HOST


def _require_direct_transport() -> None:
    configured_proxies = urllib_request.getproxies()
    if any(
        configured_proxies.get(scheme)
        for scheme in _DEFAULT_TRANSPORT_PROXY_SCHEMES
    ):
        raise SystemExit(
            "Not run: the real DeepSeek smoke requires a direct connection; "
            "proxy configuration is present."
        )


def _safe_evidence_value(value: Any, *, label: str) -> str:
    text = str(value or "").strip()
    if not _SAFE_EVIDENCE_VALUE.fullmatch(text):
        raise RuntimeError(f"Smoke failed: unsafe or missing {label}.")
    return text


def _tool_call_ids(tool_calls: Any) -> list[str]:
    if not isinstance(tool_calls, list) or not tool_calls:
        raise RuntimeError("Smoke failed: DeepSeek did not return a tool call.")

    call_ids = []
    for call in tool_calls:
        if isinstance(call, dict):
            call_id = call.get("id")
        else:
            call_id = getattr(call, "id", None)
        call_ids.append(_safe_evidence_value(call_id, label="tool-call identifier"))
    return call_ids


def main() -> None:
    _require_opt_in()
    _require_direct_transport()
    provider = DeepSeekProvider()
    endpoint_host = _official_endpoint_host(provider.base_url)
    selected_model = _safe_evidence_value(
        provider.reasoning_model, label="selected model"
    )
    message = provider.tool_call(
        [
            {
                "role": "system",
                "content": (
                    "Call lookup_weather exactly once for the requested city. "
                    "Do not answer directly."
                ),
            },
            {"role": "user", "content": "What is the weather in Hangzhou?"},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "lookup_weather",
                    "description": "Look up the current weather for a city.",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                        "additionalProperties": False,
                    },
                },
            }
        ],
        model=selected_model,
        reasoning=True,
        reasoning_effort="high",
        tool_choice="auto",
        max_tokens=1024,
        timeout=60,
    )

    call_ids = _tool_call_ids(message.get("tool_calls"))
    response_id = message.get("response_id")
    request_id = message.get("request_id")
    reasoning_preserved = bool(message.get("reasoning_content"))

    evidence_fields = [
        f"endpoint_host={endpoint_host}",
        f"selected_model={selected_model}",
    ]
    if response_id is not None:
        evidence_fields.append(
            "provider_response_id="
            + _safe_evidence_value(response_id, label="provider response identifier")
        )
    if request_id is not None:
        evidence_fields.append(
            "sdk_request_id="
            + _safe_evidence_value(request_id, label="SDK request identifier")
        )
    evidence_fields.extend(
        [
            f"tool_call_ids={','.join(call_ids)}",
            "reasoning_content=" + ("present" if reasoning_preserved else "absent"),
            f"tool_call_count={len(call_ids)}",
        ]
    )
    if not reasoning_preserved:
        raise RuntimeError("Smoke failed: " + "; ".join(evidence_fields))

    print("DeepSeek thinking tool-call smoke passed; " + "; ".join(evidence_fields))


if __name__ == "__main__":
    main()
