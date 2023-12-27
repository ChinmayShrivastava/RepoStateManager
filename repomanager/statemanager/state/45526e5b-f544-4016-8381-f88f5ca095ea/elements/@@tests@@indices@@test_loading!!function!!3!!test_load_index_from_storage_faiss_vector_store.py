def test_load_index_from_storage_faiss_vector_store(
    documents: List[Document],
    tmp_path: Path,
    mock_service_context: ServiceContext,
) -> None:
    import faiss

    # construct custom storage context
    storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore(),
        index_store=SimpleIndexStore(),
        vector_store=FaissVectorStore(faiss_index=faiss.IndexFlatL2(5)),
    )

    # construct index
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    nodes = index.as_retriever().retrieve("test query str")

    # persist storage to disk
    storage_context.persist(persist_dir=str(tmp_path))

    # load storage context
    new_storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore.from_persist_dir(str(tmp_path)),
        index_store=SimpleIndexStore.from_persist_dir(str(tmp_path)),
        vector_store=FaissVectorStore.from_persist_dir(str(tmp_path)),
    )

    # load index
    new_index = load_index_from_storage(
        new_storage_context, service_context=mock_service_context
    )

    new_nodes = new_index.as_retriever().retrieve("test query str")

    assert nodes == new_nodes
