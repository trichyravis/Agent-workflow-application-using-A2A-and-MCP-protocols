
import streamlit as st
import requests
import time

# Ensure this matches your FastAPI port (usually 8000)
BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Philips Agentic Workflow", layout="wide", page_icon="🩺")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stCard { border-radius: 10px; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 Philips Agentic Workflow Console")
st.sidebar.image("https://www.philips.com/content/dam/philips/global/corporate/philips-logo.png", width=150)

# Sidebar - A2A Mode Selection
mode = st.sidebar.selectbox("Workflow Module", ["ECG Report Automation", "MRI Performance Drift"])

if mode == "ECG Report Automation":
    st.header("ECG AI-Assisted Report Generation")
    
    col1, col2 = st.columns(2)
    with col1:
        ecg_id = st.text_input("ECG ID", value="ECG-5a24db")
    with col2:
        patient_id = st.text_input("Patient ID", value="P-9901")

    if st.button("🚀 Generate AI Report"):
        with st.status("Orchestrating Agents (A2A Protocol)...", expanded=True) as status:
            try:
                # 1. Trigger the workflow
                payload = {"goal": "Automate ECG report", "context": {"ecg_id": ecg_id, "patient_id": patient_id}}
                res = requests.post(f"{BASE_URL}/ecg_report_task", json=payload, timeout=10)
                
                if res.status_code == 200:
                    task_steps = res.json()
                    
                    # 2. Display steps as a timeline
                    st.write("### Agent Execution Trace")
                    for i, step in enumerate(task_steps):
                        st.write(f"**Step {i+1}: {step['metadata']['executed_step'].replace('_', ' ').title()}**")
                        st.caption(f"Task ID: {step['task_id']} | Status: ✅ {step['status']}")
                        
                    status.update(label="Report Generation Complete!", state="complete", expanded=False)
                    st.success(f"Final Report ready for {ecg_id}")
                    
                    # 3. Final Artifact Presentation
                    with st.expander("View Full Detailed Logs (JSON)"):
                        st.json(task_steps)
                else:
                    st.error(f"Backend Error: {res.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: The FastAPI backend (main.py) is not running or unreachable.")

elif mode == "MRI Performance Drift":
    st.info("MRI Module Loaded. Ready for input.")
