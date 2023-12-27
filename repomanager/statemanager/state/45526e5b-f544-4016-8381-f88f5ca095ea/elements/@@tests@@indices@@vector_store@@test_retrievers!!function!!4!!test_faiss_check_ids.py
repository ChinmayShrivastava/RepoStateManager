def test_faiss_check_ids(
    mock_service_context: ServiceContext,
    faiss_storage_context: StorageContext,
) -> None:
    """Test embedding query."""
    ref_doc_id = "ref_doc_id_test"
    source_rel = {NodeRelationship.SOURCE: RelatedNodeInfo(node_id=ref_doc_id)}
    all_nodes = [
        TextNode(text="Hello world.", id_="node1", relationships=source_rel),
        TextNode(text="This is a test.", id_="node2", relationships=source_rel),
        TextNode(text="This is another test.", id_="node3", relationships=source_rel),
        TextNode(text="This is a test v2.", id_="node4", relationships=source_rel),
    ]

    index = VectorStoreIndex(
        all_nodes,
        storage_context=faiss_storage_context,
        service_context=mock_service_context,
    )

    # test query
    query_str = "What is?"
    retriever = index.as_retriever()
    nodes = retriever.retrieve(QueryBundle(query_str))
    assert nodes[0].node.get_content() == "This is another test."
    assert nodes[0].node.ref_doc_id == "ref_doc_id_test"
    assert nodes[0].node.node_id == "node3"
