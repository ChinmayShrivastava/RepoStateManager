def _generate_sql(
    llama_index: SQLStructStoreIndex,
    nl_query_text: str,
) -> str:
    """Generate SQL query for the given NL query text."""
    query_engine = llama_index.as_query_engine()
    response = query_engine.query(nl_query_text)
    if (
        response.metadata is None
        or "sql_query" not in response.metadata
        or response.metadata["sql_query"] is None
    ):
        raise RuntimeError("No SQL query generated.")
    query = response.metadata["sql_query"]
    # Remove newlines and extra spaces.
    query = _newlines.sub(" ", query)
    query = _spaces.sub(" ", query)
    return query.strip()
