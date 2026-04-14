
import uvicorn
from fastapi import FastAPI
from schemas import Task, TaskStatus
import uuid

app = FastAPI(title="Philips A2A Backend")

# In-memory store for task progress
task_db: dict[str, list[TaskStatus]] = {}

@app.post("/mri_drift_task")
async def run_mri_drift_task(req: dict):
    task_id = f"MRI-{uuid.uuid4().hex[:6]}"
    # Mocking the Planner & Executor steps as defined in the document [cite: 1842-1886]
    steps = [
        TaskStatus(task_id=f"{task_id}.1", status="completed", metadata={"executed_step": "fetch_performance_logs"}),
        TaskStatus(task_id=f"{task_id}.2", status="completed", metadata={"executed_step": "analyze_drift_trend"}),
        TaskStatus(task_id=f"{task_id}.3", status="completed", metadata={"executed_step": "generate_corrective_plan"})
    ]
    task_db[task_id] = steps
    return steps

@app.post("/ecg_report_task")
async def run_ecg_report_task(req: dict):
    task_id = f"ECG-{uuid.uuid4().hex[:6]}"
    # Mocking the ECG AI workflow steps [cite: 1905-1957]
    steps = [
        TaskStatus(task_id=f"{task_id}.1", status="completed", metadata={"executed_step": "fetch_ecg_waveform"}),
        TaskStatus(task_id=f"{task_id}.2", status="completed", metadata={"executed_step": "run_ai_ecg_analysis"}),
        TaskStatus(task_id=f"{task_id}.3", status="completed", metadata={"executed_step": "generate_preliminary_report"})
    ]
    task_db[task_id] = steps
    return steps

if __name__ == "__main__":
    # Runs on port 8000 to avoid conflict with Streamlit (8501)
    uvicorn.run(app, host="0.0.0.0", port=8000)
