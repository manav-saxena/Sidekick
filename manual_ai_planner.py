from sidekick.AI_planner import AIPlanner
from sidekick.tools import ToolRegistry, ToolDefinition

registry = ToolRegistry()

registry.register(
    ToolDefinition(
        name="search_emails",
        description="Search emails by sender, subject, or keywords",
        parameters={"query": "string"},
    )
)

planner = AIPlanner(registry)

plan = planner.create_plan(
    user_request="Find unread emails from my manager",
    task_id="task-ai-001",
)

print(plan.model_dump_json(indent=2))