def _default_approximate_search_query(
    query_vector: List[float],
    k: int = 4,
    vector_field: str = "embedding",
) -> Dict:
    """For Approximate k-NN Search, this is the default query."""
    return {
        "size": k,
        "query": {"knn": {vector_field: {"vector": query_vector, "k": k}}},
    }
