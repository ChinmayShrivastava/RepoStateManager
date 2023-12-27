def test_embedding_recency_postprocessor(
    mock_service_context: ServiceContext,
) -> None:
    """Test fixed recency processor."""
    # try in node info
    nodes = [
        TextNode(
            text="Hello world.",
            id_="1",
            metadata={"date": "2020-01-01"},
            excluded_embed_metadata_keys=["date"],
        ),
        TextNode(
            text="This is a test.",
            id_="2",
            metadata={"date": "2020-01-02"},
            excluded_embed_metadata_keys=["date"],
        ),
        TextNode(
            text="This is another test.",
            id_="3",
            metadata={"date": "2020-01-02"},
            excluded_embed_metadata_keys=["date"],
        ),
        TextNode(
            text="This is another test.",
            id_="3v2",
            metadata={"date": "2020-01-03"},
            excluded_embed_metadata_keys=["date"],
        ),
        TextNode(
            text="This is a test v2.",
            id_="4",
            metadata={"date": "2020-01-04"},
            excluded_embed_metadata_keys=["date"],
        ),
    ]
    nodes_with_scores = [NodeWithScore(node=node) for node in nodes]

    postprocessor = EmbeddingRecencyPostprocessor(
        top_k=1,
        service_context=mock_service_context,
        in_metadata=False,
        query_embedding_tmpl="{context_str}",
    )
    query_bundle: QueryBundle = QueryBundle(query_str="What is?")
    result_nodes = postprocessor.postprocess_nodes(
        nodes_with_scores, query_bundle=query_bundle
    )
    # TODO: bring back this test
    # assert len(result_nodes) == 4
    assert result_nodes[0].node.get_content() == "This is a test v2."
    assert cast(Dict, result_nodes[0].node.metadata)["date"] == "2020-01-04"
