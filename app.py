
import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Philips A2A Console", layout="wide")
st.title("🩺 Philips Agentic Workflow Console")

# Sidebar for use case selection
use_case = st.sidebar.selectbox("Select Workflow", ["ECG Report Automation", "MRI Performance Drift"])

if use_case == "ECG Report Automation":
    st.header("ECG Report Automation (AI-assisted)")
    ecg_id = st.text_input("ECG ID", "ECG-2026-0456")
    patient_id = st.text_input("Patient ID", "Patient-1122")

    if st.button("Generate ECG Report Draft"):
        context = {"ecg_id": ecg_id, "patient_id": patient_id}

        try:
            # Call backend orchestrator
            res = requests.post(
                f"{BASE_URL}/ecg_report_task",
                json={"goal": "Automate ECG report", "context": context},
                timeout=10
            )

            if res.status_code == 200:
                statuses = res.json()
                st.success("Workflow completed successfully.")

                # Render the execution trace
                for step in statuses:
                    with st.expander(f"Step: {step['metadata']['executed_step'].replace('_', ' ').title()}"):
                        st.write(f"**Status:** {step['status']}")
                        if step['artifacts']:
                            st.info(f"**Artifact:** {step['artifacts'][0]}")
            else:
                st.error(f"Backend error: {res.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to backend at {BASE_URL}. Ensure main-2.py is running.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
