class SimpleQueryToolNodeMapping(BaseQueryToolNodeMapping):
    """Simple query tool mapping."""

    def __init__(self, objs: Optional[Sequence[QueryEngineTool]] = None) -> None:
        objs = objs or []
        self._tools = {tool.metadata.name: tool for tool in objs}

    def validate_object(self, obj: QueryEngineTool) -> None:
        if not isinstance(obj, QueryEngineTool):
            raise ValueError(f"Object must be of type {QueryEngineTool}")

    @classmethod
    def from_objects(
        cls, objs: Sequence[QueryEngineTool], *args: Any, **kwargs: Any
    ) -> "BaseObjectNodeMapping":
        return cls(objs)

    def _add_object(self, tool: QueryEngineTool) -> None:
        if tool.metadata.name is None:
            raise ValueError("Tool name must be set")
        self._tools[tool.metadata.name] = tool

    def to_node(self, obj: QueryEngineTool) -> TextNode:
        """To node."""
        return convert_tool_to_node(obj)

    def _from_node(self, node: BaseNode) -> QueryEngineTool:
        """From node."""
        if node.metadata is None:
            raise ValueError("Metadata must be set")
        return self._tools[node.metadata["name"]]
