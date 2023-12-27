def _parse_filters(filters: Optional[MetadataFilters]) -> Any:
    pre_filter = []
    if filters is not None:
        for f in filters.legacy_filters():
            pre_filter.append({f.key: json.loads(str(f.value))})

    return pre_filter
