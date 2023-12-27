def _wrap_query(query: QueryType) -> QueryBundle:
    if isinstance(query, QueryBundle):
        return query
    elif isinstance(query, str):
        return QueryBundle(query_str=query)
    else:
        raise ValueError(f"Unexpected type: {type(query)}")
