def test_build_query_filter_returns_empty_filter_on_query_str() -> None:
    from qdrant_client.http.models import Filter

    client = qdrant_client.QdrantClient(":memory:")
    qdrant_vector_store = QdrantVectorStore(collection_name="test", client=client)

    query = VectorStoreQuery(query_str="lorem")
    query_filter = cast(Filter, qdrant_vector_store._build_query_filter(query))

    assert query_filter is not None
    assert len(query_filter.must) == 0  # type: ignore[index, arg-type]
