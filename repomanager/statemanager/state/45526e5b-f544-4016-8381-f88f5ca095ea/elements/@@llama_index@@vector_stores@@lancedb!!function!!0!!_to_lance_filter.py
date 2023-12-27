def _to_lance_filter(standard_filters: MetadataFilters) -> Any:
    """Translate standard metadata filters to Lance specific spec."""
    filters = []
    for filter in standard_filters.legacy_filters():
        if isinstance(filter.value, str):
            filters.append(filter.key + ' = "' + filter.value + '"')
        else:
            filters.append(filter.key + " = " + str(filter.value))
    return " AND ".join(filters)
