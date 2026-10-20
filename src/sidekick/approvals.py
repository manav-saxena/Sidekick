from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sidekick.models import Action, ActionStatus

class ApprovalService:
    def __init__(self):
        self.actions: dict[str, Action] = {}

    def create_action(self, task_id:str,action_type:str,payload: dict,ttl_minutes = 15,) ->Action:
        if ttl_minutes <=0:
            raise ValueError("the ttl should be positive")

        now = datetime.now(timezone.utc)
        action = Action(action_id=str(uuid4()),
                        task_id=task_id,
                        action_type=action_type,
                        payload=payload,
                        status=ActionStatus.PENDING,
                        created_at=now,
                        expires_at=now + timedelta(minutes = ttl_minutes))
        self.actions[action.action_id]= action
        return action

    
    def approve_action(self, action_id: str) -> Action:
        action = self._get_pending_action(action_id)

        action.status = ActionStatus.APPROVED
        action.approved_at = datetime.now(timezone.utc)
        return action

    def reject_action(self, action_id: str) -> Action:
        action = self._get_pending_action(action_id)

        action.status = ActionStatus.REJECTED
        return action

    def _get_pending_action(self,action_id:str) -> Action:
        action = self.actions.get(action_id)

        if action is None:
            raise KeyError(f"Action '{action_id} not found")

        if action.status != ActionStatus.PENDING:
            raise ValueError("Action is no longer pending")

        now = datetime.now(timezone.utc)

        if action.expires_at is not None and now >= action.expires_at:
            action.status = ActionStatus.EXPIRED
            raise ValueError("Approval has expired")

        return action
        

    