def test_kvstore_getall(redis_kvstore: RedisKVStore) -> None:
    test_key = "test_key"
    test_blob = {"test_obj_key": "test_obj_val"}
    redis_kvstore.put(test_key, test_blob)
    blob = redis_kvstore.get(test_key)
    assert blob == test_blob
    test_key = "test_key_2"
    test_blob = {"test_obj_key": "test_obj_val"}
    redis_kvstore.put(test_key, test_blob)
    blob = redis_kvstore.get(test_key)
    assert blob == test_blob

    blob = redis_kvstore.get_all()
    assert len(blob) == 2
