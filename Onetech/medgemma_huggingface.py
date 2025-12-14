"""
MedGemma-4b Implementation using Hugging Face Transformers
This runs on CPU by default (set device='cpu')
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def setup_medgemma():
    """Initialize MedGemma model and tokenizer"""
    model_name = "google/medgemma-4b-it"

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print("Loading model (this may take a few minutes on first run)...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,  # Use float32 for CPU
        device_map="cpu",  # Force CPU usage
        low_cpu_mem_usage=True  # Optimize CPU memory
    )

    return model, tokenizer

def ask_medical_question(model, tokenizer, question):
    """Ask a medical question to MedGemma"""

    # Format the prompt for instruction-tuned model
    prompt = f"Question: {question}\nAnswer:"

    inputs = tokenizer(prompt, return_tensors="pt")

    print("Generating response...")
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    # Initialize model
    model, tokenizer = setup_medgemma()

    # Example medical questions
    questions = [
        "What are the common symptoms of type 2 diabetes?",
        "How does metformin work in treating diabetes?",
        "What is the difference between hypertension and hypotension?"
    ]

    print("\n" + "="*60)
    print("MedGemma Medical Q&A System")
    print("="*60 + "\n")

    # Interactive mode
    while True:
        user_question = input("\nEnter your medical question (or 'quit' to exit): ")

        if user_question.lower() in ['quit', 'exit', 'q']:
            break

        answer = ask_medical_question(model, tokenizer, user_question)
        print(f"\n{answer}\n")
        print("-"*60)
