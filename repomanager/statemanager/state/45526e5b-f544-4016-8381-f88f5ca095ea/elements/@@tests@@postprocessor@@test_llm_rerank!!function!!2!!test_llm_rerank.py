def test_llm_rerank(mock_service_context: ServiceContext) -> None:
    """Test LLM rerank."""
    nodes = [
        TextNode(text="Test"),
        TextNode(text="Test2"),
        TextNode(text="Test3"),
        TextNode(text="Test4"),
        TextNode(text="Test5"),
        TextNode(text="Test6"),
        TextNode(text="Test7"),
        TextNode(text="Test8"),
    ]
    nodes_with_score = [NodeWithScore(node=n) for n in nodes]

    # choice batch size 4 (so two batches)
    # take top-3 across all data
    llm_rerank = LLMRerank(
        format_node_batch_fn=mock_format_node_batch_fn,
        choice_batch_size=4,
        top_n=3,
        service_context=mock_service_context,
    )
    query_str = "What is?"
    result_nodes = llm_rerank.postprocess_nodes(
        nodes_with_score, QueryBundle(query_str)
    )
    assert len(result_nodes) == 3
    assert result_nodes[0].node.get_content() == "Test7"
    assert result_nodes[1].node.get_content() == "Test5"
    assert result_nodes[2].node.get_content() == "Test3"
