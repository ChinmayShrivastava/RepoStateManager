def test_build_faiss(
    documents: List[Document],
    faiss_storage_context: StorageContext,
    mock_service_context: ServiceContext,
) -> None:
    """Test build VectorStoreIndex with FaissVectoreStore."""
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=faiss_storage_context,
        service_context=mock_service_context,
    )
    assert len(index.index_struct.nodes_dict) == 4

    node_ids = list(index.index_struct.nodes_dict.values())
    nodes = index.docstore.get_nodes(node_ids)
    node_texts = [node.get_content() for node in nodes]
    assert "Hello world." in node_texts
    assert "This is a test." in node_texts
    assert "This is another test." in node_texts
    assert "This is a test v2." in node_texts
