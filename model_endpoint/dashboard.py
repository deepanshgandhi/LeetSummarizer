import streamlit as st
import requests

# Set the URL of your FastAPI logs endpoint
LOGS_URL = "http://34.125.6.114:8000/logs"

st.title("Logs Dashboard")

# Fetch logs from the FastAPI endpoint
def fetch_logs():
    try:
        response = requests.get(LOGS_URL)
        response.raise_for_status()
        logs = response.json().get("logs", "")
        return logs
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching logs: {e}")
        return ""

logs = fetch_logs()

st.text_area("Application Logs", logs, height=500)
