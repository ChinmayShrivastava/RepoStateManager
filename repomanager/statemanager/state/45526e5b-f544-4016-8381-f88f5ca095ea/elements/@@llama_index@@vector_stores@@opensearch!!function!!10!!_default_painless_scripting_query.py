def _default_painless_scripting_query(
    query_vector: List[float],
    k: int = 4,
    space_type: str = "l2Squared",
    pre_filter: Optional[Union[Dict, List]] = None,
    vector_field: str = "embedding",
) -> Dict:
    """For Painless Scripting Search, this is the default query."""
    if not pre_filter:
        pre_filter = MATCH_ALL_QUERY

    source = __get_painless_scripting_source(space_type, vector_field)
    return {
        "size": k,
        "query": {
            "script_score": {
                "query": pre_filter,
                "script": {
                    "source": source,
                    "params": {
                        "field": vector_field,
                        "query_value": query_vector,
                    },
                },
            }
        },
    }
