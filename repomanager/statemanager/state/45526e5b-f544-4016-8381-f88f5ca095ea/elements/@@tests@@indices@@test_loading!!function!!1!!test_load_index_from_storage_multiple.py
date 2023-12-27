def test_load_index_from_storage_multiple(
    nodes: List[BaseNode],
    tmp_path: Path,
    mock_service_context: ServiceContext,
) -> None:
    # construct simple (i.e. in memory) storage context
    storage_context = StorageContext.from_defaults()

    # add nodes to docstore
    storage_context.docstore.add_documents(nodes)

    # construct multiple indices
    vector_index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        service_context=mock_service_context,
    )
    vector_id = vector_index.index_id

    summary_index = SummaryIndex(
        nodes=nodes,
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    list_id = summary_index.index_id

    # persist storage to disk
    storage_context.persist(str(tmp_path))

    # load storage context
    new_storage_context = StorageContext.from_defaults(persist_dir=str(tmp_path))

    # load single index should fail since there are multiple indices in index store
    with pytest.raises(ValueError):
        load_index_from_storage(
            new_storage_context, service_context=mock_service_context
        )

    # test load all indices
    indices = load_indices_from_storage(storage_context)
    index_ids = [index.index_id for index in indices]
    assert len(index_ids) == 2
    assert vector_id in index_ids
    assert list_id in index_ids

    # test load multiple indices by ids
    indices = load_indices_from_storage(storage_context, index_ids=[list_id, vector_id])
    index_ids = [index.index_id for index in indices]
    assert len(index_ids) == 2
    assert vector_id in index_ids
    assert list_id in index_ids
