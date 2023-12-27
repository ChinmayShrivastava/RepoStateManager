def default_stop_fn(stop_dict: Dict) -> bool:
    """Stop function for multi-step query combiner."""
    query_bundle = cast(QueryBundle, stop_dict.get("query_bundle"))
    if query_bundle is None:
        raise ValueError("Response must be provided to stop function.")

    return "none" in query_bundle.query_str.lower()
