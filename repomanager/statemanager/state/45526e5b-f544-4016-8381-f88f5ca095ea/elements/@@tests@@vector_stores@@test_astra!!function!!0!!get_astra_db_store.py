def get_astra_db_store() -> AstraDBVectorStore:
    return AstraDBVectorStore(
        token="AstraCS:<...>",
        api_endpoint=f"https://<...>",
        collection_name="test_collection",
        embedding_dimension=2,
        namespace="default_keyspace",
        ttl_seconds=123,
    )
