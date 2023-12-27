def test_elasticsearch_embedding_constructor(
    model_id: str, es_url: str, es_username: str, es_password: str
) -> None:
    """Test Elasticsearch embedding query."""
    ElasticsearchEmbedding.from_credentials(
        model_id=model_id,
        es_url=es_url,
        es_username=es_username,
        es_password=es_password,
    )
