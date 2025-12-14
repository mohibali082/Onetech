# MedGemma-4b Medical AI Assistant

## Overview
This project uses Google's MedGemma-4b model for medical question answering.

## Setup Instructions

### Option 1: Hugging Face (Recommended for beginners)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python medgemma_huggingface.py
```

**Note**: First run will download ~8GB model. Subsequent runs are faster.

### Option 2: Ollama

1. Install Ollama from https://ollama.ai

2. Pull a compatible model or import MedGemma:
```bash
# Ollama doesn't have MedGemma built-in yet
# You can use a similar medical model or import manually
ollama pull meditron
```

3. Run Ollama server:
```bash
ollama serve
```

4. Run the script:
```bash
python medgemma_ollama.py
```

## System Requirements

### CPU Usage:
- **RAM**: Minimum 16GB recommended for 4B model
- **Storage**: ~8GB for model weights
- **Performance**: Expect 2-10 seconds per response on modern CPU

### GPU Usage (Optional):
To use GPU, modify `medgemma_huggingface.py`:
```python
device_map="auto"  # Instead of "cpu"
torch_dtype=torch.float16  # Instead of float32
```

## Example Questions

- "What are the symptoms of pneumonia?"
- "How does aspirin work?"
- "What is the difference between bacteria and viruses?"
- "Explain how vaccines provide immunity"

## Important Disclaimers

⚠️ **This is for educational purposes only**
- Not a substitute for professional medical advice
- Always consult healthcare professionals for medical decisions
- Model responses should be verified with medical literature

## Performance Tips

1. **First run is slow**: Model downloads ~8GB
2. **CPU optimization**: Close other applications
3. **Batch questions**: Reuse loaded model for multiple queries
4. **Consider cloud GPU**: Google Colab free tier if CPU too slow
