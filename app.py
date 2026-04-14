
import streamlit as st
import requests
import time
import uuid
import json
from typing import Optional, Dict

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
BACKEND_URL = "http://localhost:8000"  # Change if FastAPI runs elsewhere
POLL_INTERVAL_SEC = 2                  # How often to check task status
REQUEST_TIMEOUT_SEC = 10               # HTTP request timeout

# ─────────────────────────────────────────────────────────────────────────────
# API CLIENT HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def submit_task(endpoint: str, payload: dict) -> Optional[str]:
    """Submit a task to the FastAPI backend and return the task_id."""
    try:
        res = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=REQUEST_TIMEOUT_SEC)
        res.raise_for_status()
        data = res.json()
        # Backend may return task_id in response or we fall back to payload
        return data.get("task_id") or payload.get("task_id")
    except requests.RequestException as e:
        st.error(f"🚨 Failed to submit task: {e}")
        return None

def fetch_status(task_id: str) -> Optional[Dict]:
    """Poll the backend for the latest task status."""
    try:
        res = requests.get(f"{BACKEND_URL}/status/{task_id}", timeout=REQUEST_TIMEOUT_SEC)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        st.warning(f"⚠️ Could not fetch status for `{task_id}`: {e}")
        return None

def poll_until_terminal(task_id: str, status_box: st.empty) -> Optional[Dict]:
    """Block until task reaches a terminal state (completed/failed)."""
    with st.status(f"🔄 Executing workflow `{task_id}`...", expanded=True) as status:
        while True:
            data = fetch_status(task_id)
            if not data:
                status.error("Failed to retrieve status. Check backend connectivity.")
                return None

            current_status = data.get("status", "unknown")
            status.update(label=f"🔄 Status: `{current_status}` | Artifacts: {len(data.get('artifacts', []))}")

            if current_status in ("completed", "failed", "cancelled"):
                status.update(state="complete" if current_status == "completed" else "error")
                return data

            time.sleep(POLL_INTERVAL_SEC)

# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Philips Agentic Workflow Console", layout="wide")
st.title("🏥 Philips A2A + MCP Workflow Console")
st.markdown("""
Select a clinical workflow, configure parameters, and monitor the multi-agent execution. 
All orchestration, A2A handoffs, and MCP tool calls are handled by the FastAPI backend.
""")

# Initialize session state
if "current_task_id" not in st.session_state:
    st.session_state.current_task_id = None
if "task_result" not in st.session_state:
    st.session_state.task_result = None

# ─────────────────────────────────────────────────────────────────────────────
# WORKFLOW FORMS
# ─────────────────────────────────────────────────────────────────────────────
with st.form("workflow_form", clear_on_submit=False):
    workflow = st.selectbox("Select Workflow", [
        "Generic Task", 
        "MRI Performance Drift", 
        "ECG Report Automation", 
        "Custom JSON"
    ])

    goal, context_json = "", "{}"

    if workflow == "Generic Task":
        goal = st.text_input("Goal", "Analyze system logs and summarize findings")
        context_json = st.text_area("Context (JSON)", '{"environment": "prod", "priority": "high"}')

    elif workflow == "MRI Performance Drift":
        goal = "Investigate MRI performance drift and propose corrective actions"
        col1, col2 = st.columns(2)
        with col1:
            device_id = st.text_input("Device ID", "MRI-2026-0789")
            alert_type = st.text_input("Alert Type", "performance_drift")
        with col2:
            hospital = st.text_input("Hospital", "Hospital-X")
            priority = st.selectbox("Priority", ["low", "medium", "high"])
        context = {"device_id": device_id, "hospital": hospital, "alert_type": alert_type, "priority": priority}
        context_json = json.dumps(context, indent=2)

    elif workflow == "ECG Report Automation":
        goal = "Automate ECG report generation with AI analysis and clinical rules"
        col1, col2 = st.columns(2)
        with col1:
            ecg_id = st.text_input("ECG ID", "ECG-2026-0456")
            patient_id = st.text_input("Patient ID", "Patient-1122")
        with col2:
            hospital = st.text_input("Hospital", "Hospital-Y")
            priority = st.selectbox("Priority", ["routine", "urgent"])
        context = {"ecg_id": ecg_id, "patient_id": patient_id, "hospital": hospital, "priority": priority}
        context_json = json.dumps(context, indent=2)

    else:  # Custom JSON
        context_json = st.text_area("Raw Task JSON (must include 'goal' and 'context')", 
                                    '{"goal": "Custom task", "context": {}}', height=150)

    submitted = st.form_submit_button("🚀 Submit Workflow")

if submitted:
    try:
        payload = json.loads(context_json)
        # Ensure goal is attached (for non-custom workflows)
        if workflow != "Custom JSON":
            payload["goal"] = goal
        
        # Generate unique task ID
        task_id = f"{workflow.replace(' ', '_').lower()}-{uuid.uuid4().hex[:8]}"
        payload["task_id"] = task_id

        # Map to FastAPI endpoints defined in your architecture doc
        endpoint_map = {
            "Generic Task": "/task",
            "MRI Performance Drift": "/mri_drift_task",
            "ECG Report Automation": "/ecg_report_task",
            "Custom JSON": "/task"
        }
        endpoint = endpoint_map.get(workflow, "/task")

        st.session_state.current_task_id = submit_task(endpoint, payload)
        if st.session_state.current_task_id:
            st.success(f"✅ Workflow submitted! Task ID: `{st.session_state.current_task_id}`")

    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format in context. Please check syntax.")

# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS & RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.current_task_id:
    st.divider()
    st.header("📊 Execution Progress & Results")
    
    col_ctrl, col_info = st.columns([1, 4])
    with col_ctrl:
        st.write(f"**Active Task:** `{st.session_state.current_task_id}`")
        if st.button("⏹️ Clear Task"):
            st.session_state.current_task_id = None
            st.session_state.task_result = None
            st.rerun()

    with col_info:
        # Polling block
        result = poll_until_terminal(st.session_state.current_task_id, st.empty())
        
        if result:
            st.session_state.task_result = result
            status = result.get("status", "unknown")
            
            if status == "completed":
                st.success("✅ Task Completed Successfully")
                st.json(result)
                if result.get("artifacts"):
                    st.subheader("📄 Generated Artifacts")
                    for art in result["artifacts"]:
                        st.code(art)
                        
            elif status == "failed":
                st.error("❌ Task Failed")
                st.json(result.get("metadata", {}))

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR: TRACK EXISTING TASK
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.subheader("🔍 Track Existing Task")
existing_id = st.sidebar.text_input("Task ID")
if st.sidebar.button("📥 Track Task"):
    if existing_id.strip():
        st.session_state.current_task_id = existing_id.strip()
        st.session_state.task_result = None
        st.rerun()
