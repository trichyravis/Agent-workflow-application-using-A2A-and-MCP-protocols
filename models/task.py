
class Task:
    def __init__(self, task_id, goal, context=None, step=None, required_capabilities=None):
        self.task_id = task_id
        self.goal = goal
        self.context = context or {}
        self.step = step
        self.required_capabilities = required_capabilities or []


class TaskStatus:
    def __init__(self, task_id, status, artifacts=None, metadata=None):
        self.task_id = task_id
        self.status = status
        self.artifacts = artifacts or []
        self.metadata = metadata or {}
