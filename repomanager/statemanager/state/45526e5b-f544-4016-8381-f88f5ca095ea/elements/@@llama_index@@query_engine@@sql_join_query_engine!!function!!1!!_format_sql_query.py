def _format_sql_query(sql_query: str) -> str:
    """Format SQL query."""
    return sql_query.replace("\n", " ").replace("\t", " ")
