def validate_client(client: Any) -> None:
    """Validate client and import weaviate library."""
    try:
        import weaviate  # noqa
        from weaviate import Client

        client = cast(Client, client)
    except ImportError:
        raise ImportError(
            "Weaviate is not installed. "
            "Please install it with `pip install weaviate-client`."
        )
    cast(Client, client)
