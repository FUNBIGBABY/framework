from openai import OpenAI

# ============ 配置 ============
API_KEY = "Your open ai API key"
VS_ID = "VS ID"
# ==============================

client = OpenAI(api_key=API_KEY)

print(f"🔍 Checking Vector Store: {VS_ID}")
print("=" * 70)

try:
    # show files in vector store
    files = client.vector_stores.files.list(vector_store_id=VS_ID, limit=20)

    print(f"\n📁 Found {len(files.data)} file(s) in Vector Store:\n")

    has_attributes = False
    missing_attributes = False

    for i, file in enumerate(files.data, 1):
        print(f"{'─'*70}")
        print(f"📄 File {i}:")
        print(f"   • ID:      {file.id}")
        print(f"   • Status:  {file.status}")
        print(f"   • Created: {file.created_at}")

        # check attributes
        if hasattr(file, "attributes") and file.attributes:
            print(f"   • ✅ Attributes: {file.attributes}")
            has_attributes = True

            # show specific attributes
            attrs = file.attributes
            if isinstance(attrs, dict):
                print(f"      └─ visibility: {attrs.get('visibility', 'N/A')}")
                print(f"      └─ domain:     {attrs.get('domain', 'N/A')}")
                print(f"      └─ tenantId:   {attrs.get('tenantId', 'N/A')}")
        else:
            print(f"   • ❌ Attributes: (empty)")
            missing_attributes = True

        print()

    print("=" * 70)
    print("📊 Summary:")
    if has_attributes and not missing_attributes:
        print("   ✅ All files have attributes - Push is working correctly!")
    elif has_attributes and missing_attributes:
        print("   ⚠️  Some files have attributes, some don't")
        print("      (Old files may not have attributes, new ones should)")
    else:
        print("   ❌ No files have attributes - There may be an issue")

    print("=" * 70)

except Exception as e:
    import traceback

    print(f"❌ Error: {e}")
    traceback.print_exc()
