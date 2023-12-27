def collection_exists(client: Any, collection_name: str = "test") -> bool:
    try:
        client.Collections.get(collection=collection_name)
    except rockset.exceptions.NotFoundException:
        return False
    return True
