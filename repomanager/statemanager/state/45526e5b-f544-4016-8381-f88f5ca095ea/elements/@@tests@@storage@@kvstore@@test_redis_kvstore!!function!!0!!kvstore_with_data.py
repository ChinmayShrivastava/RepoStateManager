def kvstore_with_data(redis_kvstore: RedisKVStore) -> RedisKVStore:
    test_key = "test_key"
    test_blob = {"test_obj_key": "test_obj_val"}
    redis_kvstore.put(test_key, test_blob)
    return redis_kvstore
