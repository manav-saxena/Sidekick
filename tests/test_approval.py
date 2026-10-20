from datetime import datetime, timedelta, timezone

import pytest

from sidekick.approvals import ApprovalService
from sidekick.models import ActionStatus


def test_expired_action_cannot_be_approved():
    service = ApprovalService()

    action = service.create_action(
        task_id="task-001",
        action_type="send_email",
        payload={"to": "test@example.com"},
        ttl_minutes=15,
    )

    # Simulate the action expiring.
    action.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)

    with pytest.raises(ValueError, match="expired"):
        service.approve_action(action.action_id)

    assert action.status == ActionStatus.EXPIRED


def test_rejected_action_cannot_be_approved():
    service = ApprovalService()

    action = service.create_action(
        task_id="task-001",
        action_type="send_email",
        payload={"to": "test@example.com"},
    )

    service.reject_action(action.action_id)

    with pytest.raises(ValueError, match="no longer pending"):
        service.approve_action(action.action_id)