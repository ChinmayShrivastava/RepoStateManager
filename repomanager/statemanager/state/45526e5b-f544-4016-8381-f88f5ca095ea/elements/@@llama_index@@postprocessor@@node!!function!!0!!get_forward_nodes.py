def get_forward_nodes(
    node_with_score: NodeWithScore, num_nodes: int, docstore: BaseDocumentStore
) -> Dict[str, NodeWithScore]:
    """Get forward nodes."""
    node = node_with_score.node
    nodes: Dict[str, NodeWithScore] = {node.node_id: node_with_score}
    cur_count = 0
    # get forward nodes in an iterative manner
    while cur_count < num_nodes:
        if NodeRelationship.NEXT not in node.relationships:
            break

        next_node_info = node.next_node
        if next_node_info is None:
            break

        next_node_id = next_node_info.node_id
        next_node = docstore.get_node(next_node_id)
        nodes[next_node.node_id] = NodeWithScore(node=next_node)
        node = next_node
        cur_count += 1
    return nodes
