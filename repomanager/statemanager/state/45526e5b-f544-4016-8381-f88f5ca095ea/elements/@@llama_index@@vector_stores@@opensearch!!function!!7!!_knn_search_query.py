def _knn_search_query(
    embedding_field: str,
    query_embedding: List[float],
    k: int,
    filters: Optional[MetadataFilters] = None,
) -> Dict:
    """Do knn search.

    If there are no filters do approx-knn search.
    If there are (pre)-filters, do an exhaustive exact knn search using 'painless
        scripting'.

    Note that approximate knn search does not support pre-filtering.

    Args:
        query_embedding: Vector embedding to query.
        k: Maximum number of results.
        filters: Optional filters to apply before the search.
            Supports filter-context queries documented at
            https://opensearch.org/docs/latest/query-dsl/query-filter-context/

    Returns:
        Up to k docs closest to query_embedding
    """
    if filters is None:
        search_query = _default_approximate_search_query(
            query_embedding, k, vector_field=embedding_field
        )
    else:
        pre_filter = _parse_filters(filters)
        # https://opensearch.org/docs/latest/search-plugins/knn/painless-functions/
        search_query = _default_painless_scripting_query(
            query_embedding,
            k,
            space_type="l2Squared",
            pre_filter={"bool": {"filter": pre_filter}},
            vector_field=embedding_field,
        )

    return search_query
