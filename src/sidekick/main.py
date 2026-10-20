from pydantic import BaseModel, Field
from fastapi import FastAPI
from sidekick.orchestrator import Orchestrator
from sidekick.planner import Planner
from sidekick.tools import ToolRegistry,ToolDefinition
from sidekick.AI_planner import AIPlanner

app = FastAPI(title="Sidekick API")

registry = ToolRegistry()

registry.register(
    ToolDefinition(
        name = "search_emails",
        description="Search emails by sender, subject, or keywords",
        parameters={"query": "string"}
    )
)

planner = AIPlanner(registry)
orchestrator = Orchestrator(planner)

class TaskRequest(BaseModel):
    user_request: str

@app.get("/health")
def health_check():
    return {"status" : "ok"}

@app.post("/task")
def create_task(request : TaskRequest):
    task, plan = orchestrator.create_task(request.user_request)

    return {
        "task": task.model_dump(mode="json"),
        "plan": plan.model_dump(mode="json"),
    }


