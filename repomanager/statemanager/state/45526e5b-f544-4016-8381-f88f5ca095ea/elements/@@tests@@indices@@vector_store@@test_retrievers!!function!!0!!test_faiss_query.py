def test_faiss_query(
    documents: List[Document],
    faiss_storage_context: StorageContext,
    mock_service_context: ServiceContext,
) -> None:
    """Test embedding query."""
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=faiss_storage_context,
        service_context=mock_service_context,
    )

    # test embedding query
    query_str = "What is?"
    retriever = index.as_retriever(similarity_top_k=1)
    nodes = retriever.retrieve(QueryBundle(query_str))
    assert len(nodes) == 1
    assert nodes[0].node.get_content() == "This is another test."
