def test_build_query_filter_returns_combined_filter() -> None:
    from qdrant_client.http.models import (
        FieldCondition,
        Filter,
        MatchAny,
        MatchValue,
        Range,
    )

    client = qdrant_client.QdrantClient(":memory:")
    qdrant_vector_store = QdrantVectorStore(collection_name="test", client=client)

    filters = MetadataFilters(
        filters=[
            ExactMatchFilter(key="text_field", value="text_value"),
            ExactMatchFilter(key="int_field", value=4),
            ExactMatchFilter(key="float_field", value=3.5),
        ]
    )
    query = VectorStoreQuery(doc_ids=["1", "2", "3"], filters=filters)
    query_filter = cast(Filter, qdrant_vector_store._build_query_filter(query))

    assert query_filter is not None
    assert len(query_filter.must) == 4  # type: ignore[index, arg-type]

    assert isinstance(query_filter.must[0], FieldCondition)  # type: ignore[index]
    assert query_filter.must[0].key == "doc_id"  # type: ignore[index]
    assert isinstance(query_filter.must[0].match, MatchAny)  # type: ignore[index]
    assert query_filter.must[0].match.any == ["1", "2", "3"]  # type: ignore[index]

    assert isinstance(query_filter.must[1], FieldCondition)  # type: ignore[index]
    assert query_filter.must[1].key == "text_field"  # type: ignore[index]
    assert isinstance(query_filter.must[1].match, MatchValue)  # type: ignore[index]
    assert query_filter.must[1].match.value == "text_value"  # type: ignore[index]

    assert isinstance(query_filter.must[2], FieldCondition)  # type: ignore[index]
    assert query_filter.must[2].key == "int_field"  # type: ignore[index]
    assert isinstance(query_filter.must[2].match, MatchValue)  # type: ignore[index]
    assert query_filter.must[2].match.value == 4  # type: ignore[index]

    assert isinstance(query_filter.must[3], FieldCondition)  # type: ignore[index]
    assert query_filter.must[3].key == "float_field"  # type: ignore[index]
    assert isinstance(query_filter.must[3].range, Range)  # type: ignore[index]
    assert query_filter.must[3].range.gte == 3.5  # type: ignore[index]
    assert query_filter.must[3].range.lte == 3.5  # type: ignore[index]
