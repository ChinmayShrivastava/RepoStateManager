def test_load_index_query_engine_service_context(
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

    # persist storage to disk
    storage_context.persist(str(tmp_path))

    # load storage context
    new_storage_context = StorageContext.from_defaults(persist_dir=str(tmp_path))

    # load index
    new_index = load_index_from_storage(
        storage_context=new_storage_context, service_context=mock_service_context
    )

    query_engine = index.as_query_engine()
    new_query_engine = new_index.as_query_engine()

    # make types happy
    assert isinstance(query_engine, RetrieverQueryEngine)
    assert isinstance(new_query_engine, RetrieverQueryEngine)
    # Ensure that the loaded index will end up querying with the same service_context
    assert (
        new_query_engine._response_synthesizer.service_context == mock_service_context
    )
