def test_init_without_documents(documents: List[Document]) -> None:
    client = clickhouse_connect.get_client(
        host=MYSCALE_CLUSTER_URL,
        port=8443,
        username=MYSCALE_USERNAME,
        password=MYSCALE_CLUSTER_PASSWORD,
    )
    vector_store = MyScaleVectorStore(myscale_client=client)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    for doc in documents:
        index.insert(document=doc)
    query_engine = index.as_query_engine()
    response = query_engine.query("What is?")
    assert str(response).strip() == ("What is what?")

    cast(MyScaleVectorStore, index._vector_store).drop()
