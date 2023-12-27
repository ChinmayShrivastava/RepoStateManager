def _to_mongodb_filter(standard_filters: MetadataFilters) -> Dict:
    """Convert from standard dataclass to filter dict."""
    filters = {}
    for filter in standard_filters.legacy_filters():
        filters[filter.key] = filter.value
    return filters
