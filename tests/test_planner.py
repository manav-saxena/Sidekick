from sidekick.planner import Planner
from sidekick.tools import ToolDefinition, ToolRegistry

def test_email_request_creates_plan():
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="search_emails",
            description="Search emails by query",
        )
    )

    planner = Planner(registry)
    plan = planner.create_plan(
        "Search my emails",
        "task-001",
    )
    assert plan.task_id == "task-001"
    assert len(plan.steps) == 1
    assert plan.steps[0].tool_name == "search_emails"


def test_missing_tool_returns_empty_plan():
    registry = ToolRegistry()
    planner = Planner(registry)

    plan = planner.create_plan(
        "Search my emails",
        "task-002",
    )

    assert plan.steps == []

def test_unrelated_request_returns_empty_plan():
    registry = ToolRegistry()
    planner = Planner(registry)

    plan = planner.create_plan(
        "Tell me a joke",
        "task-003",
    )

    assert plan.steps == []