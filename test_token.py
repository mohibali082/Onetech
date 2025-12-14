import os
from huggingface_hub import HfApi

# Set token
os.environ['HF_TOKEN'] = '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'
token = os.getenv('HF_TOKEN')

print(f"Token found: {token[:10]}...")

# Test if we can access the model
api = HfApi()
try:
    model_info = api.model_info("google/medgemma-4b-it", token=token)
    print("[SUCCESS] You have access to the MedGemma model!")
    print(f"Model: {model_info.id}")
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nYou need to:")
    print("1. Go to: https://huggingface.co/google/medgemma-4b-it")
    print("2. Click 'Request Access'")
    print("3. Wait for approval")
