
import streamlit as st
import requests
import time
import uuid
import json
from typing import Dict

BASE_URL = "http://localhost:8000"  # Your FastAPI backend address

st.set_page_config(page_title="A2A Agent Workflow UI", layout="wide")
st.title("Philips Agentic Workflow Console")

# Sidebar for use case selection
use_case = st.sidebar.selectbox(
    "Select Workflow",
    ["MRI Performance Drift", "ECG Report Automation"]
)

# UI for MRI Performance Drift
if use_case == "MRI Performance Drift":
    st.header("MRI Performance Drift Investigation")
    device_id = st.text_input("Device ID", "MRI-2026-0789")
    hospital = st.text_input("Hospital", "Hospital-X")
    priority = st.selectbox("Priority", ["low", "medium", "high"])

    if st.button("Run MRI Workflow"):
        context = {"device_id": device_id, "hospital": hospital, "priority": priority}
        res = requests.post(
            f"{BASE_URL}/mri_drift_task",
            json={"goal": "Investigate MRI performance drift", "context": context}
        )
        if res.status_code == 200:
            st.session_state.statuses = res.json()
            st.success("Workflow completed!")
        else:
            st.error(f"Error: {res.status_code}")

# Displaying Results/Progress
if "statuses" in st.session_state:
    st.subheader("Workflow Execution Trace")
    for step in st.session_state.statuses:
        with st.expander(f"Step: {step.get('metadata', {}).get('executed_step', 'Task')}"):
            st.json(step)
