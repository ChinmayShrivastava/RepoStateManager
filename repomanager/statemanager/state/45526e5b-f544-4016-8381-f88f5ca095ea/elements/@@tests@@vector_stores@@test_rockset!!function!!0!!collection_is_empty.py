def collection_is_empty(client: Any, collection_name: str = "test") -> bool:
    return len(client.sql(f"SELECT _id FROM {collection_name} LIMIT 1").results) == 0
