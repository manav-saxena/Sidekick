from pydantic import BaseModel, Field
from typing import Callable, Any

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict = Field(default_factory=dict)
    requires_approval: bool = False
    func: Callable[..., Any] | None = None

class ToolRegistry():
    def __init__(self):
        self._tools = {}
    def register(self, tool: ToolDefinition):
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")

        self._tools[tool.name] = tool
    def get(self, name: str) -> ToolDefinition:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found")

        return self._tools[name]
    def get_all_descriptions(self) -> list[dict]:
        return [
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
            "requires_approval": tool.requires_approval,
        }
        for tool in self._tools.values()
    ]

    def validate_arguments(self, name: str, arguments: dict) -> None:
        tool = self.get(name)
        if not isinstance(arguments, dict):
            raise ValueError("Arguments must be a dictionary")

        parameters = tool.parameters

        for args_name in arguments:
            if args_name not in parameters:
                raise ValueError(f"Unexpected arguments:'{args_name}'")

        for param_name, schema in parameters.items():
            if schema.get("required", False) and param_name not in arguments:
                raise ValueError(f"Missing required argument: '{param_name}'")

    # Check argument types
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list,
        }

        for arg_name, value in arguments.items():
            expected_type = parameters[arg_name].get("type")
            python_type = type_map.get(expected_type)

            if python_type is None:
                raise ValueError(
                    f"Unsupported schema type '{expected_type}' for '{arg_name}'"
                )

        # bool is a subclass of int, so reject it for integer parameters
            if expected_type == "integer" and type(value) is not int:
                raise ValueError(f"Argument '{arg_name}' must be an integer")

            if expected_type == "number" and (
                isinstance(value, bool) or not isinstance(value, (int, float))
            ):
                raise ValueError(f"Argument '{arg_name}' must be a number")

            if expected_type not in ("integer", "number") and not isinstance(value, python_type):
                raise ValueError(
                    f"Argument '{arg_name}' must be of type '{expected_type}'"
                )

        return None
    def execute(self, name: str, arguments: dict) -> Any:
        tool = self.get(name)
        self.validate_arguments(name, arguments)
        if tool.func is None:
            raise ValueError(f"Tool '{name}' has no executable function")

        return tool.func(**arguments)