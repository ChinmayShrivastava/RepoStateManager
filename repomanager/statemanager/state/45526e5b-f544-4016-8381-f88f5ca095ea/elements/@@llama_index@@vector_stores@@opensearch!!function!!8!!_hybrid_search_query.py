def _hybrid_search_query(
    text_field: str,
    query_str: str,
    embedding_field: str,
    query_embedding: List[float],
    k: int,
    filters: Optional[MetadataFilters] = None,
) -> Dict:
    knn_query = _knn_search_query(embedding_field, query_embedding, k, filters)["query"]
    lexical_query = {"must": {"match": {text_field: {"query": query_str}}}}

    parsed_filters = _parse_filters(filters)
    if len(parsed_filters) > 0:
        lexical_query["filter"] = parsed_filters
    return {
        "size": k,
        "query": {"hybrid": {"queries": [{"bool": lexical_query}, knn_query]}},
    }
