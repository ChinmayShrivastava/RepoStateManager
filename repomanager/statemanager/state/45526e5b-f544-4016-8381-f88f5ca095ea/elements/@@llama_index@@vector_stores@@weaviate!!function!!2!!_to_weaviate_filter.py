def _to_weaviate_filter(standard_filters: MetadataFilters) -> Dict[str, Any]:
    filters_list = []
    condition = standard_filters.condition or "and"
    condition = _transform_weaviate_filter_condition(condition)

    if standard_filters.filters:
        for filter in standard_filters.filters:
            value_type = "valueText"
            if isinstance(filter.value, float):
                value_type = "valueNumber"
            elif isinstance(filter.value, int):
                value_type = "valueNumber"
            filters_list.append(
                {
                    "path": filter.key,
                    "operator": _transform_weaviate_filter_operator(filter.operator),
                    value_type: filter.value,
                }
            )
    else:
        return {}

    if len(filters_list) == 1:
        # If there is only one filter, return it directly
        return filters_list[0]

    return {"operands": filters_list, "operator": condition}
