def test_embedding_query(
    _patch_get_embeddings: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test embedding query."""
    index = SummaryIndex.from_documents(documents, service_context=mock_service_context)

    # test embedding query
    query_str = "What is?"
    retriever = index.as_retriever(retriever_mode="embedding", similarity_top_k=1)
    nodes = retriever.retrieve(query_str)
    assert len(nodes) == 1

    assert nodes[0].node.get_content() == "Hello world."
