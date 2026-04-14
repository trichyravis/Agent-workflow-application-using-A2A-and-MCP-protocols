
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Task(BaseModel):
    task_id: str
    goal: str
    context: Dict[str, str] = Field(default_factory=dict)
    plan_json: Optional[str] = None
    step: Optional[str] = None
    required_capabilities: List[str] = Field(default_factory=list)

class TaskStatus(BaseModel):
    task_id: str
    status: str
    artifacts: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)
