import os
from transformers import AutoTokenizer

# Set token
os.environ['HF_TOKEN'] = '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'
token = os.getenv('HF_TOKEN')

print("Testing actual model file download...")
print(f"Using token: {token[:10]}...\n")

try:
    print("Attempting to download tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("google/medgemma-4b-it", token=token)
    print("[SUCCESS] Tokenizer downloaded successfully!")
    print("You have full access to the MedGemma model!")
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {str(e)[:200]}")
    print("\n=== ACTION REQUIRED ===")
    print("You need to request access to download the model:")
    print("1. Visit: https://huggingface.co/google/medgemma-4b-it")
    print("2. Make sure you're logged in")
    print("3. Click 'Request Access' or 'Agree and Access'")
    print("4. Wait for approval (usually instant if you accept terms)")
    print("5. After approval, regenerate your access token")
