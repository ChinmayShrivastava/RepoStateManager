def test_build_simple(
    mock_service_context: ServiceContext,
    documents: List[Document],
) -> None:
    """Test build VectorStoreIndex."""
    index = VectorStoreIndex.from_documents(
        documents=documents, service_context=mock_service_context
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
        # NOTE: this test breaks abstraction
        assert isinstance(index._vector_store, SimpleVectorStore)
        embedding = index._vector_store.get(text_id)
        assert (node.get_content(), embedding) in actual_node_tups

    # test ref doc info
    all_ref_doc_info = index.ref_doc_info
    for idx, ref_doc_id in enumerate(all_ref_doc_info.keys()):
        assert documents[idx].node_id == ref_doc_id
