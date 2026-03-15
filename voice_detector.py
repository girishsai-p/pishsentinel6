import os

try:
    import whisper
except ImportError:
    whisper = None

KEYWORDS = ["otp", "kyc", "upi", "bank", "verify", "account blocked", "urgent", "transfer"]

def scan_voice(audio_path: str) -> tuple[int, str]:
    if whisper is None:
        return 0, "Whisper model not found. Check requirements."
        
    try:
        # For hackathon/demo performance, using 'tiny' model.
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        transcript = result["text"]
    except Exception as e:
        transcript = f"Error transcribing audio: {e}"
        return 0, transcript
        
    transcript_lower = transcript.lower()
    risk_score = 0
    
    for kw in KEYWORDS:
        if kw in transcript_lower:
            risk_score += 30
            
    return min(risk_score, 100), transcript

def demo_scan_voice() -> tuple[int, str]:
    transcript = "Sir your KYC expired please share OTP to verify your bank account"
    risk_score = 96
    return risk_score, transcript
