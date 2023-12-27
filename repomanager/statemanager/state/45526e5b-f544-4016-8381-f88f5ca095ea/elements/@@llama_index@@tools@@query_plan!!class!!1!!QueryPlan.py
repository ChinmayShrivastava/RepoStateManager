class QueryPlan(BaseModel):
    """Query plan.

    Contains a list of QueryNode objects (which is a recursive object).
    Out of the list of QueryNode objects, one of them must be the root node.
    The root node is the one that isn't a dependency of any other node.

    """

    nodes: List[QueryNode] = Field(
        ...,
        description="The original question we are asking.",
    )
