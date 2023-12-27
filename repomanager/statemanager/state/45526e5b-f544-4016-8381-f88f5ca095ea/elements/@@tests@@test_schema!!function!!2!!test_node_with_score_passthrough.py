def test_node_with_score_passthrough(node_with_score: NodeWithScore) -> None:
    _ = node_with_score.id_
    _ = node_with_score.node_id
    _ = node_with_score.text
    _ = node_with_score.metadata
    _ = node_with_score.embedding
    _ = node_with_score.get_text()
    _ = node_with_score.get_content()
    _ = node_with_score.get_embedding()
