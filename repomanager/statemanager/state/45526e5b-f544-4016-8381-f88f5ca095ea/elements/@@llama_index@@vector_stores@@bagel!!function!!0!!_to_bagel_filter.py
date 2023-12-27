def _to_bagel_filter(standard_filters: MetadataFilters) -> dict:
    """
    Translate standard metadata filters to Bagel specific spec.
    """
    filters = {}
    for filter in standard_filters.legacy_filters():
        filters[filter.key] = filter.value
    return filters
