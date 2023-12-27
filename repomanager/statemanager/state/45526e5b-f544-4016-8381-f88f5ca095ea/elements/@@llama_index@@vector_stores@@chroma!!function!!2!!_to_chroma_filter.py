def _to_chroma_filter(
    standard_filters: MetadataFilters,
) -> dict:
    """Translate standard metadata filters to Chroma specific spec."""
    filters = {}
    filters_list = []
    condition = standard_filters.condition or "and"
    condition = _transform_chroma_filter_condition(condition)
    if standard_filters.filters:
        for filter in standard_filters.filters:
            if filter.operator:
                filters_list.append(
                    {
                        filter.key: {
                            _transform_chroma_filter_operator(
                                filter.operator
                            ): filter.value
                        }
                    }
                )
            else:
                filters_list.append({filter.key: filter.value})

    if len(filters_list) == 1:
        # If there is only one filter, return it directly
        return filters_list[0]
    elif len(filters_list) > 1:
        filters[condition] = filters_list
    return filters
