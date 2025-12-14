"""
Medical Report Generator using Gemini 2.5 Flash
Generates medical referral letters from doctor-patient conversations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import base64
import tempfile
import os
import json
import whisper
import google.generativeai as genai
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCzxtIMqkcws2s8VLuZiK1QVpAVZBRLIAU"
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(
    title="Medical Report Generator API",
    description="Generate medical referral letters from doctor-patient conversations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
whisper_model = None
gemini_model = None
template_data = None

class AudioRequest(BaseModel):
    audio_base64: str
    template_type: str = "referral_letter"

class ReportResponse(BaseModel):
    transcribed_text: str
    medical_report: str
    timestamp: str

@app.on_event("startup")
async def load_models():
    """Load models and template on startup"""
    global whisper_model, gemini_model, template_data

    try:
        # Load Whisper model
        logger.info("Loading Whisper model for speech recognition...")
        whisper_model = whisper.load_model("base")
        logger.info("Whisper model loaded successfully!")

        # Initialize Gemini model
        logger.info("Initializing Gemini 2.5 Flash model...")
        gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        logger.info("Gemini model initialized successfully!")

        # Load template
        logger.info("Loading report template...")
        with open("template.json", "r") as f:
            template_data = json.load(f)
        logger.info("Template loaded successfully!")

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Medical Report Generator API",
        "version": "1.0.0",
        "endpoints": {
            "POST /generate-report": "Generate medical report from audio",
            "GET /health": "Check API health status",
            "GET /docs": "API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if whisper_model is None or gemini_model is None or template_data is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    return {
        "status": "healthy",
        "whisper_model": "base",
        "gemini_model": "gemini-2.5-flash",
        "template_loaded": template_data is not None
    }

@app.get("/templates")
async def get_templates():
    """Get available report templates"""
    if template_data is None:
        raise HTTPException(status_code=503, detail="Templates not loaded")

    return {
        "templates": {
            key: {"name": value["name"]}
            for key, value in template_data['templates'].items()
        }
    }

@app.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: AudioRequest):
    """
    Generate medical report from doctor-patient conversation audio

    Parameters:
    - audio_base64: Base64 encoded audio file of the conversation

    Returns:
    - transcribed_text: The transcribed conversation
    - medical_report: The generated medical referral letter
    - timestamp: When the report was generated
    """

    if whisper_model is None or gemini_model is None or template_data is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    if not request.audio_base64:
        raise HTTPException(status_code=400, detail="Audio data cannot be empty")

    # Validate template type
    if request.template_type not in template_data['templates']:
        raise HTTPException(status_code=400, detail=f"Invalid template type. Available: {list(template_data['templates'].keys())}")

    try:
        logger.info(f"Processing audio for medical report generation using template: {request.template_type}")

        # Get selected template
        selected_template = template_data['templates'][request.template_type]

        # Step 1: Decode base64 audio
        audio_bytes = base64.b64decode(request.audio_base64)

        # Step 2: Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_path = temp_audio_file.name

        try:
            # Step 3: Transcribe audio using Whisper
            logger.info("Transcribing audio...")
            result = whisper_model.transcribe(temp_audio_path)
            transcribed_text = result["text"].strip()
            logger.info(f"Transcription complete: {len(transcribed_text)} characters")

            if not transcribed_text:
                raise HTTPException(status_code=400, detail="Could not transcribe audio")

            # Step 4: Generate report using Gemini
            logger.info("Generating medical report with Gemini...")

            # Create the prompt with system instructions and template
            prompt = f"""{selected_template['system_prompt']}

TEMPLATE:
{selected_template['template']}

CONVERSATION TRANSCRIPT:
{transcribed_text}

Generate a medical report based on the conversation above. Follow the template exactly and only include information explicitly mentioned in the transcript. Replace [Today's Date] with {datetime.now().strftime('%B %d, %Y')}."""

            # Generate report with Gemini
            response = gemini_model.generate_content(prompt)
            medical_report = response.text.strip()

            logger.info("Medical report generated successfully")

            return ReportResponse(
                transcribed_text=transcribed_text,
                medical_report=medical_report,
                timestamp=datetime.now().isoformat()
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
