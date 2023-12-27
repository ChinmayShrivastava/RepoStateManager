def _import_bulk() -> Any:
    """Import bulk if available, otherwise raise error."""
    try:
        from opensearchpy.helpers import bulk
    except ImportError:
        raise ValueError(IMPORT_OPENSEARCH_PY_ERROR)
    return bulk
