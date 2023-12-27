class _NodeGroup(BaseModel):
    """Every node in nodes have the same source node."""

    source_node: RelatedNodeInfo
    nodes: List[BaseNode]
