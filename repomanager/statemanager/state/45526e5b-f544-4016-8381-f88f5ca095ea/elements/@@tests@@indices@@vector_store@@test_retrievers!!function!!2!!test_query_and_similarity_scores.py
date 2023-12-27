def test_query_and_similarity_scores(
    mock_service_context: ServiceContext,
) -> None:
    """Test that sources nodes have similarity scores."""
    doc_text = (
        "Hello world.\n"
        "This is a test.\n"
        "This is another test.\n"
        "This is a test v2."
    )
    document = Document(text=doc_text)
    index = VectorStoreIndex.from_documents(
        [document], service_context=mock_service_context
    )

    # test embedding query
    query_str = "What is?"
    retriever = index.as_retriever()
    nodes = retriever.retrieve(QueryBundle(query_str))
    assert len(nodes) > 0
    assert nodes[0].score is not None
