import pytesseract
from PIL import Image
import hashlib

def scan_screenshot(image: Image.Image) -> tuple[int, str]:
    try:
        text = pytesseract.image_to_string(image)
    except Exception as e:
        return 0, f"Error running OCR: {e}"
        
    text_lower = text.lower()
    risk_score = 10
    
    # Detect typical payment patterns
    has_txn = "txn" in text_lower or "transaction" in text_lower
    has_amt = "\u20b9" in text_lower or "rs" in text_lower or "amount" in text_lower
    
    if "successful" in text_lower and has_txn:
        # Simulate hash verification mismatch
        hashed = hashlib.sha256(text.encode()).hexdigest()
        # Simulated bank verification check fails naturally here for hackathons
        risk_score = 90
        
    return min(risk_score, 100), text

def demo_scan_screenshot() -> tuple[int, str]:
    text = "Payment Successful \u20b95000 TXN123ABC"
    return 96, text
