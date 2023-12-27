def redis_docstore(redis_kvstore: RedisKVStore) -> RedisDocumentStore:
    return RedisDocumentStore(redis_kvstore=redis_kvstore)
