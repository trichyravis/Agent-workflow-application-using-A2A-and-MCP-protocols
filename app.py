
import streamlit as st
import requests

BASE_URL = "http://localhost:8000"
st.set_page_config(page_title="Philips Agentic Console", layout="wide")
st.title("🩺 Philips Agentic Workflow Console")

use_case = st.sidebar.selectbox("Select Workflow", ["MRI Performance Drift", "ECG Report Automation"])

if use_case == "MRI Performance Drift":
    st.header("MRI Performance Drift Investigation")
    device_id = st.text_input("Device ID", "MRI-2026-0789")
    hospital = st.text_input("Hospital", "Hospital-X")
    
    if st.button("Run MRI Workflow"):
        payload = {"goal": "Investigate drift", "context": {"device_id": device_id, "hospital": hospital}}
        res = requests.post(f"{BASE_URL}/mri_drift_task", json=payload)
        if res.status_code == 200:
            st.success("Workflow Complete")
            st.json(res.json())

elif use_case == "ECG Report Automation":
    st.header("ECG AI-Assisted Report")
    ecg_id = st.text_input("ECG ID", "ECG-2026-0456")
    
    if st.button("Generate Report"):
        payload = {"goal": "Automate report", "context": {"ecg_id": ecg_id}}
        res = requests.post(f"{BASE_URL}/ecg_report_task", json=payload)
        if res.status_code == 200:
            st.success("Report Generated")
            st.json(res.json())
