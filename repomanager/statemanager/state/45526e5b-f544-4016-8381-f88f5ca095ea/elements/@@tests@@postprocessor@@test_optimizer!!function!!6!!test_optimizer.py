def test_optimizer(_mock_embeds: Any, _mock_embed: Any) -> None:
    """Test optimizer."""
    optimizer = SentenceEmbeddingOptimizer(
        tokenizer_fn=mock_tokenizer_fn,
        percentile_cutoff=0.5,
        context_before=0,
        context_after=0,
    )
    query = QueryBundle(query_str="hello", embedding=[1, 0, 0, 0, 0])
    orig_node = TextNode(text="hello world")
    optimized_node = optimizer.postprocess_nodes(
        [NodeWithScore(node=orig_node)], query
    )[0]
    assert optimized_node.node.get_content() == "hello"

    # test with threshold cutoff
    optimizer = SentenceEmbeddingOptimizer(
        tokenizer_fn=mock_tokenizer_fn,
        threshold_cutoff=0.3,
        context_after=0,
        context_before=0,
    )
    query = QueryBundle(query_str="world", embedding=[0, 1, 0, 0, 0])
    orig_node = TextNode(text="hello world")
    optimized_node = optimizer.postprocess_nodes(
        [NodeWithScore(node=orig_node)], query
    )[0]
    assert optimized_node.node.get_content() == "world"

    # test with comma splitter
    optimizer = SentenceEmbeddingOptimizer(
        tokenizer_fn=mock_tokenizer_fn2,
        threshold_cutoff=0.3,
        context_after=0,
        context_before=0,
    )
    query = QueryBundle(query_str="foo", embedding=[0, 0, 1, 0, 0])
    orig_node = TextNode(text="hello,world,foo,bar")
    optimized_node = optimizer.postprocess_nodes(
        [NodeWithScore(node=orig_node)], query
    )[0]
    assert optimized_node.node.get_content() == "foo"

    # test with further context after top sentence
    optimizer = SentenceEmbeddingOptimizer(
        tokenizer_fn=mock_tokenizer_fn2,
        threshold_cutoff=0.3,
        context_after=1,
        context_before=0,
    )
    query = QueryBundle(query_str="foo", embedding=[0, 0, 1, 0, 0])
    orig_node = TextNode(text="hello,world,foo,bar")
    optimized_node = optimizer.postprocess_nodes(
        [NodeWithScore(node=orig_node)], query
    )[0]
    assert optimized_node.node.get_content() == "foo bar"

    # test with further context before and after top sentence
    optimizer = SentenceEmbeddingOptimizer(
        tokenizer_fn=mock_tokenizer_fn2,
        threshold_cutoff=0.3,
        context_after=1,
        context_before=1,
    )
    query = QueryBundle(query_str="foo", embedding=[0, 0, 1, 0, 0])
    orig_node = TextNode(text="hello,world,foo,bar")
    optimized_node = optimizer.postprocess_nodes(
        [NodeWithScore(node=orig_node)], query
    )[0]
    assert optimized_node.node.get_content() == "world foo bar"
