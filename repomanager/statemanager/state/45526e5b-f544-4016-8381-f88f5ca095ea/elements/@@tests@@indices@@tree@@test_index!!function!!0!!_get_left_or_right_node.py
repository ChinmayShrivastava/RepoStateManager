def _get_left_or_right_node(
    docstore: BaseDocumentStore,
    index_graph: IndexGraph,
    node: Optional[BaseNode],
    left: bool = True,
) -> BaseNode:
    """Get 'left' or 'right' node."""
    children_dict = index_graph.get_children(node)
    indices = list(children_dict.keys())
    index = min(indices) if left else max(indices)
    node_id = children_dict[index]
    return docstore.get_node(node_id)
