import streamlit as st
import requests
from ast import literal_eval

# Set the URL of your FastAPI logs endpoint
LOGS_URL = "http://34.125.6.114:8000/logs"

st.title("Logs Dashboard")

# Fetch logs from the FastAPI endpoint
def fetch_logs():
    try:
        response = requests.get(LOGS_URL)
        response.raise_for_status()
        logs = response.text
        return literal_eval(logs)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching logs: {e}")
        return ""

logs = fetch_logs()

# Replace "\n" with "  \n" for markdown line break
logs_formatted = logs.replace("\n", "  \n")

# Display logs in a markdown text area
st.markdown(f"**Application Logs:**  \n{logs_formatted}")

