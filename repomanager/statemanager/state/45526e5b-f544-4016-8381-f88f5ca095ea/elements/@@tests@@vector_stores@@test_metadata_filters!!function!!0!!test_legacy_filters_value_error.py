def test_legacy_filters_value_error() -> None:
    """Test legacy filters."""
    filters = [
        MetadataFilter(key="key1", value="value1", operator=FilterOperator.GTE),
        MetadataFilter(key="key2", value="value2"),
        ExactMatchFilter(key="key3", value="value3"),
    ]
    metadata_filters = MetadataFilters(filters=filters)

    with pytest.raises(ValueError):
        metadata_filters.legacy_filters()
