def test_retrieve(
    documents: List[Document], mock_service_context: ServiceContext
) -> None:
    """Test query."""
    # test simple keyword table
    # NOTE: here the keyword extraction isn't mocked because we're using
    # the regex-based keyword extractor, not GPT
    table = SimpleKeywordTableIndex.from_documents(
        documents, service_context=mock_service_context
    )

    retriever = table.as_retriever(retriever_mode="simple")
    nodes = retriever.retrieve(QueryBundle("Hello"))
    assert len(nodes) == 1
    assert nodes[0].node.get_content() == "Hello world."
