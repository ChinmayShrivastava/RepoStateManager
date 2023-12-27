def test_list_insert(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test insert to list."""
    summary_index = SummaryIndex([], service_context=mock_service_context)
    assert len(summary_index.index_struct.nodes) == 0
    summary_index.insert(documents[0])
    nodes = summary_index.docstore.get_nodes(summary_index.index_struct.nodes)
    # check contents of nodes
    assert nodes[0].get_content() == "Hello world."
    assert nodes[1].get_content() == "This is a test."
    assert nodes[2].get_content() == "This is another test."
    assert nodes[3].get_content() == "This is a test v2."

    # test insert with ID
    document = documents[0]
    document.doc_id = "test_id"  # type: ignore[misc]
    summary_index = SummaryIndex([])
    summary_index.insert(document)
    # check contents of nodes
    nodes = summary_index.docstore.get_nodes(summary_index.index_struct.nodes)
    # check contents of nodes
    for node in nodes:
        assert node.ref_doc_id == "test_id"
