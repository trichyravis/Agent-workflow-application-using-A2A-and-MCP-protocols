
import uvicorn
from fastapi import FastAPI
import uuid

app = FastAPI()

@app.post("/ecg_report_task")
async def run_ecg_report_task(req: dict):
    task_id = f"ECG-{uuid.uuid4().hex[:6]}"
    
    # We add actual content into the 'artifacts' list as per A2A standards
    return [
        {
            "task_id": f"{task_id}.1",
            "status": "completed",
            "artifacts": ["Waveform Data: 72 BPM, Normal Sinus Rhythm"],
            "metadata": {"executed_step": "fetch_ecg_waveform"}
        },
        {
            "task_id": f"{task_id}.2",
            "status": "completed",
            "artifacts": ["AI Insight: No ST-segment elevation detected. PR Interval: 160ms"],
            "metadata": {"executed_step": "run_ai_ecg_analysis"}
        },
        {
            "task_id": f"{task_id}.3",
            "status": "completed",
            "artifacts": ["PRELIMINARY REPORT: The ECG shows a normal sinus rhythm with no acute ischemic changes."],
            "metadata": {"executed_step": "generate_preliminary_report"}
        }
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
