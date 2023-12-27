def test_fixed_recency_postprocessor(
    mock_service_context: ServiceContext,
) -> None:
    """Test fixed recency processor."""
    # try in metadata
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
    node_with_scores = [NodeWithScore(node=node) for node in nodes]

    postprocessor = FixedRecencyPostprocessor(
        top_k=1, service_context=mock_service_context
    )
    query_bundle: QueryBundle = QueryBundle(query_str="What is?")
    result_nodes = postprocessor.postprocess_nodes(
        node_with_scores, query_bundle=query_bundle
    )
    assert len(result_nodes) == 1
    assert (
        result_nodes[0].node.get_content(metadata_mode=MetadataMode.ALL)
        == "date: 2020-01-04\n\nThis is a test v2."
    )
