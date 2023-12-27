def _to_elasticsearch_filter(standard_filters: MetadataFilters) -> Dict[str, Any]:
    """Convert standard filters to Elasticsearch filter.

    Args:
        standard_filters: Standard Llama-index filters.

    Returns:
        Elasticsearch filter.
    """
    if len(standard_filters.legacy_filters()) == 1:
        filter = standard_filters.legacy_filters()[0]
        return {
            "term": {
                f"metadata.{filter.key}.keyword": {
                    "value": filter.value,
                }
            }
        }
    else:
        operands = []
        for filter in standard_filters.legacy_filters():
            operands.append(
                {
                    "term": {
                        f"metadata.{filter.key}.keyword": {
                            "value": filter.value,
                        }
                    }
                }
            )
        return {"bool": {"must": operands}}
