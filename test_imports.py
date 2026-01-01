import sys
print("=== Python Environment Info ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[0:3]}")

print("\n=== Testing LangChain Imports ===")
try:
    import langchain_core
    print("✅ langchain_core found at:", langchain_core.__file__)
except ImportError as e:
    print("❌ langchain_core NOT FOUND")
    print(f"   Error: {e}")

try:
    import langchain_openai
    print("✅ langchain_openai found")
except ImportError as e:
    print("❌ langchain_openai NOT FOUND")

try:
    from langchain_prompts import DATE_ASSISTANT_SYSTEM_PROMPT
    print("✅ langchain_prompts found")
except ImportError as e:
    print("❌ langchain_prompts NOT FOUND")
    print(f"   Error: {e}")
