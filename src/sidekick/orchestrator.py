from uuid import uuid4

from sidekick.models import Task, TaskStatus, ActionStatus  
from sidekick.planner import Planner, TaskPlan
from sidekick.approvals import ApprovalService
from datetime import datetime, timezone

class Orchestrator:
    def __init__(self,planner:Planner,registry, approval_service:ApprovalService):
        self.planner = planner
        self.registry = registry
        self.approval_service = approval_service

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

    def execute_plan(self, plan: TaskPlan):
        results = []

        for step in plan.steps:
            tool = self.registry.get(step.tool_name)

            if tool.requires_approval:
                action = self.approval_service.create_action(
                    task_id = plan.task_id,
                    action_type = step.tool_name,
                    payload={
                        "arguments": step.arguments,
                    },
                )
                return {
                    "status": "pending_approval",
                    "results": results,
                    "approval": {
                        "action_id": action.action_id,
                        "action_type": action.action_type,
                        "status": action.status.value,
                        "expires_at": action.expires_at.isoformat(),
                    },
                }
            result = self.registry.execute(
            step.tool_name,
            step.arguments,
            )

            results.append({
                "tool_name": step.tool_name,
                "result": result,
            })


        return {"status":"completed",
                "results": results,}

    def excecute_approved_action(self,action_id:str) ->dict:
        action = self.approval_service.actions.get(action_id)

        if action is None:
            raise KeyError(f"Action '{action_id}' not found")

        if action.status != ActionStatus.APPROVED:
            raise PermissionError(
            "Action must be approved before execution"
        )
        if action.expires_at is not None:
            if datetime.now(timezone.utc) >= action.expires_at:
                action.status = ActionStatus.EXPIRED
                raise PermissionError("Approval has expired")
        
        tool = self.registry.get(action.action_type)

        if not tool.requires_approval:
            raise PermissionError(
            "This action is not an approval-required tool"
        )

        action.status = ActionStatus.EXECUTING

        try:
            result = self.registry.execute(
                action.action_type,
                action.payload["arguments"],

            )
            action.status = ActionStatus.COMPLETED

            return {
                "status": "completed",
                "action_id": action.action_id,
                "result": result,
            }

        except Exception:
            action.status = ActionStatus.FAILED
            raise
    