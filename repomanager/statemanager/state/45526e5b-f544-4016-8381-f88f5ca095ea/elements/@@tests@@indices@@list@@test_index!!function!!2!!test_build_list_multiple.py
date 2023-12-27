def test_build_list_multiple(mock_service_context: ServiceContext) -> None:
    """Test build list multiple."""
    documents = [
        Document(text="Hello world.\nThis is a test."),
        Document(text="This is another test.\nThis is a test v2."),
    ]
    summary_index = SummaryIndex.from_documents(
        documents, service_context=mock_service_context
    )
    assert len(summary_index.index_struct.nodes) == 4
    nodes = summary_index.docstore.get_nodes(summary_index.index_struct.nodes)
    # check contents of nodes
    assert nodes[0].get_content() == "Hello world."
    assert nodes[1].get_content() == "This is a test."
    assert nodes[2].get_content() == "This is another test."
    assert nodes[3].get_content() == "This is a test v2."
