
import streamlit as st
import json
from orchestrator import run_workflow

st.set_page_config(page_title="Agent Workflow System", layout="wide")

st.title("🤖 Agent Workflow System (A2A Style)")

st.sidebar.header("⚙️ Input")

goal = st.sidebar.text_input(
    "Goal",
    "Check eligibility for adjunct faculty role"
)

context_text = st.sidebar.text_area(
    "Context (JSON)",
    '{"citizenship": "Indian", "visa": "None"}'
)

run = st.sidebar.button("🚀 Run Workflow")

if run:
    try:
        context = json.loads(context_text)
    except:
        context = {}

    st.subheader("📋 Execution Flow")

    plan, results, review = run_workflow(goal, context)

    st.markdown("### 🧠 Planner Output")
    for step in plan:
        st.write(f"Step: {step.step} | Capability: {step.required_capabilities}")

    st.markdown("### ⚙️ Executor Output")
    for res in results:
        st.json({
            "task_id": res.task_id,
            "status": res.status,
            "artifacts": res.artifacts
        })

    st.markdown("### 🔍 Reviewer Output")
    st.write(review)
