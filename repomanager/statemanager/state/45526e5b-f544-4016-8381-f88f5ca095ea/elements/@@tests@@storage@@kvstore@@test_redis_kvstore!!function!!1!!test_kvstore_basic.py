def test_kvstore_basic(redis_kvstore: RedisKVStore) -> None:
    test_key = "test_key"
    test_blob = {"test_obj_key": "test_obj_val"}
    redis_kvstore.put(test_key, test_blob)
    blob = redis_kvstore.get(test_key)
    assert blob == test_blob

    blob = redis_kvstore.get(test_key, collection="non_existent")
    assert blob is None
