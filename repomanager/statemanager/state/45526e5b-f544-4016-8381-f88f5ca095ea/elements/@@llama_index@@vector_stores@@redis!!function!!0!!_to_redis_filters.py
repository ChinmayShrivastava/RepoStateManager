def _to_redis_filters(metadata_filters: MetadataFilters) -> str:
    tokenizer = TokenEscaper()

    filter_strings = []
    for filter in metadata_filters.legacy_filters():
        # adds quotes around the value to ensure that the filter is treated as an
        #   exact match
        filter_string = f"@{filter.key}:{{{tokenizer.escape(str(filter.value))}}}"
        filter_strings.append(filter_string)

    joined_filter_strings = " & ".join(filter_strings)
    return f"({joined_filter_strings})"
