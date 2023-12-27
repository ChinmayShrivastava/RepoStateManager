def test_query(
    documents: List[Document],
    mock_service_context: ServiceContext,
    struct_kwargs: Dict,
) -> None:
    """Test query."""
    index_kwargs, query_kwargs = struct_kwargs
    tree = TreeIndex.from_documents(
        documents, service_context=mock_service_context, **index_kwargs
    )

    # test default query
    query_str = "What is?"
    retriever = tree.as_retriever()
    nodes = retriever.retrieve(query_str)
    assert len(nodes) == 1
