def _get_client(api_key: str | None, api_server: str | None, client: Any | None) -> Any:
    """Returns the passed in client object if valid, else
    constructs and returns one.

    Returns:
        The rockset client object (rockset.RocksetClient)
    """
    rockset = _get_rockset()
    if client:
        if type(client) is not rockset.RocksetClient:
            raise ValueError("Parameter `client` must be of type rockset.RocksetClient")
    elif not api_key and not getenv("ROCKSET_API_KEY"):
        raise ValueError(
            "Parameter `client`, `api_key` or env var `ROCKSET_API_KEY` must be set"
        )
    else:
        client = rockset.RocksetClient(
            api_key=api_key or getenv("ROCKSET_API_KEY"),
            host=api_server or getenv("ROCKSET_API_SERVER"),
        )
    return client
