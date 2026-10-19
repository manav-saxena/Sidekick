from sidekick.models import TaskStatus
from sidekick.orchestrator import Orchestrator
from sidekick.planner import Planner
from sidekick.tools import ToolDefinition, ToolRegistry


def test_orchestrator_creates_task_and_plan():
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="search_emails",
            description="Search emails by query",
        )
    )

    planner = Planner(registry)
    orchestrator = Orchestrator(planner)

    task, plan = orchestrator.create_task("Search my emails")

    assert task.user_request == "Search my emails"
    assert task.status == TaskStatus.PENDING
    assert task.task_id == plan.task_id
    assert task.selected_tools == ["search_emails"]


def test_orchestrator_handles_unsupported_request():
    registry = ToolRegistry()
    planner = Planner(registry)
    orchestrator = Orchestrator(planner)

    task, plan = orchestrator.create_task("Tell me a joke")

    assert task.status == TaskStatus.FAILED
    assert task.result == plan.summary
    assert task.selected_tools == []