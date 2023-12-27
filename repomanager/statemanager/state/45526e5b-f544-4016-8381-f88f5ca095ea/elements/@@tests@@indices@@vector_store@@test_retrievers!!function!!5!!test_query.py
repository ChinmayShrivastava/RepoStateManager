def test_query(mock_service_context: ServiceContext) -> None:
    """Test embedding query."""
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
    _ = retriever.retrieve(QueryBundle(query_str))
