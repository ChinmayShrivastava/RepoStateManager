def adapt_to_async_tool(tool: BaseTool) -> AsyncBaseTool:
    """
    Converts a synchronous tool to an async tool.
    """
    if isinstance(tool, AsyncBaseTool):
        return tool
    else:
        return BaseToolAsyncAdapter(tool)
