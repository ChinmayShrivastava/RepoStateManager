def _get_opensearch_client(opensearch_url: str, **kwargs: Any) -> Any:
    """Get OpenSearch client from the opensearch_url, otherwise raise error."""
    try:
        opensearch = _import_opensearch()
        client = opensearch(opensearch_url, **kwargs)

    except ValueError as e:
        raise ValueError(
            f"OpenSearch client string provided is not in proper format. "
            f"Got error: {e} "
        )
    return client
