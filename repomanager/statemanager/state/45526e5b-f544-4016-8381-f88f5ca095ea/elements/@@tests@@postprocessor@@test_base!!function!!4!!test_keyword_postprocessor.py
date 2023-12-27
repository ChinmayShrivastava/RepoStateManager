def test_keyword_postprocessor() -> None:
    """Test keyword processor."""
    key = "__last_accessed__"
    # try in metadata
    nodes = [
        TextNode(text="Hello world.", id_="1", metadata={key: 0}),
        TextNode(text="This is a test.", id_="2", metadata={key: 1}),
        TextNode(text="This is another test.", id_="3", metadata={key: 2}),
        TextNode(text="This is a test v2.", id_="4", metadata={key: 3}),
    ]
    node_with_scores = [NodeWithScore(node=node) for node in nodes]

    postprocessor = KeywordNodePostprocessor(required_keywords=["This"])
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[0].node.get_content() == "This is a test."
    assert new_nodes[1].node.get_content() == "This is another test."
    assert new_nodes[2].node.get_content() == "This is a test v2."

    postprocessor = KeywordNodePostprocessor(required_keywords=["Hello"])
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[0].node.get_content() == "Hello world."
    assert len(new_nodes) == 1

    postprocessor = KeywordNodePostprocessor(required_keywords=["is another"])
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[0].node.get_content() == "This is another test."
    assert len(new_nodes) == 1

    # test exclude keywords
    postprocessor = KeywordNodePostprocessor(exclude_keywords=["is another"])
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[1].node.get_content() == "This is a test."
    assert new_nodes[2].node.get_content() == "This is a test v2."
    assert len(new_nodes) == 3
