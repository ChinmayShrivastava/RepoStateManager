def test_simple_query(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test embedding query."""
    index = VectorStoreIndex.from_documents(
        documents, service_context=mock_service_context
    )

    # test embedding query
    query_str = "What is?"
    retriever = index.as_retriever(similarity_top_k=1)
    nodes = retriever.retrieve(QueryBundle(query_str))
    assert len(nodes) == 1
    assert nodes[0].node.get_content() == "This is another test."
