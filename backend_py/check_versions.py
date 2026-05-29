import sys

print("=" * 50)
print("Environment Diagnostic Report")
print("=" * 50)

# Python version
print(f"\n🐍 Python Version: {sys.version}")

# OpenAI SDK version
try:
    import openai

    print(f"✅ OpenAI SDK Version: {openai.__version__}")
except ImportError:
    print("❌ OpenAI SDK is not installed")
except AttributeError:
    print("⚠️ Unable to determine OpenAI SDK version")

# httpx version
try:
    import httpx

    print(f"✅ httpx Version: {httpx.__version__}")
except ImportError:
    print("❌ httpx is not installed")
except AttributeError:
    print("⚠️ Unable to determine httpx version")

# requests version
try:
    import requests

    print(f"✅ requests Version: {requests.__version__}")
except ImportError:
    print("❌ requests is not installed")

print("\n" + "=" * 50)
print("Diagnostic Suggestions")
print("=" * 50)

# Compatibility check
try:
    import openai
    import httpx

    openai_version = tuple(map(int, openai.__version__.split(".")[:2]))
    httpx_version = tuple(map(int, httpx.__version__.split(".")[:2]))

    print(f"\nOpenAI {openai.__version__} + httpx {httpx.__version__}")

    # OpenAI 1.10+ requires httpx 0.24+
    if openai_version >= (1, 10) and httpx_version < (0, 24):
        print("⚠️ Version incompatibility detected! OpenAI 1.10+ requires httpx 0.24+")
        print("\n📝 Solution 1 (Recommended): Upgrade httpx")
        print("   pip install --upgrade httpx")
        print("\n📝 Solution 2: Downgrade OpenAI SDK")
        print("   pip install openai==1.3.0")
    else:
        print("✅ Version combination appears compatible")
        print("⚠️ The issue may be related to system proxy settings")

except Exception as e:
    print(f"⚠️ Unable to perform version compatibility check: {e}")

print("\n" + "=" * 50)
