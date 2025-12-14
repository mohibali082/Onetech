"""
MedGemma with Ollama Integration
Note: You need to import the model into Ollama first
"""

import requests
import json

def ask_ollama(prompt, model_name="medgemma"):
    """Send request to Ollama API"""
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Start it with 'ollama serve'"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("="*60)
    print("MedGemma via Ollama")
    print("="*60)
    print("\nNote: Make sure Ollama is running and MedGemma is imported")
    print("To import MedGemma into Ollama, see setup instructions below\n")

    while True:
        question = input("\nEnter your medical question (or 'quit' to exit): ")

        if question.lower() in ['quit', 'exit', 'q']:
            break

        prompt = f"Question: {question}\nAnswer:"
        answer = ask_ollama(prompt)

        print(f"\n{answer}\n")
        print("-"*60)

if __name__ == "__main__":
    main()
