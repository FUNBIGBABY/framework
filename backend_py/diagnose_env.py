#!/usr/bin/env python3
"""
Environment variable diagnostic script for the current provider setup.

This script performs local configuration checks only. It does not call any LLM
or legacy Cloud LLM endpoint.
"""

import os

from dotenv import load_dotenv


def _enabled(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


print("=" * 60)
print("PROVIDER ENVIRONMENT DIAGNOSTIC")
print("=" * 60)

env_file = ".env"
if os.path.exists(env_file):
    print(f"OK .env file found: {os.path.abspath(env_file)}")
else:
    print(f"ERROR .env file NOT found in: {os.getcwd()}")
    print("      Create .env in backend_py or export the required variables.")
    exit(1)

print("\nLoading .env file...")
load_dotenv()
print("OK dotenv loaded")

print("\nChecking provider environment variables:")
print("-" * 60)

expected_vars = {
    "LLM_PROVIDER": "deepseek",
    "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
    "DEEPSEEK_MODEL_DEFAULT": "deepseek-v4-flash",
    "DEEPSEEK_MODEL_REASONING": "deepseek-v4-pro",
    "DEEPSEEK_THINKING_MODE": "false",
    "ENABLE_LEGACY_LLM": "false",
}

all_ok = True

for var, expected in expected_vars.items():
    value = os.getenv(var, "")
    display_value = value or "NOT SET"
    print(f"{var}: {display_value} (expected default: {expected})")

    if var == "LLM_PROVIDER" and value.strip().lower() not in {"", "deepseek"}:
        print("  ERROR: default provider should be deepseek for Phase 3.")
        all_ok = False
    if var == "DEEPSEEK_BASE_URL":
        normalized = (value or expected).rstrip("/")
        if normalized.endswith("/v1"):
            print("  ERROR: DEEPSEEK_BASE_URL must not include a /v1 suffix.")
            all_ok = False
    if var == "ENABLE_LEGACY_LLM" and _enabled(value):
        print("  ERROR: legacy local/Ollama/GCP path is enabled.")
        all_ok = False

api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"DEEPSEEK_API_KEY: {'SET' if api_key else 'NOT SET'}")
if not api_key:
    print("  ERROR: DeepSeek calls will fail until DEEPSEEK_API_KEY is configured.")
    all_ok = False

print("-" * 60)

print("\nTesting provider factory initialization without a network call...")
try:
    from app.services.llm import get_llm_provider

    provider = get_llm_provider()

    print("Provider configuration:")
    print(f"  - name: {provider.name}")
    print(f"  - base_url: {getattr(provider, 'base_url', '(n/a)')}")
    print(f"  - default_model: {getattr(provider, 'default_model', '(n/a)')}")
    print(f"  - reasoning_model: {getattr(provider, 'reasoning_model', '(n/a)')}")

    if provider.name != "deepseek":
        print("ERROR: provider factory did not select DeepSeek.")
        all_ok = False

except Exception as exc:
    print(f"ERROR creating provider: {exc}")
    all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("ALL CHECKS PASSED")
    print("Provider configuration is ready for the Phase 3 DeepSeek path.")
else:
    print("SOME CHECKS FAILED")
    print("Fix the issues above before relying on the backend LLM path.")
print("=" * 60)
