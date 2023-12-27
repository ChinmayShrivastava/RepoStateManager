def test_retrieve_default(
    documents: List[Document], mock_service_context: ServiceContext
) -> None:
    """Test list query."""
    index = SummaryIndex.from_documents(documents, service_context=mock_service_context)

    query_str = "What is?"
    retriever = index.as_retriever(retriever_mode="default")
    nodes = retriever.retrieve(query_str)

    for node_with_score, line in zip(nodes, documents[0].get_content().split("\n")):
        assert node_with_score.node.get_content() == line
