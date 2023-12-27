def get_backward_nodes(
    node_with_score: NodeWithScore, num_nodes: int, docstore: BaseDocumentStore
) -> Dict[str, NodeWithScore]:
    """Get backward nodes."""
    node = node_with_score.node
    # get backward nodes in an iterative manner
    nodes: Dict[str, NodeWithScore] = {node.node_id: node_with_score}
    cur_count = 0
    while cur_count < num_nodes:
        prev_node_info = node.prev_node
        if prev_node_info is None:
            break
        prev_node_id = prev_node_info.node_id
        prev_node = docstore.get_node(prev_node_id)
        if prev_node is None:
            break
        nodes[prev_node.node_id] = NodeWithScore(node=prev_node)
        node = prev_node
        cur_count += 1
    return nodes
