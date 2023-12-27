class QueryNode(BaseModel):
    """Query node.

    A query node represents a query (query_str) that must be answered.
    It can either be answered by a tool (tool_name), or by a list of child nodes
    (child_nodes).
    The tool_name and child_nodes fields are mutually exclusive.

    """

    # NOTE: inspired from https://github.com/jxnl/openai_function_call/pull/3/files

    id: int = Field(..., description="ID of the query node.")
    query_str: str = Field(..., description=QUERYNODE_QUERY_STR_DESC)
    tool_name: Optional[str] = Field(
        default=None, description="Name of the tool to execute the `query_str`."
    )
    dependencies: List[int] = Field(
        default_factory=list, description=QUERYNODE_DEPENDENCIES_DESC
    )
