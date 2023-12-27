def test_build_query_filter_returns_match_any() -> None:
    from qdrant_client.http.models import FieldCondition, Filter, MatchAny

    client = qdrant_client.QdrantClient(":memory:")
    qdrant_vector_store = QdrantVectorStore(collection_name="test", client=client)

    query = VectorStoreQuery(doc_ids=["1", "2", "3"])
    query_filter = cast(Filter, qdrant_vector_store._build_query_filter(query))

    assert query_filter is not None
    assert len(query_filter.must) == 1  # type: ignore[index, arg-type]
    assert isinstance(query_filter.must[0], FieldCondition)  # type: ignore[index]
    assert query_filter.must[0].key == "doc_id"  # type: ignore[index]
    assert isinstance(query_filter.must[0].match, MatchAny)  # type: ignore[index]
    assert query_filter.must[0].match.any == ["1", "2", "3"]  # type: ignore[index]
