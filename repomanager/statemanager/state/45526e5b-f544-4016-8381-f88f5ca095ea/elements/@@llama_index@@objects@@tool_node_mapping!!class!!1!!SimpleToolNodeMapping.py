class SimpleToolNodeMapping(BaseToolNodeMapping):
    """Simple Tool mapping.

    In this setup, we assume that the tool name is unique, and
    that the list of all tools are stored in memory.

    """

    def __init__(self, objs: Optional[Sequence[BaseTool]] = None) -> None:
        objs = objs or []
        self._tools = {tool.metadata.name: tool for tool in objs}

    @classmethod
    def from_objects(
        cls, objs: Sequence[BaseTool], *args: Any, **kwargs: Any
    ) -> "BaseObjectNodeMapping":
        return cls(objs)

    def _add_object(self, tool: BaseTool) -> None:
        self._tools[tool.metadata.name] = tool

    def to_node(self, tool: BaseTool) -> TextNode:
        """To node."""
        return convert_tool_to_node(tool)

    def _from_node(self, node: BaseNode) -> BaseTool:
        """From node."""
        if node.metadata is None:
            raise ValueError("Metadata must be set")
        return self._tools[node.metadata["name"]]
