def _default_check_stop(query_bundle: QueryBundle) -> bool:
    """Default check stop function."""
    return query_bundle.query_str.lower() == "none"
