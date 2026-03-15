# PhishSentinel 3.0 \u2013 AI Multi-Channel Cyber Fraud Detection System

PhishSentinel 3.0 is a professional AI-powered cybersecurity web application that detects modern phishing and fraud attacks from multiple sources including text, voice, QR codes, and fake payment screenshots.

## Features

1. **Email / URL Phishing Detection:** Uses BERT multilingual model to classify phishing text/URLs.
2. **Voice Phishing Detection (Vishing):** Uses Whisper speech recognition to transcribe and scan audio for fraud keywords.
3. **QR Code Phishing Detection (QRishing):** Decodes QR codes and scans for suspicious links.
4. **Fake UPI Screenshot Detection:** Uses Pytesseract OCR and SHA256 hashing to verify transaction records.
5. **Multi-Threat Risk Engine:** Combines scores from different vectors to dynamically evaluate overall threat levels.
6. **Fraud Analytics Dashboard:** Visualizes attack attempts on a real-time heatmap.
7. **Cross-Platform Alert System:** Simulates Telegram & SMS rapid alerting.
8. **Hackathon Demo Mode:** Provides pre-loaded mock data to simulate high-risk alerts for quick evaluation.

## Installation

1. Clone the repository.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application locally:
   ```bash
   streamlit run app.py
   ```

## Mobile PWA Support
This project features a responsive interface optimized for mobile usage. You can load the Streamlit application on any modern smartphone browser and use the `Add to Home Screen` option to install it as a PWA-like native web application.

## Cloud Deployment (Vercel)
A `vercel.json` file is provided to allow deployment through Vercel Serverless Functions.
