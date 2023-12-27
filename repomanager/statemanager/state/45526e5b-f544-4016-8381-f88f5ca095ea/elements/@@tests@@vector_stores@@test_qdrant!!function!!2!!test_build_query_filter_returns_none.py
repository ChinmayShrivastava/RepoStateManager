def test_build_query_filter_returns_none() -> None:
    client = qdrant_client.QdrantClient(":memory:")
    qdrant_vector_store = QdrantVectorStore(collection_name="test", client=client)

    query = VectorStoreQuery()
    query_filter = qdrant_vector_store._build_query_filter(query)

    assert query_filter is None
