def _build_metadata_filter_fn(
    metadata_lookup_fn: Callable[[str], Mapping[str, Any]],
    metadata_filters: Optional[MetadataFilters] = None,
) -> Callable[[str], bool]:
    """Build metadata filter function."""
    filter_list = metadata_filters.legacy_filters() if metadata_filters else []
    if not filter_list:
        return lambda _: True

    def filter_fn(node_id: str) -> bool:
        metadata = metadata_lookup_fn(node_id)
        for filter_ in filter_list:
            metadata_value = metadata.get(filter_.key, None)
            if metadata_value is None:
                return False
            elif isinstance(metadata_value, list):
                if filter_.value not in metadata_value:
                    return False
            elif isinstance(metadata_value, (int, float, str, bool)):
                if metadata_value != filter_.value:
                    return False
        return True

    return filter_fn
