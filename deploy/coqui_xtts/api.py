"""
Coqui XTTS v2 - FastAPI Server for Voice Cloning TTS
Endpoints:
  POST /tts - Generate speech from text
  GET /health - Health check
"""

import os
import tempfile
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from TTS.api import TTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Coqui XTTS v2 API", version="1.0.0")

# Initialize TTS model (loads on startup)
logger.info("Loading XTTS v2 model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
logger.info("✅ Model loaded successfully!")

# Directory for uploaded reference voices
VOICES_DIR = Path("/app/voices")
VOICES_DIR.mkdir(exist_ok=True)


class TTSRequest(BaseModel):
    text: str
    language: str = "pt"  # Default to Portuguese
    speaker_wav: Optional[str] = None  # Path to reference voice (optional)


@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers."""
    return {"status": "healthy", "model": "xtts_v2"}


@app.post("/tts")
async def generate_speech(
    text: str = Form(...),
    language: str = Form("pt"),
    speaker_wav_file: Optional[UploadFile] = File(None)
):
    """
    Generate speech from text with optional voice cloning.
    
    Args:
        text: Text to synthesize
        language: Language code (pt, en, es, fr, de, it, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko, hi)
        speaker_wav_file: Reference voice audio file (optional, for voice cloning)
    
    Returns:
        WAV audio file
    """
    try:
        logger.info(f"TTS request: '{text[:50]}...' (lang: {language})")
        
        # Handle reference voice upload
        speaker_wav_path = None
        if speaker_wav_file:
            # Save uploaded file temporarily
            temp_ref = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_ref.write(await speaker_wav_file.read())
            temp_ref.close()
            speaker_wav_path = temp_ref.name
            logger.info(f"Using uploaded reference voice: {speaker_wav_file.filename}")
        
        # Generate speech
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker_wav_path,
            language=language
        )
        
        logger.info(f"✅ Speech generated: {output_path}")
        
        # Clean up reference voice temp file
        if speaker_wav_path and os.path.exists(speaker_wav_path):
            os.remove(speaker_wav_path)
        
        # Return audio file
        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename=f"speech_{hash(text)}.wav"
        )
    
    except Exception as e:
        logger.error(f"❌ TTS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload_reference_voice")
async def upload_reference_voice(
    voice_name: str = Form(...),
    voice_file: UploadFile = File(...)
):
    """
    Upload a reference voice for future use.
    
    Args:
        voice_name: Name identifier for this voice (e.g., "epic_narrator")
        voice_file: WAV audio file (6-30 seconds recommended)
    
    Returns:
        Confirmation with voice name
    """
    try:
        voice_path = VOICES_DIR / f"{voice_name}.wav"
        
        with open(voice_path, "wb") as f:
            f.write(await voice_file.read())
        
        logger.info(f"✅ Reference voice saved: {voice_name}")
        
        return {
            "status": "success",
            "voice_name": voice_name,
            "path": str(voice_path)
        }
    
    except Exception as e:
        logger.error(f"❌ Upload Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/voices")
async def list_voices():
    """List all uploaded reference voices."""
    voices = [v.stem for v in VOICES_DIR.glob("*.wav")]
    return {"voices": voices}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
