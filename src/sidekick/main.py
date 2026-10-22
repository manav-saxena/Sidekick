from pydantic import BaseModel, Field
from fastapi import FastAPI , HTTPException
from sidekick.orchestrator import Orchestrator
from sidekick.planner import Planner
from sidekick.tools import ToolRegistry,ToolDefinition
from sidekick.AI_planner import AIPlanner
from sidekick.approvals import ApprovalService


app = FastAPI(title="Sidekick API")

registry = ToolRegistry()

def search_emails(query: str) -> dict:
    return {
        "query": query,
        "emails": [],
        "message": "Mock result. Email integration is not connected yet.",
    }

def mock_sensitive_action(message: str) -> dict:
    return {
        "executed": True,
        "message": message,
    }

registry.register(
    ToolDefinition(
        name="search_emails",
        description="Search emails by sender, subject, or keywords",
        parameters={
            "query": {
                "type": "string",
                "required": True,
            }
        },
        requires_approval=False,
        func=search_emails,
    )
)

approval_service = ApprovalService()

planner = AIPlanner(registry)

orchestrator = Orchestrator(
    planner=planner,
    registry=registry,
    approval_service=approval_service,
)

class TaskRequest(BaseModel):
    user_request: str

@app.get("/health")
def health_check():
    return {"status" : "ok"}


@app.post("/task")
def create_task(request: TaskRequest):
    task, plan = orchestrator.create_task(request.user_request)

    try:
        execution = orchestrator.execute_plan(plan)
    except (KeyError, ValueError, PermissionError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "task": task.model_dump(mode="json"),
        "plan": plan.model_dump(mode="json"),
        "execution": execution,
    }


@app.post("/actions/{action_id}/approve")
def approve_action(action_id:str):
    try:
        action = orchestrator.approval_service.approve_action(action_id)

        return {"action_id":action.action_id,
                "status": action.status.value,
                "message": "Action approved. Ready for execution.",
            }

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail = str(exc)
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

@app.post("/actions/{action_id}/execute")
def execute(action_id:str):
    try:
        return orchestrator.execute_approved_action(action_id)
        

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc



@app.post("/actions/{action_id}/reject")

def reject_action(action_id:str):
    try:

        action = orchestrator.approval_service.reject_action(
            action_id
        )

        return {
            "action_id": action.action_id,
            "status": action.status.value,
            "message": "Action rejected",
        }

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc





