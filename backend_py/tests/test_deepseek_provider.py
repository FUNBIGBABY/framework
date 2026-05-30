from types import SimpleNamespace

import pytest

import app.services.llm.deepseek as deepseek_module
from app.services.llm import LLMProviderConfigurationError
from app.services.llm.deepseek import DeepSeekProvider
from app.services.llm.model_policy import sanitize_model_for_provider


def _install_fake_openai(monkeypatch, *, content='{"ok": true}'):
    requests = []
    clients = []

    class FakeCompletions:
        def create(self, **kwargs):
            requests.append(kwargs)
            if kwargs.get("stream"):
                return iter(
                    [
                        SimpleNamespace(
                            choices=[
                                SimpleNamespace(
                                    delta=SimpleNamespace(content="hel")
                                )
                            ]
                        ),
                        SimpleNamespace(
                            choices=[
                                SimpleNamespace(
                                    delta=SimpleNamespace(content="lo")
                                )
                            ]
                        ),
                    ]
                )

            message = SimpleNamespace(
                role="assistant",
                content=content,
                reasoning_content="kept reasoning",
                tool_calls=[{"id": "call_1", "type": "function"}],
            )
            return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    class FakeOpenAI:
        def __init__(self, **kwargs):
            clients.append(kwargs)
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=FakeCompletions().create)
            )

    monkeypatch.setattr(deepseek_module, "OpenAI", FakeOpenAI)
    return requests, clients


def test_deepseek_missing_api_key_raises_on_call(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    provider = DeepSeekProvider()

    with pytest.raises(LLMProviderConfigurationError, match="DEEPSEEK_API_KEY"):
        provider.chat([{"role": "user", "content": "hello"}])


def test_deepseek_base_url_rejects_v1_suffix():
    with pytest.raises(LLMProviderConfigurationError, match="/v1"):
        DeepSeekProvider(
            api_key="test-key",
            base_url="https://api.deepseek.com/v1/",
        )


def test_generate_json_uses_json_response_format(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.delenv("DEEPSEEK_THINKING_MODE", raising=False)
    requests, clients = _install_fake_openai(monkeypatch)

    provider = DeepSeekProvider()
    result = provider.generate_json([{"role": "user", "content": "json"}])

    assert result == {"ok": True}
    assert clients[0]["base_url"] == "https://api.deepseek.com"
    assert requests[0]["model"] == "deepseek-v4-flash"
    assert requests[0]["response_format"] == {"type": "json_object"}


def test_default_thinking_mode_is_fast_disabled_flash(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.delenv("DEEPSEEK_THINKING_MODE", raising=False)
    requests, _clients = _install_fake_openai(monkeypatch)

    provider = DeepSeekProvider()
    provider.generate_json(
        [{"role": "user", "content": "json"}],
        temperature=0.2,
    )

    assert requests[0]["model"] == "deepseek-v4-flash"
    assert requests[0]["extra_body"] == {"thinking": {"type": "disabled"}}
    assert requests[0]["temperature"] == 0.2


def test_chat_does_not_default_to_json_mode(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    requests, _clients = _install_fake_openai(monkeypatch, content="plain text")

    provider = DeepSeekProvider()
    assert provider.chat([{"role": "user", "content": "hello"}]) == "plain text"

    assert "response_format" not in requests[0]


def test_thinking_mode_false_sends_disabled_extra_body(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setenv("DEEPSEEK_THINKING_MODE", "false")
    requests, _clients = _install_fake_openai(monkeypatch)

    provider = DeepSeekProvider()
    provider.generate_json(
        [{"role": "user", "content": "json"}],
        temperature=0.3,
    )

    assert requests[0]["extra_body"] == {"thinking": {"type": "disabled"}}
    assert requests[0]["temperature"] == 0.3


def test_reasoning_true_uses_pro_model_and_enabled_high_thinking(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    requests, _clients = _install_fake_openai(monkeypatch)

    provider = DeepSeekProvider()
    provider.generate_json(
        [{"role": "user", "content": "json"}],
        reasoning=True,
        temperature=0.9,
    )

    assert requests[0]["model"] == "deepseek-v4-pro"
    assert requests[0]["extra_body"] == {"thinking": {"type": "enabled"}}
    assert requests[0]["reasoning_effort"] == "high"
    assert "temperature" not in requests[0]


def test_tool_call_preserves_reasoning_content_and_tool_calls(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    requests, _clients = _install_fake_openai(monkeypatch, content=None)

    provider = DeepSeekProvider()
    message = provider.tool_call(
        [{"role": "user", "content": "call tool"}],
        tools=[{"type": "function", "function": {"name": "lookup"}}],
        tool_choice="auto",
        reasoning=True,
    )

    assert requests[0]["tools"] == [
        {"type": "function", "function": {"name": "lookup"}}
    ]
    assert requests[0]["tool_choice"] == "auto"
    assert message["content"] is None
    assert message["reasoning_content"] == "kept reasoning"
    assert message["tool_calls"] == [{"id": "call_1", "type": "function"}]


def test_stream_yields_text_deltas(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    requests, _clients = _install_fake_openai(monkeypatch)

    provider = DeepSeekProvider()
    chunks = list(provider.stream([{"role": "user", "content": "hello"}]))

    assert chunks == ["hel", "lo"]
    assert requests[0]["stream"] is True
    assert "response_format" not in requests[0]


def test_legacy_gpt_4o_sanitize_returns_none_for_deepseek():
    assert sanitize_model_for_provider("gpt-4o", provider_name="deepseek") is None
