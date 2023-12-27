class LlamaIndexTool(BaseTool):
    """Tool for querying a LlamaIndex."""

    # NOTE: name/description still needs to be set
    query_engine: BaseQueryEngine
    return_sources: bool = False

    @classmethod
    def from_tool_config(cls, tool_config: IndexToolConfig) -> "LlamaIndexTool":
        """Create a tool from a tool config."""
        return_sources = tool_config.tool_kwargs.pop("return_sources", False)
        return cls(
            query_engine=tool_config.query_engine,
            name=tool_config.name,
            description=tool_config.description,
            return_sources=return_sources,
            **tool_config.tool_kwargs,
        )

    def _run(self, input: str) -> str:
        response = self.query_engine.query(input)
        if self.return_sources:
            return _get_response_with_sources(response)
        return str(response)

    async def _arun(self, input: str) -> str:
        response = await self.query_engine.aquery(input)
        if self.return_sources:
            return _get_response_with_sources(response)
        return str(response)
