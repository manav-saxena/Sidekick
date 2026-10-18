from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class ActionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    OUTCOME_UNKNOWN = "outcome_unknown"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Action(BaseModel):
    action_id: str
    task_id: str
    action_type: str
    status: ActionStatus = ActionStatus.PENDING
    created_at: datetime
    expires_at: datetime | None = None
    approved_at: datetime | None = None


class TaskStatus(str, Enum):
    PENDING = "pending"
    PLANNING = "planning"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    task_id : str
    user_request : str
    status: TaskStatus
    plan = list[str] 
    selected_tool = list[str]
    result: str | None
    created=datetime.now()



    