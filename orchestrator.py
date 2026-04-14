
import uuid
from models.task import Task
from agents.planner import planner_agent
from agents.executor import executor_agent
from agents.reviewer import reviewer_agent

def run_workflow(goal, context):
    task_id = f"TASK-{uuid.uuid4().hex[:6]}"

    main_task = Task(task_id, goal, context)

    # PLAN
    plan_steps = planner_agent(main_task)

    results = []

    # EXECUTE
    for step in plan_steps:
        result = executor_agent(step)
        results.append(result)

    # REVIEW
    review = reviewer_agent(results)

    return plan_steps, results, review
