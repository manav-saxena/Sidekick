from datetime import datetime, timezone
from sidekick.models import Action, ActionStatus
import pytest
from pydantic import ValidationError

def test_action_defaults_to_pending():
    action = Action(
        action_id="act_001",
        task_id="task_001",
        action_type="send_email",
        created_at=datetime.now()
    )

    assert action.status == ActionStatus.PENDING

def test_invalid_default():
    with pytest.raises(ValidationError):
        action = Action(
                action_id="act_001",
                task_id="task_001",
                action_type="send_email",
                status = 0
            )

        