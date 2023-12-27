def test_llm_query(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test llm query."""
    index = SummaryIndex.from_documents(documents, service_context=mock_service_context)

    # test llm query (batch size 10)
    query_str = "What is?"
    retriever = index.as_retriever(retriever_mode="llm")
    nodes = retriever.retrieve(query_str)
    assert len(nodes) == 1

    assert nodes[0].node.get_content() == "This is a test."

    # test llm query (batch size 2)
    query_str = "What is?"
    retriever = index.as_retriever(retriever_mode="llm", choice_batch_size=2)
    nodes = retriever.retrieve(query_str)
    assert len(nodes) == 2

    assert nodes[0].node.get_content() == "This is a test."
    assert nodes[1].node.get_content() == "This is a test v2."
