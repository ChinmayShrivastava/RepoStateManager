def _import_opensearch() -> Any:
    """Import OpenSearch if available, otherwise raise error."""
    try:
        from opensearchpy import OpenSearch
    except ImportError:
        raise ValueError(IMPORT_OPENSEARCH_PY_ERROR)
    return OpenSearch
