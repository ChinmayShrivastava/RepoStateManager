def get_redis_query(
    return_fields: List[str],
    top_k: int = 20,
    vector_field: str = "vector",
    sort: bool = True,
    filters: str = "*",
) -> "Query":
    """Create a vector query for use with a SearchIndex.

    Args:
        return_fields (t.List[str]): A list of fields to return in the query results
        top_k (int, optional): The number of results to return. Defaults to 20.
        vector_field (str, optional): The name of the vector field in the index.
            Defaults to "vector".
        sort (bool, optional): Whether to sort the results by score. Defaults to True.
        filters (str, optional): string to filter the results by. Defaults to "*".

    """
    from redis.commands.search.query import Query

    base_query = f"{filters}=>[KNN {top_k} @{vector_field} $vector AS vector_score]"

    query = Query(base_query).return_fields(*return_fields).dialect(2).paging(0, top_k)

    if sort:
        query.sort_by("vector_score")
    return query
