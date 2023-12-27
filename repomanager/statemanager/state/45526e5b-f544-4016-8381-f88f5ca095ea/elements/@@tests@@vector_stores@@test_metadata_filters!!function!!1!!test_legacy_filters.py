def test_legacy_filters() -> None:
    filters = [
        ExactMatchFilter(key="key1", value="value1"),
        ExactMatchFilter(key="key2", value="value2"),
    ]
    metadata_filters = MetadataFilters(filters=filters)
    legacy_filters = metadata_filters.legacy_filters()

    assert len(legacy_filters) == 2
    assert legacy_filters[0].key == "key1"
    assert legacy_filters[0].value == "value1"
    assert legacy_filters[1].key == "key2"
    assert legacy_filters[1].value == "value2"
