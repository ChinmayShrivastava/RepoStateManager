def test_simple_async(
    allow_networking: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test simple vector index with use_async."""
    index = VectorStoreIndex.from_documents(
        documents=documents, use_async=True, service_context=mock_service_context
    )
    assert isinstance(index, VectorStoreIndex)
    assert len(index.index_struct.nodes_dict) == 4
    # check contents of nodes
    actual_node_tups = [
        ("Hello world.", [1, 0, 0, 0, 0]),
        ("This is a test.", [0, 1, 0, 0, 0]),
        ("This is another test.", [0, 0, 1, 0, 0]),
        ("This is a test v2.", [0, 0, 0, 1, 0]),
    ]
    for text_id in index.index_struct.nodes_dict:
        node_id = index.index_struct.nodes_dict[text_id]
        node = index.docstore.get_node(node_id)
        vector_store = cast(SimpleVectorStore, index._vector_store)
        embedding = vector_store.get(text_id)
        assert (node.get_content(), embedding) in actual_node_tups
