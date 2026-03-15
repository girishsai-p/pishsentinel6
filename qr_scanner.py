import cv2
import numpy as np
from PIL import Image

SUSPICIOUS_WORDS = ["wallet", "crypto", "upi", "payment", "transfer", "bonus", "claim"]

def scan_qr(image: Image.Image) -> tuple[int, str]:
    img_np = np.array(image.convert('RGB'))
    # Convert to grayscale 
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(gray)
    
    if not data:
        return 0, "No QR Code found or unable to decode."
        
    data_lower = data.lower()
    risk_score = 0
    
    for word in SUSPICIOUS_WORDS:
        if word in data_lower:
            risk_score += 40
            
    if risk_score > 0:
        risk_score = max(risk_score, 85) # Immediately high risk if suspicious word found
        
    return min(risk_score, 100), data

def demo_scan_qr() -> tuple[int, str]:
    data = "crypto-wallet-payment.com"
    return 95, data
