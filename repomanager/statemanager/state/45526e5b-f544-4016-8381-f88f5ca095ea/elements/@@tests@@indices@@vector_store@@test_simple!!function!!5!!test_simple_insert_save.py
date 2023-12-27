def test_simple_insert_save(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(
        documents=documents,
        service_context=mock_service_context,
        storage_context=storage_context,
    )
    assert isinstance(index, VectorStoreIndex)

    loaded_index = load_index_from_storage(storage_context=storage_context)
    assert isinstance(loaded_index, VectorStoreIndex)
    assert index.index_struct == loaded_index.index_struct

    # insert into index
    index.insert(Document(text="This is a test v3."))

    loaded_index = load_index_from_storage(storage_context=storage_context)
    assert isinstance(loaded_index, VectorStoreIndex)
    assert index.index_struct == loaded_index.index_struct
