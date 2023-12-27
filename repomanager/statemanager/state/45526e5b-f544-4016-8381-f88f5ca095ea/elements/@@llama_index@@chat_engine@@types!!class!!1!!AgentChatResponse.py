class AgentChatResponse:
    """Agent chat response."""

    response: str = ""
    sources: List[ToolOutput] = field(default_factory=list)
    source_nodes: List[NodeWithScore] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.sources and not self.source_nodes:
            for tool_output in self.sources:
                if isinstance(tool_output.raw_output, (Response, StreamingResponse)):
                    self.source_nodes.extend(tool_output.raw_output.source_nodes)

    def __str__(self) -> str:
        return self.response
