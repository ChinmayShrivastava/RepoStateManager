def es_store(index_name: str, elasticsearch_connection: Dict) -> ElasticsearchStore:
    return ElasticsearchStore(
        **elasticsearch_connection,
        index_name=index_name,
        distance_strategy="EUCLIDEAN_DISTANCE",
    )
