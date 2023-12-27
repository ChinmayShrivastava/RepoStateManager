def _to_filter_expr(filters: MetadataFilters) -> str:
    conditions = []
    for f in filters.legacy_filters():
        value = str(f.value)
        if isinstance(f.value, str):
            value = '"' + value + '"'
        conditions.append(f"{f.key}=={value}")
    return "&&".join(conditions)
