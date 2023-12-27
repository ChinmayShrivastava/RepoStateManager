def test_simple_pickle(
    mock_service_context: ServiceContext,
    documents: List[Document],
) -> None:
    """Test build VectorStoreIndex."""
    service_context = ServiceContext.from_service_context(
        mock_service_context,
        llm=OpenAI(),
    )

    index = VectorStoreIndex.from_documents(
        documents=documents, service_context=service_context
    )

    data = pickle.dumps(index)
    new_index = pickle.loads(data)

    assert isinstance(new_index, VectorStoreIndex)
    assert len(new_index.index_struct.nodes_dict) == 4
    # check contents of nodes
    actual_node_tups = [
        ("Hello world.", [1, 0, 0, 0, 0]),
        ("This is a test.", [0, 1, 0, 0, 0]),
        ("This is another test.", [0, 0, 1, 0, 0]),
        ("This is a test v2.", [0, 0, 0, 1, 0]),
    ]
    for text_id in new_index.index_struct.nodes_dict:
        node_id = new_index.index_struct.nodes_dict[text_id]
        node = new_index.docstore.get_node(node_id)
        # NOTE: this test breaks abstraction
        assert isinstance(new_index._vector_store, SimpleVectorStore)
        embedding = new_index._vector_store.get(text_id)
        assert (node.get_content(), embedding) in actual_node_tups

    # test ref doc info
    all_ref_doc_info = new_index.ref_doc_info
    for idx, ref_doc_id in enumerate(all_ref_doc_info.keys()):
        assert documents[idx].node_id == ref_doc_id
