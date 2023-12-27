def _to_metal_filters(standard_filters: MetadataFilters) -> list:
    filters = []
    for filter in standard_filters.legacy_filters():
        filters.append(
            {
                "field": filter.key,
                "value": filter.value,
            }
        )
    return filters
