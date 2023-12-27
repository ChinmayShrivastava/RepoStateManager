def test_load_index_from_storage_retrieval_result_identical(
    documents: List[Document],
    tmp_path: Path,
    mock_service_context: ServiceContext,
) -> None:
    # construct simple (i.e. in memory) storage context
    storage_context = StorageContext.from_defaults()

    # construct index
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    nodes = index.as_retriever().retrieve("test query str")

    # persist storage to disk
    storage_context.persist(str(tmp_path))

    # load storage context
    new_storage_context = StorageContext.from_defaults(persist_dir=str(tmp_path))

    # load index
    new_index = load_index_from_storage(
        new_storage_context, service_context=mock_service_context
    )

    new_nodes = new_index.as_retriever().retrieve("test query str")

    assert nodes == new_nodes
