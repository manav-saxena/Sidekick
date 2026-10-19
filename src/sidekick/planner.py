from pydantic import BaseModel, Field
from sidekick.tools import ToolRegistry

class PlanStep(BaseModel):
    
    tool_name: str
    reason: str
    arguments: dict = Field(default_factory=dict)

class TaskPlan(BaseModel):
    task_id: str
    summary: str
    steps: list[PlanStep] = Field(default_factory=list)

class Planner:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
    def create_plan(self,user_request: str, task_id:str) -> TaskPlan:
        if "emails" in user_request.lower():
            try:
                self.registry.get("search_emails")
                step = PlanStep(
                    tool_name="search_emails",
                    reason="Search emails to help with the user's request",
                    arguments={"query": user_request},
                )

                return TaskPlan(
                    task_id=task_id,
                    summary="Plan to search emails",
                    steps=[step],
                )

            except KeyError:
                pass

        return TaskPlan(
            task_id=task_id,
            summary="No matching tool found for this request",
            steps=[],
        )
                


