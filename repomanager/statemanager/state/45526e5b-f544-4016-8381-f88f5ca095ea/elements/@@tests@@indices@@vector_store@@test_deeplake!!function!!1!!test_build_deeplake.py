def test_build_deeplake(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    import deeplake

    """Test build VectorStoreIndex with DeepLakeVectorStore."""
    dataset_path = "./llama_index_test"
    vector_store = DeepLakeVectorStore(
        dataset_path=dataset_path,
        overwrite=True,
        verbose=False,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    retriever = index.as_retriever(similarity_top_k=1)
    nodes = retriever.retrieve("What is the answer to the third test?")
    assert len(nodes) == 1
    assert nodes[0].node.get_content() == "This is the third test. answer is C"

    node = nodes[0].node

    node_with_embedding = node.copy()
    node_with_embedding.embedding = [1.0 for i in range(EMBEDDING_DIM)]
    new_nodes = [node_with_embedding for i in range(NUMBER_OF_DATA)]
    vector_store.add(new_nodes)
    assert len(vector_store.vectorstore) == 14

    ref_doc_id = str(node.ref_doc_id)
    vector_store.delete(ref_doc_id)
    assert len(vector_store.vectorstore) == 3
    deeplake.delete(dataset_path)
