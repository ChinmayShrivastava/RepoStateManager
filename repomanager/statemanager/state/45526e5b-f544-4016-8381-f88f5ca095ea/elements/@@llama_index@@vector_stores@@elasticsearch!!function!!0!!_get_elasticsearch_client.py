def _get_elasticsearch_client(
    *,
    es_url: Optional[str] = None,
    cloud_id: Optional[str] = None,
    api_key: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> Any:
    """Get AsyncElasticsearch client.

    Args:
        es_url: Elasticsearch URL.
        cloud_id: Elasticsearch cloud ID.
        api_key: Elasticsearch API key.
        username: Elasticsearch username.
        password: Elasticsearch password.

    Returns:
        AsyncElasticsearch client.

    Raises:
        ConnectionError: If Elasticsearch client cannot connect to Elasticsearch.
    """
    try:
        import elasticsearch
    except ImportError:
        raise ImportError(
            "Could not import elasticsearch python package. "
            "Please install it with `pip install elasticsearch`."
        )

    if es_url and cloud_id:
        raise ValueError(
            "Both es_url and cloud_id are defined. Please provide only one."
        )

    if es_url and cloud_id:
        raise ValueError(
            "Both es_url and cloud_id are defined. Please provide only one."
        )

    connection_params: Dict[str, Any] = {}

    if es_url:
        connection_params["hosts"] = [es_url]
    elif cloud_id:
        connection_params["cloud_id"] = cloud_id
    else:
        raise ValueError("Please provide either elasticsearch_url or cloud_id.")

    if api_key:
        connection_params["api_key"] = api_key
    elif username and password:
        connection_params["basic_auth"] = (username, password)

    sync_es_client = elasticsearch.Elasticsearch(
        **connection_params, headers={"user-agent": ElasticsearchStore.get_user_agent()}
    )
    async_es_client = elasticsearch.AsyncElasticsearch(**connection_params)
    try:
        sync_es_client.info()  # so don't have to 'await' to just get info
    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")
        raise

    return async_es_client
