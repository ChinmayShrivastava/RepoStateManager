def test_instance_creation(index_name: str, elasticsearch_connection: Dict) -> None:
    es_store = ElasticsearchStore(
        **elasticsearch_connection,
        index_name=index_name,
    )
    assert isinstance(es_store, ElasticsearchStore)
