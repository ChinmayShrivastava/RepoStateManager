def test_keyword_postprocessor_for_non_english() -> None:
    """Test keyword processor for non English."""
    key = "__last_accessed__"
    # try in metadata
    nodes = [
        TextNode(text="こんにちは世界。", id_="1", metadata={key: 0}),
        TextNode(text="これはテストです。", id_="2", metadata={key: 1}),
        TextNode(text="これは別のテストです。", id_="3", metadata={key: 2}),
        TextNode(text="これはテストv2です。", id_="4", metadata={key: 3}),
    ]
    node_with_scores = [NodeWithScore(node=node) for node in nodes]

    postprocessor = KeywordNodePostprocessor(required_keywords=["これ"], lang="ja")
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[0].node.get_content() == "これはテストです。"
    assert new_nodes[1].node.get_content() == "これは別のテストです。"
    assert new_nodes[2].node.get_content() == "これはテストv2です。"

    postprocessor = KeywordNodePostprocessor(required_keywords=["別の"], lang="ja")
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[0].node.get_content() == "これは別のテストです。"
    assert len(new_nodes) == 1

    # test exclude keywords
    postprocessor = KeywordNodePostprocessor(exclude_keywords=["別の"], lang="ja")
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[1].node.get_content() == "これはテストです。"
    assert new_nodes[2].node.get_content() == "これはテストv2です。"
    assert len(new_nodes) == 3

    # test both required and exclude keywords
    postprocessor = KeywordNodePostprocessor(
        required_keywords=["テスト"], exclude_keywords=["v2"], lang="ja"
    )
    new_nodes = postprocessor.postprocess_nodes(node_with_scores)
    assert new_nodes[0].node.get_content() == "これはテストです。"
    assert new_nodes[1].node.get_content() == "これは別のテストです。"
    assert len(new_nodes) == 2
