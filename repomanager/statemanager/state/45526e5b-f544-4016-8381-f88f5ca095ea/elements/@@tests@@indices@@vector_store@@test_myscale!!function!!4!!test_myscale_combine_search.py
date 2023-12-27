def test_myscale_combine_search(
    documents: List[Document], query: VectorStoreQuery
) -> None:
    client = clickhouse_connect.get_client(
        host=MYSCALE_CLUSTER_URL,
        port=8443,
        username=MYSCALE_USERNAME,
        password=MYSCALE_CLUSTER_PASSWORD,
    )
    vector_store = MyScaleVectorStore(myscale_client=client)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    query.query_embedding = index.service_context.embed_model.get_query_embedding(
        cast(str, query.query_str)
    )
    responseNodes = cast(List[BaseNode], index._vector_store.query(query).nodes)
    assert len(responseNodes) == 1
    assert responseNodes[0].id_ == "1"
    cast(MyScaleVectorStore, index._vector_store).drop()
