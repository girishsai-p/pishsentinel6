import streamlit as st

def send_alerts(message: str = "[ALERT] Fraud attempt detected. User protected."):
    # Simulate sending to Telegram / SMS
    print(f"TELEGRAM ALERT: {message}")
    print(f"SMS ALERT: {message}")
    try:
        st.toast(f"[SMS] Alert Sent: {message}")
        st.toast(f"[Telegram] Alert Sent: {message}")
    except Exception as e:
        pass
    return True
