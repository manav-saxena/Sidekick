import pytest
from sidekick.tools import ToolDefinition, ToolRegistry

def test_register_and_get_tool():
    registry = ToolRegistry()
    tool = ToolDefinition(
        name="search_emails",
        description="Search emails by query"
    )

    registry.register(tool)

    assert registry.get("search_emails") == tool


def test_duplicate_registration():
    registry = ToolRegistry()
    tool = ToolDefinition(
        name="search_emails",
        description="Search emails by query"
    )

    registry.register(tool)

    with pytest.raises(ValueError):
        registry.register(tool)


def test_get_all_descriptions():
    registry = ToolRegistry()
    tool = ToolDefinition(
        name="search_emails",
        description="Search emails by query"
    )

    registry.register(tool)
    descriptions = registry.get_all_descriptions()

    assert len(descriptions) == 1
    assert descriptions[0]["name"] == "search_emails"
    assert isinstance(descriptions[0], dict)


def test_unknown_tool():
    registry = ToolRegistry()

    with pytest.raises(KeyError):
        registry.get("unknown_tool")

