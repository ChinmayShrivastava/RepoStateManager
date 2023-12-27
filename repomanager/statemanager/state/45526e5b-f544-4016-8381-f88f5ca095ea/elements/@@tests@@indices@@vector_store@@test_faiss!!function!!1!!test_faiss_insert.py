def test_faiss_insert(
    documents: List[Document],
    faiss_storage_context: StorageContext,
    mock_service_context: ServiceContext,
) -> None:
    """Test insert VectorStoreIndex with FaissVectoreStore."""
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=faiss_storage_context,
        service_context=mock_service_context,
    )

    # insert into index
    index.insert(Document(text="This is a test v3."))

    # check contents of nodes
    node_ids = list(index.index_struct.nodes_dict.values())
    nodes = index.docstore.get_nodes(node_ids)
    node_texts = [node.get_content() for node in nodes]
    assert "This is a test v2." in node_texts
    assert "This is a test v3." in node_texts
