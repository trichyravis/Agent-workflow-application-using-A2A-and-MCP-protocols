
from typing import List, Optional, Dict
from pydantic import BaseModel

class Task(BaseModel):
    task_id: str
    goal: str
    context: Dict[str, str] = {}
    step: Optional[str] = None
    required_capabilities: List[str] = []

class TaskStatus(BaseModel):
    task_id: str
    status: str   # "pending", "running", "completed", "failed"
    artifacts: List[str] = []
    metadata: Dict[str, str] = {}
