from pydantic import BaseModel, Field

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict = Field(default_factory=dict)
    requires_approval: bool = False

class ToolRegistry():
    def __init__(self):
        self._tools = {}
    def register(self, tool: ToolDefinition):
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")

        self._tools[tool.name] = tool
    def get(self , name:str) -> ToolDefinition:
        if name not in self._tools:
            raise KeyError(f"{name} not found")
        return self._tools


