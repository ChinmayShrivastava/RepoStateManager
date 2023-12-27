def test_node_with_metadata(
    mock_service_context: ServiceContext,
) -> None:
    storage_context = get_pinecone_storage_context()
    input_nodes = [TextNode(text="test node text", metadata={"key": "value"})]
    index = VectorStoreIndex(
        input_nodes,
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    retriever = index.as_retriever(similarity_top_k=1)
    nodes = retriever.retrieve("What is?")
    assert len(nodes) == 1
    assert nodes[0].node.get_content() == "test node text"
    assert nodes[0].node.metadata == {"key": "value"}
