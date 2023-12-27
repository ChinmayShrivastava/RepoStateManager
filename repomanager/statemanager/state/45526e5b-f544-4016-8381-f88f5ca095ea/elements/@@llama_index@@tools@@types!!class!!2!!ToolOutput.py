class ToolOutput(BaseModel):
    """Tool output."""

    content: str
    tool_name: str
    raw_input: Dict[str, Any]
    raw_output: Any

    def __str__(self) -> str:
        """String."""
        return str(self.content)
