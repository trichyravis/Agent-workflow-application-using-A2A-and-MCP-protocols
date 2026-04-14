
import streamlit as st
import requests
import json
import uuid

# Configuration - BASE_URL points to the FastAPI A2A Backend
# If running locally, this is typically http://localhost:8000
BASE_URL = "http://localhost:8000" 

st.set_page_config(page_title="Philips A2A Agent Console", layout="wide")
st.title("Philips Agentic Workflow Console")

# Sidebar for Use Case Selection [cite: 2015-2018]
use_case = st.sidebar.selectbox(
    "Select Workflow",
    ["MRI Performance Drift", "ECG Report Automation"]
)

if use_case == "MRI Performance Drift":
    st.header("MRI Performance Drift Investigation")
    
    # User Inputs based on MRI Task Schema [cite: 1831-1839, 2021-2024]
    device_id = st.text_input("Device ID", "MRI-2026-0789")
    hospital = st.text_input("Hospital", "Hospital-X")
    priority = st.selectbox("Priority", ["low", "medium", "high"])

    if st.button("Run MRI Workflow"):
        # Context object following A2A task schema [cite: 1828-1841]
        context = {
            "device_id": device_id,
            "hospital": hospital,
            "alert_type": "performance_drift",
            "priority": priority
        }
        
        with st.spinner("Orchestrating A2A Agents..."):
            try:
                # Call the specific FastAPI endpoint for MRI [cite: 1979-1982, 2033-2035]
                res = requests.post(
                    f"{BASE_URL}/mri_drift_task",
                    json={
                        "goal": f"Investigate {device_id} at {hospital} showing drift",
                        "context": context
                    },
                    timeout=15
                )
                
                if res.status_code == 200:
                    statuses = res.json()
                    st.success("Workflow successfully orchestrated!")
                    
                    # Display the execution trace/artifacts [cite: 2040-2041, 2065-2066]
                    st.subheader("Agent Execution Progress")
                    for step in statuses:
                        with st.expander(f"Step: {step.get('metadata', {}).get('executed_step', 'Unknown')}"):
                            st.json(step)
                else:
                    st.error(f"Backend error: {res.status_code} - {res.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to the A2A Backend at {BASE_URL}. Is main.py running?")

elif use_case == "ECG Report Automation":
    st.header("ECG Report Automation (AI-Assisted)")
    ecg_id = st.text_input("ECG ID", "ECG-2026-0456")
    patient_id = st.text_input("Patient ID", "Patient-1122")
    
    if st.button("Generate ECG Report"):
        # ECG Context [cite: 1892-1904, 2051-2056]
        context = {"ecg_id": ecg_id, "patient_id": patient_id}
        
        with st.spinner("Executing AI Analysis..."):
            res = requests.post(
                f"{BASE_URL}/ecg_report_task",
                json={"goal": "Automate ECG report", "context": context}
            )
            if res.status_code == 200:
                st.json(res.json())
