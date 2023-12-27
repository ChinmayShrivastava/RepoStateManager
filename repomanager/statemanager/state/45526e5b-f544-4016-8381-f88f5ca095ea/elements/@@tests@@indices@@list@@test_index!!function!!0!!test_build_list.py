def test_build_list(
    documents: List[Document], mock_service_context: ServiceContext
) -> None:
    """Test build list."""
    summary_index = SummaryIndex.from_documents(
        documents, service_context=mock_service_context
    )
    assert len(summary_index.index_struct.nodes) == 4
    # check contents of nodes
    node_ids = summary_index.index_struct.nodes
    nodes = summary_index.docstore.get_nodes(node_ids)
    assert nodes[0].get_content() == "Hello world."
    assert nodes[1].get_content() == "This is a test."
    assert nodes[2].get_content() == "This is another test."
    assert nodes[3].get_content() == "This is a test v2."
