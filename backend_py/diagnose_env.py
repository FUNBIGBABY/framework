#!/usr/bin/env python3
"""
Environment variable diagnostic script
Diagnose whether environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

print("=" * 60)
print("ENVIRONMENT VARIABLE DIAGNOSTIC")
print("=" * 60)

# 1. Check if .env file exists
env_file = ".env"
if os.path.exists(env_file):
    print(f"✅ .env file found: {os.path.abspath(env_file)}")
else:
    print(f"❌ .env file NOT found in: {os.getcwd()}")
    print("   Please create .env file in backend_py directory")
    exit(1)

# 2. Load .env file
print("\n📂 Loading .env file...")
load_dotenv()
print("✅ dotenv loaded")

# 3. Check critical environment variables
print("\n🔍 Checking environment variables:")
print("-" * 60)

required_vars = {
    "LLM_TYPE": "Should be 'cloud'",
    "LOCAL_LLM_URL": "Should be 'http://34.87.13.228:8000/v1'",
    "LOCAL_LLM_MODEL": "Should be 'meta-llama/Llama-3.1-8B-Instruct'",
    "LOCAL_LLM_API_KEY": "Should start with 'sk-'",
    "OPENAI_API_KEY": "Should start with 'sk-'",
}

all_ok = True

for var, expected in required_vars.items():
    value = os.getenv(var)
    if value:
        # Mask API keys for security
        if "API_KEY" in var:
            display_value = value[:10] + "..." if len(value) > 10 else value
        else:
            display_value = value
        print(f"✅ {var}: {display_value}")
        print(f"   ({expected})")
    else:
        print(f"❌ {var}: NOT FOUND")
        print(f"   ({expected})")
        all_ok = False

print("-" * 60)

# 4. Test LLMClient initialization
print("\n🧪 Testing LLMClient initialization...")
try:
    from llm_local import LLMClient

    print("\nCreating LLMClient with default settings...")
    client = LLMClient()

    print(f"\n📊 LLMClient Configuration:")
    print(f"  - Type: {client.llm_type}")
    print(f"  - Host: {client.host}")
    print(f"  - Model: {client.model}")

    if client.llm_type == "cloud":
        if client.host == "http://34.87.13.228:8000/v1":
            print("\n✅ SUCCESS! LLMClient using correct Cloud LLM URL!")
        else:
            print(f"\n❌ ERROR! LLMClient using wrong URL: {client.host}")
            print(f"   Expected: http://34.87.13.228:8000/v1")
            all_ok = False
    else:
        print(f"\n❌ ERROR! LLMClient still using local type: {client.llm_type}")
        print(f"   Expected: cloud")
        all_ok = False

except Exception as e:
    print(f"❌ Error creating LLMClient: {e}")
    all_ok = False

# 5. Final verdict
print("\n" + "=" * 60)
if all_ok:
    print("🎉 ALL CHECKS PASSED!")
    print("   Your environment is configured correctly.")
    print("   You can now start the backend server.")
else:
    print("⚠️  SOME CHECKS FAILED!")
    print("   Please fix the issues above before continuing.")
print("=" * 60)
