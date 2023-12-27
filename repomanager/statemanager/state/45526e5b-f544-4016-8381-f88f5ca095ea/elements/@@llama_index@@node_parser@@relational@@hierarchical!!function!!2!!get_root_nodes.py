def get_root_nodes(nodes: List[BaseNode]) -> List[BaseNode]:
    """Get root nodes."""
    root_nodes = []
    for node in nodes:
        if NodeRelationship.PARENT not in node.relationships:
            root_nodes.append(node)
    return root_nodes
