
import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Philips A2A Console", layout="wide")

st.title("🩺 Philips Agentic Workflow Console")

ecg_id = st.text_input("ECG ID", value="ECG-199566")
patient_id = st.text_input("Patient ID", value="P-9901")

if st.button("🚀 Generate AI Report"):
    try:
        res = requests.post(f"{BASE_URL}/ecg_report_task", json={"goal": "Automate ECG", "context": {"id": ecg_id}})
        
        if res.status_code == 200:
            steps = res.json()
            
            # --- AGENT TRACE SECTION ---
            st.subheader("Agent Execution Trace")
            cols = st.columns(len(steps))
            for i, step in enumerate(steps):
                with cols[i]:
                    st.success(f"**{step['metadata']['executed_step'].replace('_', ' ').title()}**")
                    st.caption(f"Status: {step['status']}")

            # --- CLINICAL REPORT SECTION ---
            st.divider()
            st.subheader("📋 Preliminary Clinical Report")
            
            # Extract the final artifact from the last step
            final_report_text = steps[-1]['artifacts'][0] 
            
            st.info(final_report_text)
            
            # Add a mock "Sign Off" button for the clinician
            col_a, col_b = st.columns([1, 4])
            with col_a:
                if st.button("Approve & Sign"):
                    st.balloons()
                    st.success("Report pushed to EMR")
            
            with st.expander("Technical Trace (A2A JSON)"):
                st.json(steps)
                
    except Exception as e:
        st.error(f"Connection Error: Ensure your backend is running. {e}")
