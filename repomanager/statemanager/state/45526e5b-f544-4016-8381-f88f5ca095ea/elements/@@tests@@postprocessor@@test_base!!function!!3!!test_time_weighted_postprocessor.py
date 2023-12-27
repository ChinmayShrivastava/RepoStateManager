def test_time_weighted_postprocessor() -> None:
    """Test time weighted processor."""
    key = "__last_accessed__"
    # try in metadata
    nodes = [
        TextNode(text="Hello world.", id_="1", metadata={key: 0}),
        TextNode(text="This is a test.", id_="2", metadata={key: 1}),
        TextNode(text="This is another test.", id_="3", metadata={key: 2}),
        TextNode(text="This is a test v2.", id_="4", metadata={key: 3}),
    ]
    node_with_scores = [NodeWithScore(node=node) for node in nodes]

    # high time decay
    postprocessor = TimeWeightedPostprocessor(
        top_k=1, time_decay=0.99999, time_access_refresh=True, now=4.0
    )
    result_nodes_with_score = postprocessor.postprocess_nodes(node_with_scores)

    assert len(result_nodes_with_score) == 1
    assert result_nodes_with_score[0].node.get_content() == "This is a test v2."
    assert cast(Dict, nodes[0].metadata)[key] == 0
    assert cast(Dict, nodes[3].metadata)[key] != 3

    # low time decay
    # artificially make earlier nodes more relevant
    # therefore postprocessor should still rank earlier nodes higher
    nodes = [
        TextNode(text="Hello world.", id_="1", metadata={key: 0}),
        TextNode(text="This is a test.", id_="2", metadata={key: 1}),
        TextNode(text="This is another test.", id_="3", metadata={key: 2}),
        TextNode(text="This is a test v2.", id_="4", metadata={key: 3}),
    ]
    node_with_scores = [
        NodeWithScore(node=node, score=-float(idx)) for idx, node in enumerate(nodes)
    ]
    postprocessor = TimeWeightedPostprocessor(
        top_k=1, time_decay=0.000000000002, time_access_refresh=True, now=4.0
    )
    result_nodes_with_score = postprocessor.postprocess_nodes(node_with_scores)
    assert len(result_nodes_with_score) == 1
    assert result_nodes_with_score[0].node.get_content() == "Hello world."
    assert cast(Dict, nodes[0].metadata)[key] != 0
    assert cast(Dict, nodes[3].metadata)[key] == 3
