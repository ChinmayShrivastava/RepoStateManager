def test_simple_insert(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test insert VectorStoreIndex."""
    index = VectorStoreIndex.from_documents(
        documents=documents, service_context=mock_service_context
    )
    assert isinstance(index, VectorStoreIndex)
    # insert into index
    index.insert(Document(text="This is a test v3."))

    # check contenst of nodes
    actual_node_tups = [
        ("Hello world.", [1, 0, 0, 0, 0]),
        ("This is a test.", [0, 1, 0, 0, 0]),
        ("This is another test.", [0, 0, 1, 0, 0]),
        ("This is a test v2.", [0, 0, 0, 1, 0]),
        ("This is a test v3.", [0, 0, 0, 0, 1]),
    ]
    for text_id in index.index_struct.nodes_dict:
        node_id = index.index_struct.nodes_dict[text_id]
        node = index.docstore.get_node(node_id)
        # NOTE: this test breaks abstraction
        assert isinstance(index._vector_store, SimpleVectorStore)
        embedding = index._vector_store.get(text_id)
        assert (node.get_content(), embedding) in actual_node_tups
