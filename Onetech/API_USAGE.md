# MedGemma API Usage Guide

## Starting the API Server

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
**GET /**

```bash
curl http://localhost:8000/
```

### 2. Health Check
**GET /health**

```bash
curl http://localhost:8000/health
```

### 3. Ask Medical Question (Main Endpoint)
**POST /ask**

**Simple Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What are the symptoms of diabetes?\"}"
```

**With Custom Parameters:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"How does insulin work in the human body?\",
    \"max_tokens\": 300,
    \"temperature\": 0.8,
    \"top_p\": 0.95
  }"
```

**Windows PowerShell (Escape quotes):**
```powershell
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{\"question\": \"What are the symptoms of diabetes?\"}'
```

**Windows CMD:**
```cmd
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"What are the symptoms of diabetes?\"}"
```

### 4. Batch Questions
**POST /batch**

```bash
curl -X POST "http://localhost:8000/batch" \
  -H "Content-Type: application/json" \
  -d "[
    \"What is hypertension?\",
    \"How does aspirin work?\",
    \"What are the symptoms of pneumonia?\"
  ]"
```

## Example Questions to Try

```bash
# Question about disease symptoms
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What are the common symptoms of type 2 diabetes?\"}"

# Question about medication
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"How does metformin work in treating diabetes?\"}"

# Question about anatomy
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Explain the function of the pancreas\"}"

# Question about differences
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is the difference between bacteria and viruses?\"}"

# Question about procedures
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What happens during a CT scan?\"}"
```

## Response Format

**Success Response:**
```json
{
  "question": "What are the symptoms of diabetes?",
  "answer": "Common symptoms include increased thirst, frequent urination, extreme fatigue...",
  "model": "google/medgemma-4b-it"
}
```

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

## Testing with Python

```python
import requests

url = "http://localhost:8000/ask"
data = {
    "question": "What are the symptoms of diabetes?",
    "max_tokens": 512,
    "temperature": 0.7
}

response = requests.post(url, json=data)
print(response.json())
```

## Testing with JavaScript (Node.js)

```javascript
const axios = require('axios');

async function askQuestion() {
  const response = await axios.post('http://localhost:8000/ask', {
    question: 'What are the symptoms of diabetes?',
    max_tokens: 512,
    temperature: 0.7
  });

  console.log(response.data);
}

askQuestion();
```

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Parameters Explanation

- **question** (required): Your medical question as a string
- **max_tokens** (optional, default: 512): Maximum length of the response
- **temperature** (optional, default: 0.7): Controls randomness (0.0 = deterministic, 1.0 = very random)
- **top_p** (optional, default: 0.9): Controls diversity of response

## Performance Notes

- First request will be slower (model initialization)
- CPU inference: expect 2-10 seconds per response
- Batch endpoint processes questions sequentially
- Maximum 10 questions per batch request

## Troubleshooting

**Connection Refused:**
- Make sure the server is running: `python app.py`
- Check if port 8000 is available

**503 Model Not Loaded:**
- Wait for model to finish loading on startup
- Check server logs for errors

**Slow Responses:**
- Normal on CPU (2-10 seconds)
- Consider reducing max_tokens
- Consider using GPU if available
