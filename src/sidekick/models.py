from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel,Field

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
    status: TaskStatus = TaskStatus.PENDING
    plan: list[str] = Field(default_factory=list)
    selected_tools: list[str] = Field(default_factory=list)
    result: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )



    