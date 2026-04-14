
from models.task import Task

def planner_agent(main_task):
    steps = [
        Task(
            task_id=f"{main_task.task_id}.1",
            goal=main_task.goal,
            context=main_task.context,
            step="research",
            required_capabilities=["search"]
        ),
        Task(
            task_id=f"{main_task.task_id}.2",
            goal=main_task.goal,
            context=main_task.context,
            step="analysis",
            required_capabilities=["compute"]
        ),
        Task(
            task_id=f"{main_task.task_id}.3",
            goal=main_task.goal,
            context=main_task.context,
            step="review",
            required_capabilities=["review"]
        ),
    ]
    return steps
