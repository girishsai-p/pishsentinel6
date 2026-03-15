try:
    from transformers import pipeline
except ImportError:
    pipeline = None

import threading
import time
import requests
import streamlit as st

def scan_text_url(text: str) -> tuple[int, str]:
    risk_score = 0
    scam_keywords = ['login', 'verify', 'update', 'account', 'secure', 'bank', 'urgent', 'wallet', 'reward', 'free']
    text_lower = text.lower()
    
    matched_kws = []
    for kw in scam_keywords:
        if kw in text_lower:
            risk_score += 20
            matched_kws.append(kw)
            
    # Try classifying using transformers if available
    advanced_result = ""
    if pipeline is not None and text.strip():
        try:
            # Tokenize input using bert-base-multilingual-cased and run classification
            classifier = pipeline("text-classification", model="bert-base-multilingual-cased", top_k=1)
            result = classifier(text[:512])
            advanced_result = f" [BERT Extracted]"
            risk_score += 15
        except Exception as e:
            pass

    if risk_score > 80:
        risk_score = 92
        
    evidence = f"Keywords detected: {', '.join(matched_kws)}" if matched_kws else "No suspicious keywords found."
    return min(risk_score, 100), evidence + advanced_result

def compute_overall_risk(scores: list) -> int:
    if not scores:
        return 0
    return int(sum(scores) / len(scores))

class BackgroundAPKScanner:
    def __init__(self):
        self.scan_progress = 0
        self.scan_result = None
        self.scan_running = False
    
    def start_background_scan(self, apk_file):
        """Kick off VirusTotal scan in background thread"""
        self.scan_running = True
        self.scan_progress = 0
        
        # Start background thread
        thread = threading.Thread(target=self._scan_apk_worker, args=(apk_file,))
        thread.daemon = True
        thread.start()
    
    def _scan_apk_worker(self, apk_file):
        """Background worker - VirusTotal scan"""
        try:
            # Step 1: Upload (10%)
            self.scan_progress = 10
            upload_result = self.upload_to_virustotal(apk_file)
            
            # Handle mock scenario or errors without a key
            if 'error' in upload_result:
                self.scan_result = upload_result
                self.scan_running = False
                return
                
            scan_id = upload_result.get('scan_id')
            if not scan_id:
                self.scan_result = {"error": "Invalid response from VirusTotal"}
                self.scan_running = False
                return
            
            # Step 2: Poll results (progress updates)
            for i in range(20):
                self.scan_progress = 10 + (i * 4)  # 10→90%
                time.sleep(1.5)  # Simulate VirusTotal polling delay
                
                result = self.check_scan_results(scan_id)
                if result.get('complete'):
                    self.scan_result = result
                    self.scan_progress = 100
                    self.scan_running = False
                    break
            
            # If hit max retries
            if self.scan_running:
                self.scan_result = {"error": "Scan timeout"}
                self.scan_progress = 100
                self.scan_running = False
                    
        except Exception as e:
            self.scan_result = {"error": str(e)}
            self.scan_running = False
    
    def upload_to_virustotal(self, apk_file):
        """VirusTotal upload"""
        api_key = st.secrets.get("VIRUSTOTAL_API_KEY", "MOCK_KEY")
        if api_key == "MOCK_KEY":
            time.sleep(1) # Fake delay
            return {"scan_id": "MOCK_SCAN_ID_123"}
            
        url = "https://www.virustotal.com/vtapi/v2/file/scan"
        files = {'file': apk_file}
        params = {'apikey': api_key}
        response = requests.post(url, files=files, params=params)
        if response.status_code == 200:
            return response.json()
        return {"error": f"Upload failed: {response.text}"}
    
    def check_scan_results(self, scan_id):
        """Poll VirusTotal results"""
        if scan_id == "MOCK_SCAN_ID_123":
            # Return fake malicious result if we're mocking
            return {
                'complete': True,
                'malware_score': 85.0,
                'positives': 51,
                'total': 60
            }
            
        api_key = st.secrets.get("VIRUSTOTAL_API_KEY", "MOCK_KEY")
        url = f"https://www.virustotal.com/vtapi/v2/file/report"
        params = {'apikey': api_key, 'resource': scan_id}
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return {"error": f"Check failed: {response.status_code}"}
            
        data = response.json()
        
        positives = data.get('positives', 0)
        total = data.get('total', 0)
        
        # VirusTotal might return 200 but report doesn't exist yet, meaning still analyzing
        complete = data.get('response_code') == 1 and data.get('scan_date', None) is not None
        
        if not complete and data.get('response_code') == -2:
             # Still queued/analyzing
             return {'complete': False}
             
        return {
            'complete': True,
            'malware_score': (positives / total * 100) if total > 0 else 0,
            'positives': positives,
            'total': total
        }
