from uuid import uuid4

from sidekick.models import Task, TaskStatus
from sidekick.planner import Planner, TaskPlan

class Orchestrator:
    def __init__(self,planner:Planner):
        self.planner = planner

    def create_task(self,user_request:str) -> tuple[Task,TaskPlan]:
        task = Task(
            task_id = str(uuid4()),
            user_request=user_request,
            status=TaskStatus.PLANNING,
        )
        plan = self.planner.create_plan(
            user_request = user_request,
            task_id = task.task_id
        )
        task.plan = [
            f"{step.tool_name}: {step.reason}"
            for step in plan.steps
        ]
        task.selected_tools = [
            step.tool_name
            for step in plan.steps
        ]
        if plan.steps:
            task.status = TaskStatus.PENDING
        else:
            task.status = TaskStatus.FAILED
            task.result = plan.summary

        return task, plan