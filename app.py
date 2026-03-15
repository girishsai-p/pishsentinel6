import streamlit as st
import time
from PIL import Image
import os
import tempfile
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie

from fraud_engine import scan_text_url, compute_overall_risk, BackgroundAPKScanner
from voice_detector import scan_voice, demo_scan_voice
from qr_scanner import scan_qr, demo_scan_qr
from screenshot_detector import scan_screenshot, demo_scan_screenshot
from alert_system import send_alerts

# Mobile PWA Support metadata natively implied by Streamlit responsive views
st.set_page_config(
    page_title="PhishSentinel 3.0 - AI Cyber Fraud Shield",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lottie Animation Loader
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Custom CSS for Cyberpunk / Hackathon UI
st.markdown("""
<style>
    /* Main Background & Fonts */
    .reportview-container .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }
    
    /* Neon Headers */
    h1, h2, h3 {
        color: #00ffcc !important;
        text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffcc;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background-color: #12121c;
        border: 1px solid #00ffcc;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.6);
    }
    div[data-testid="metric-container"] > div {
        color: #e0e0e0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: transparent !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 5px !important;
        box-shadow: 0 0 5px #00ffcc;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #00ffcc !important;
        color: #0a0a0f !important;
        box-shadow: 0 0 20px #00ffcc;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1a24;
        border-radius: 5px 5px 0px 0px;
        padding: 10px 20px;
        color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ffcc !important;
        color: #0a0a0f !important;
        box-shadow: 0 0 10px #00ffcc;
        font-weight: bold;
    }

    /* Alerts / Status */
    .high-risk {
        color: #ff4b4b;
        font-weight: bold;
        text-shadow: 0 0 5px #ff4b4b;
    }
    .safe {
        color: #00fa9a;
        font-weight: bold;
        text-shadow: 0 0 5px #00fa9a;
    }
</style>
""", unsafe_allow_html=True)

st.title("PhishSentinel 3.0 - AI Cyber Fraud Shield")
st.markdown("### AI Multi-Channel Cyber Fraud Detection System")

st.sidebar.header("Control Panel")

# Load and display Lottie Animation in Sidebar (Cyber Shield)
lottie_url = "https://lottie.host/81b0a8d6-7aa6-43c3-8de7-dcafce8041a3/Zt2E2SGYB0.json"
lottie_anim = load_lottieurl(lottie_url)
if lottie_anim:
    with st.sidebar:
        st_lottie(lottie_anim, height=200, key="shield")

demo_mode = st.sidebar.toggle("Enable Hackathon Demo Mode", value=False)
st.sidebar.info("Demo mode automatically fills sample data and triggers high-risk detection.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "URL Scanner", 
    "Voice Call Scanner", 
    "QR Code Scanner", 
    "Payment Screenshot Verifier", 
    "Fraud Analytics Dashboard",
    "APK Malware Scanner"
])

def show_result(score, evidence=""):
    st.metric(label="Risk Score", value=f"{score}/100")
    if score > 80:
        st.error("[ALERT] PHISHING OPERATION DETECTED")
        if evidence:
            st.markdown(f"**Evidence:** {evidence}")
        st.error("User Protected Successfully")
        st.balloons()
        send_alerts()
    elif score < 40:
        st.success("[SAFE] GREEN: Safe. No significant threat detected.")
    else:
        st.warning("[WARNING] Medium Risk: Proceed with caution.")

with tab1:
    st.header("Email / URL Phishing Detection")
    user_input = st.text_area("Paste suspicious email text or URL:")
    
    if demo_mode:
        user_input = "upi-sbi-security.co"
        st.text_input("Demo Input:", value=user_input, disabled=True)
        
    if st.button("Scan Text/URL"):
        with st.spinner("Analyzing with BERT Multi-lingual Model..."):
            time.sleep(1)
            if demo_mode:
                score = 96
                evidence = "Suspicious phishing URL pattern matching 'upi-sbi-security.co'"
            else:
                score, evidence = scan_text_url(user_input)
            show_result(score, evidence)

with tab2:
    st.header("Voice Phishing Detection (Vishing)")
    audio_file = st.file_uploader("Upload mp3 or wav file", type=["mp3", "wav"])
    
    if demo_mode:
        st.info("Demo audio loaded.")
        
    if st.button("Scan Audio"):
        with st.spinner("Transcribing and analyzing with Whisper AI..."):
            time.sleep(1.5)
            if demo_mode:
                score, transcript = demo_scan_voice()
                st.write("**Transcript:**", transcript)
                show_result(score, "Trigger words detected: KYC, OTP, verify, bank account")
            else:
                if audio_file is not None:
                    # Save audio to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(audio_file.read())
                        tmp_path = tmp.name
                    score, transcript = scan_voice(tmp_path)
                    st.write("**Transcript:**", transcript)
                    show_result(score, transcript)
                    os.unlink(tmp_path)
                else:
                    st.warning("Please upload an audio file.")

with tab3:
    st.header("QR Code Phishing Detection (QRishing)")
    qr_image = st.file_uploader("Upload QR code image", type=["png", "jpg", "jpeg"])
    
    if demo_mode:
        st.info("Demo QR code loaded.")
        
    if st.button("Scan QR Code"):
        with st.spinner("Decoding QR code..."):
            time.sleep(1)
            if demo_mode:
                score, decoded = demo_scan_qr()
                st.write("**Decoded Data:**", decoded)
                show_result(score, "Suspicious redirect to crypto wallet.")
            else:
                if qr_image is not None:
                    image = Image.open(qr_image)
                    st.image(image, width=200)
                    score, decoded = scan_qr(image)
                    st.write("**Decoded Data:**", decoded)
                    show_result(score, decoded)
                else:
                    st.warning("Please upload a QR code image.")

with tab4:
    st.header("Fake UPI Screenshot Detection")
    ss_image = st.file_uploader("Upload Payment Screenshot", type=["png", "jpg", "jpeg"])
    
    if demo_mode:
        st.info("Demo Fake Screenshot loaded.")
        
    if st.button("Verify Transaction"):
        with st.spinner("Extracting text and verifying hashes..."):
            time.sleep(1)
            if demo_mode:
                score, text = demo_scan_screenshot()
                st.write("**Extracted Text:**", text)
                show_result(score, "Hash mismatch with bank database. Fake transaction.")
            else:
                if ss_image is not None:
                    image = Image.open(ss_image)
                    st.image(image, width=300)
                    score, text = scan_screenshot(image)
                    st.write("**Extracted Text:**", text)
                    if score > 80:
                        show_result(score, "Hash mismatch with simulated bank database.")
                    else:
                        show_result(score, "Screenshot appears valid.")
                else:
                    st.warning("Please upload a screenshot image.")

with tab5:
    st.header("Fraud Analytics Dashboard")
    st.markdown("Real-time simulation of cyber attack locations and statistics.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Threats Blocked", "1,204", "+14 today")
    col2.metric("Most Common Scam", "UPI Vishing")
    col3.metric("Average Threat Risk", "88/100", "+5% from last week")
    
    st.subheader("Live Phishing Heatmap")
    
    # Simulate fraud heatmap showing cyber attack locations
    cities = pd.DataFrame({
        'city': ['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi', 'Chennai'],
        'lat': [17.3850, 12.9716, 19.0760, 28.7041, 13.0827],
        'lon': [78.4867, 77.5946, 72.8777, 77.1025, 80.2707],
        'attacks': [500, 750, 900, 1200, 400]
    })
    
    # normalize sizes for scatterplot map
    cities['size'] = cities['attacks'] * 50
    st.map(cities, zoom=4, size='size', use_container_width=True)

with tab6:
    st.header("APK Malware Scanner")
    st.markdown("Scan Android `.apk` files against 65+ commercial Anti-Virus engines in real-time.")
    
    # Initialize the scanner in session state so it persists between renders
    if 'apk_scanner' not in st.session_state:
        st.session_state.apk_scanner = BackgroundAPKScanner()
        
    apk_file = st.file_uploader("Upload suspicious APK", type=['apk'])
    
    if demo_mode:
        st.info("Demo APK 'FakeWhatsApp_Mod.apk' loaded.")
        
    scanner = st.session_state.apk_scanner
    
    button_label = "🚀 SCAN IN BACKGROUND"
    if scanner.scan_running:
        button_label = "Scanning in progress..."
        
    if st.button(button_label, disabled=scanner.scan_running):
        if demo_mode or apk_file is not None:
             # Start background scan
             if demo_mode:
                 # Provide a dummy file name
                 scanner.start_background_scan("fake_whatsapp_mod.apk")
             else:
                 scanner.start_background_scan(apk_file)
        else:
             st.warning("Please upload an APK file or enable Demo Mode.")
             
    # Live progress bar block (if a scan is running or has finished)
    if scanner.scan_running or scanner.scan_progress > 0:
         # To update without refreshing the whole page block natively, 
         # we use st.empty() placeholders alongside st.rerun() or a small loop.
         # For this specific background task loop pattern:
         progress_bar = st.progress(scanner.scan_progress / 100)
         status_text = st.empty()
         
         if scanner.scan_running:
             # Progress loop (blocking UI update, but processing is background so main app doesn't hang forever)
             while scanner.scan_running:
                 progress_bar.progress(scanner.scan_progress / 100)
                 status_text.info(f"🔍 Analyzing... {scanner.scan_progress}%")
                 time.sleep(0.5)
                 
         # When loop breaks or if it was already finished, show 100%
         progress_bar.progress(100)
         status_text.empty() # Clear analyzing text
         
         # Result display
         if scanner.scan_result:
             if 'error' in scanner.scan_result:
                 st.error(f"Scan failed: {scanner.scan_result.get('error', 'Unknown Error')}")
             else:
                 res = scanner.scan_result
                 col1, col2 = st.columns(2)
                 with col1:
                     st.metric("Malware Detection Score", f"{res.get('malware_score', 0):.1f}%")
                     st.metric("Engines Flagged", f"{res.get('positives', 0)} / {res.get('total', 0)}")
                 with col2:
                     if res.get('malware_score', 0) > 5:
                         st.error("🚨 HIGH RISK MALWARE DETECTED 🚨")
                         st.error("⚠️ DO NOT INSTALL - This APK is malicious.")
                         st.balloons()
                     elif res.get('malware_score', 0) > 0:
                         st.warning("⚠️ SUSPICIOUS - Proceed with extreme caution.")
                     else:
                         st.success("✅ CLEAN - No threats detected.")
