def test_embedding_query(
    _patch_similarity: Any,
    index_kwargs: Dict,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test embedding query."""
    tree = TreeIndex.from_documents(
        documents, service_context=mock_service_context, **index_kwargs
    )

    # test embedding query
    query_str = "What is?"
    retriever = tree.as_retriever(retriever_mode="select_leaf_embedding")
    nodes = retriever.retrieve(QueryBundle(query_str))
    assert nodes[0].node.get_content() == "Hello world."
